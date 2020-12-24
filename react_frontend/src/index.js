import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import ModelGen from './components/model';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.css';
import 'jquery/dist/jquery';
import 'popper.js/dist/esm/popper';
import 'bootstrap/dist/js/bootstrap';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

ReactDOM.render(
  <React.StrictMode>
    <div className="App">
      <Router>
        <header className='navbar navbar-expand-md navbar-dark bg-success'>
          <a href='./' className='navbar-brand'>
            Titanic Survival Prediction
          </a>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto ml-3">
              <li className="nav-item">
                <Link to='/' className='btn btn-link text-white'>Home</Link>
              </li>
              <li className="nav-item">
                <Link to='/generate' className='btn btn-link text-white'>Model</Link>
              </li>
            </ul>
          </div>
        </header>
        <Route exact path='/' strict={true} component={App} />
        <Route exact path='/generate' strict={true} component={ModelGen} />
      </Router>
      <footer className='container-fluid bg-dark pb-3 pt-3'>
        <div className='row'>
          <div className='col-12 text-center text-white'>
            <h5>© Param Siddharth 2020</h5>
          </div>
        </div>
      </footer>
    </div>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
