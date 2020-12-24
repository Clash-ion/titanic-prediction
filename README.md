# Titanic Survival Prediction
A web application that predicts the survival of a Titanic passenger.

The back-end is made using Flask in Python, and located inside `model_service`.  
The front-end is made using React in NodeJS, and located inside `react_frontend`.

## Development (Back-end)
Go to the back-end directory.
``` bash
cd model_service
```

It is suggested to create and activate a Python virtual environment before proceeding, to avoid polluting the local Python installation.
``` bash
python -m venv env
. ./env/bin/activate # This step may be different in other operating systems
```

Install `wheel`, which is required for the installation of many dependencies and needs to be installed prior to them.
``` bash
pip install wheel
```

Install the PyPI requirements as needed.
``` bash
pip install requirements.txt
```

There are 2 `requirements.txt` files, one for generating the model, and another for running the back-end server in Flask (Python).
- Model-only dependencies: `model_service/model/requirements.txt`
- Model and server dependencies: `model_service/requirements.txt`

The former is just a subset of the latter. Hence, the server `requirements.txt` is preferred.

Before starting the server, the `FLASK_RUN_HOST` and `FLASK_RUN_PORT` environment variables should be set to the desired host URL and port. If not, default values will be used.

The server may either be started using the `flask` command or manually executing `app.py`. Both will behave differently if the environment variables aren't assigned values.
- ``` bash
  # If variables are not set, uses 127.0.0.1 and 5000 as the default values
  flask run
  ```
- ``` bash
  # If variables are not set, uses 0.0.0.0 and 3000 as the default values
  python app.py
  ```
- ``` bash
  # Values may be supplied separately to 'flask run'
  flask run --host=0.0.0.0 --port=3000
  ```

This will start the server. Using `python app.py` is preferred, which would start the server on http://localhost:3000/.

## Development (Front-end)
Go to the front-end directory.
``` bash
cd react_frontend
```

Install the Node.js modules using `package.json` using either of the following commands:
- ``` bash
  npm ci
  ```
- ``` bash
  npm install
  ```

The `REACT_APP_API_URL` environment variable must be set to the API server URL. By default, the React application assumes the server to be running on http://localhost:3000/.

The development server will run on http://localhost:3006/ by default. To start it, execute:
``` bash
npm start
```

To build a production-optimized build for the React application, use the following command. Make sure to set the `REACT_APP_API_URL` variable to point to the API URL before building.
``` bash
npm run build
```

The production build will be created in the `react_frontend/build` directory and may then be statically served.

# Made with ❤ by [Param](http://www.paramsid.com).