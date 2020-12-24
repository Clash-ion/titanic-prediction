from flask import Flask, request
from sys import exit, stderr
from os import environ, path, getcwd
import json
import joblib
import numpy as np

app = Flask(__name__)
try:
	port = int(environ.get('FLASK_RUN_PORT', 3000))
except:
	port = 3000
host = environ.get('FLASK_RUN_HOST', '0.0.0.0')

try:
	model = joblib.load(path.join(getcwd(), 'model', 'model_joblib'))
except Exception as e:
	stderr.write(f'Error: {e.args}')
	exit(1)

@app.route('/', methods=['GET'])
def predict():
	params = [
		('PassengerId', np.int64),
		('Pclass', np.int64),
		('Sex_male', np.float64),
		('Sex_female', np.float64),
		('Age', np.float64),
		('SibSp', np.int64),
		('Parch', np.int64),
		('Fare', np.float64),
		('Embarked_S', np.float64),
		('Embarked_C', np.float64),
		('Embarked_Q', np.float64)
	]
	values = []
	for param in params:
		value = request.args.get(param[0])
		if value is None:
			resp = {
				'status': 'FAIL',
				'statusCode': 400,
				'error': 'Invalid arguments.'
			}
			return json.dumps(resp), 400
		try:
			values.append(param[1](value))
		except:
			resp = {
				'status': 'FAIL',
				'statusCode': 400,
				'error': 'Invalid arguments.'
			}
			return json.dumps(resp), 400
	try:
		values_np = np.asarray(values).reshape(1, -1)
		pred = model.predict(values_np)[0]
	except:
		resp = {
			'status': 'FAIL',
			'statusCode': 400,
			'error': 'Invalid arguments.'
		}
		return json.dumps(resp), 400
	resp = {
		'status': 'SUCCESS',
		'statusCode': 200,
		'result': int(pred)
	}
	return json.dumps(resp), 200

if __name__ == '__main__':
	try:
		app.run(host=host, port=port, debug=False)
	except Exception as e:
		stderr.write(f'Error: {e.args}')
		exit(1)
