# Import modules
from flask import Flask, request, Response
from flask_cors import CORS
from sys import exit, stderr
from os import environ, path, getcwd
import json
import joblib
import numpy as np

# Initialize app
app = Flask(__name__)
CORS(app)
try:
	port = int(environ.get('FLASK_RUN_PORT', 3000))
except:
	port = 3000
host = environ.get('FLASK_RUN_HOST', '0.0.0.0')

# Load model
try:
	model = joblib.load(path.join(getcwd(), 'model', 'model_joblib'))
except Exception as e:
	stderr.write(f'Error: {e.args}')
	exit(1)

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
