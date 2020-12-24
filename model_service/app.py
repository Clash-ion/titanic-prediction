# Import modules
from flask import Flask, request, Response
from flask_cors import CORS
from sys import exit, stderr
from os import environ, path, getcwd
import json
import joblib
import numpy as np
from base64 import encodebytes
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from random import random

# Import model-generation dependencies
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import category_encoders as ce
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import joblib

# Initialize app
app = Flask(__name__)
CORS(app)
try:
	port = int(environ.get('FLASK_RUN_PORT', 3000))
except:
	port = 3000
host = environ.get('FLASK_RUN_HOST', '0.0.0.0')

# Load model
import make_model
try:
	model = joblib.load(path.join(getcwd(), 'model', 'model_joblib'))
except Exception as e:
	model = None

# Get image in the form of bytes
def get_image(fig):
	cv = FigureCanvas(fig)
	op = BytesIO()
	cv.print_png(op)
	return encodebytes(op.getvalue()).decode('ascii')


# Model-generation
@app.route('/generate', methods=['GET'])
def generate():
	df = pd.read_csv(path.join(getcwd(), 'model', "titanic.csv"))
	df['Age']= df['Age'].fillna(df['Age'].mean())
	df.dropna(subset=['Embarked'],inplace=True)
	num_cols = df.select_dtypes([np.int64,np.float64]).columns.tolist()
	num_cols.remove('PassengerId')
	i = 1
	fg1 = {}
	for col in num_cols:
		df.hist(column=col)
		fg1[col] = get_image(plt.figure(i))
		i += 1
	scatter_matrix(df[num_cols],figsize=(50,50))
	fg2 = get_image(plt.figure(i))
	i += 1
	obj_cols = df.select_dtypes([np.object]).columns.tolist()
	obj_cols.remove('Name')
	obj_cols.remove('Cabin')
	obj_cols.remove('Ticket')
	fg3 = {}
	for col in obj_cols:
		plt.figure(i)
		df[col].value_counts().plot(ax=plt.gca(), kind='bar')
		fg3[col] = get_image(plt.figure(i))
		i += 1
	y = pd.Series(df['Survived'])
	drop_list = ['Survived','Name','Ticket','Cabin']
	X = df.drop(drop_list,axis=1)
	encoder=ce.OneHotEncoder(handle_unknown='return_nan',return_df=True,use_cat_names=True)
	X = encoder.fit_transform(X)
	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)
	model = RandomForestClassifier()
	model.fit(X_train,y_train)
	scores = {}
	train_preds = model.predict(X_train)
	scores['Training'] = {
		'Accuracy': accuracy_score(train_preds,y_train),
		'F1': f1_score(train_preds,y_train),
		'ROC AUC': roc_auc_score(train_preds,y_train)
	}
	test_preds = model.predict(X_test)
	scores['Testing'] = {
		'Accuracy': accuracy_score(test_preds,y_test),
		'F1': f1_score(test_preds,y_test),
		'ROC AUC': roc_auc_score(test_preds,y_test)
	}
	# joblib.dump(model,path.join(getcwd(), 'model', "model_joblib"))
	# loaded_model = joblib.load("model_joblib")
	# array = [5,3,1.0,0.0,35.0,0,0,8.0500,1.0,0.0,0.0]
	# a = np.asarray(array).reshape(1,-1)
	# predicted_value= loaded_model.predict(a)
	# actual_value = y[4]
	tests = []
	MAX_TESTS = 8
	for j in range(0, min(MAX_TESTS, len(y_test))):
		predicted_value = int(test_preds[j])
		actual_value = int(y[j])
		tests.append([predicted_value == 1, actual_value == 1])
	plt.close('all')
	resp = {
		'status': 'SUCCESS',
		'statusCode': 200,
		'result': {
			'plots': {
				'histograms': fg1,
				'scatter': fg2,
				'value_counts': fg3
			},
			'scores': scores,
			'tests': tests
		}
	}
	return Response(response=json.dumps(resp), status=200, mimetype='application/json')

# Valid arguments for the API, with types
valid_params = [
	('pid', np.int64),
	('pclass', np.int64),
	('sex', np.float64),
	('age', np.float64),
	('sibsp', np.int64),
	('parch', np.int64),
	('fare', np.float64),
	('embarked', np.float64)
]

# Parse the sex argument
def parse_sex(sex):
	valid = [
		'male',
		'female'
	]
	result = []
	for val in valid:
		if sex == val:
			result.append(1.0)
		else:
			result.append(0.0)
	if result.count(1.0) == 1 and len(result) == len(valid):
		return result
	return None

# Parse the embarked argument
def parse_embarked(em):
	valid = [
		'S',
		'C',
		'Q'
	]
	result = []
	for val in valid:
		if em.upper() == val:
			result.append(1.0)
		else:
			result.append(0.0)
	if result.count(1.0) == 1 and len(result) == len(valid):
		return result
	return None

# All parsing functions
parse_arg = {
	'sex': parse_sex,
	'embarked': parse_embarked
}

# API route
@app.route('/', methods=['GET'])
def predict():
	# Input for model
	values = []

	# Read each argument
	for param in valid_params:
		value = request.args.get(param[0])

		# Argument not passed
		if value is None:
			resp = {
				'status': 'FAIL',
				'statusCode': 400,
				'error': f'Invalid value for argument "{param[0]}".'
			}
			return Response(response=json.dumps(resp), status=400, mimetype='application/json')
		
		# Categorical argument
		if param[0] in parse_arg.keys():
			try:
				parsed = parse_arg[param[0]](value)
				values += parsed
			except:
				resp = {
					'status': 'FAIL',
					'statusCode': 400,
					'error': f'Invalid value for argument "{param[0]}".'
				}
				return Response(response=json.dumps(resp), status=400, mimetype='application/json')
		# Numerical argument
		else:
			try:
				values.append(param[1](value))
			except:
				resp = {
					'status': 'FAIL',
					'statusCode': 400,
					'error': f'Invalid value for argument "{param[0]}".'
				}
				return Response(response=json.dumps(resp), status=400, mimetype='application/json')
	
	# Attempt prediction
	try:
		values_np = np.asarray(values).reshape(1, -1)
		pred = model.predict(values_np)[0]
	except:
		resp = {
			'status': 'FAIL',
			'statusCode': 400,
			'error': 'Invalid arguments.'
		}
		return Response(response=json.dumps(resp), status=400, mimetype='application/json')
	
	# Success
	resp = {
		'status': 'SUCCESS',
		'statusCode': 200,
		'result': int(pred) == 1
	}
	return Response(response=json.dumps(resp), status=200, mimetype='application/json')

# Run back-end API
if __name__ == '__main__':
	try:
		app.run(host=host, port=port, debug=False)
	except Exception as e:
		stderr.write(f'Error: {e.args}')
		exit(1)
