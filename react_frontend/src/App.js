import React, { Component } from 'react';
import predictSurvival from './services/prediction';
import './App.css';

const Prediction = (props) => {
  if (props.result === null)
    return <h4>Enter the data and submit to retrieve the prediction.</h4>;
  if (props.result.status === 'WAITING')
    return <h4>Loading...</h4>;
  if (props.result.status === 'FAIL')
    return <h4 className='text-danger'>Error: { props.result.error }</h4>;
  if (props.result.status === 'SUCCESS') {
    if (props.result.result)
      return <h4 className='text-success'>The person survives.</h4>
    else
      return <h4 className='text-secondary'>The person doesn't survive.</h4>;
  }
  return <h4 className='text-danger'>Error: Unknown error.</h4>;
};

class App extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);

    this.state = {
      pid: '',
      pclass: '1',
      sex: 'male',
      age: 0,
      sibsp: 0,
      parch: 0,
      fare: 0.0,
      embarked: 'C',
      pidTouched: false,
      result: null
    };
  }

  handleChange(e) {
    if (e.target.id === 'pid')
      this.setState({ pidTouched: true });
    this.setState({ [e.target.id]: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    if (!this.state.pidTouched) {
      this.setState({ pidTouched: true });
      return;
    }
    this.setState({
      result: { status: 'WAITING' }
    });
    let queryArgs = {
      pid: this.state.pid,
      pclass: this.state.pclass,
      sex: this.state.sex,
      age: this.state.age,
      sibsp: this.state.sibsp,
      parch: this.state.parch,
      fare: this.state.fare,
      embarked: this.state.embarked
    };
    predictSurvival(queryArgs)
      .then(resp => this.setState({ result: resp.data }))
      .catch(err => {
        if (err.response)
          this.setState({ result: err.response.data });
        else
          this.setState({ result: {
            status: 'FAIL',
            statusCode: 404,
            error: 'Request failed.'
          } })
      });
  }

  render() {
    return (
      <div className="App">
        <header className='navbar navbar-dark bg-success'>
          <a href='./' className='navbar-brand'>
            Titanic Survival Prediction
          </a>
        </header>
        <main className='container-fluid mt-3 mb-4'>
          <div className='row'>
            <h1 className='col-12'>Titanic Survival Prediction</h1>
          </div>
          <form onSubmit={this.handleSubmit} className='row pl-4 pr-4 mt-1'>
            <div  className='form-group col-12'>
              <label htmlFor='pid'>Passenger ID: </label>
              <input type='text' id='pid' value={this.state.pid} onChange={this.handleChange}
                placeholder='Passenger ID' className='form-control' />
              { this.state.pid === '' && this.state.pidTouched ? <small className='text-danger'>Can't be empty.</small> : '' }
            </div>
            <div className='form-group col-12'>
              <label htmlFor='pclass'>Class: </label>
              <select id='pclass' className='form-control'
                value={this.state.pclass} onChange={this.handleChange}>
                <option value='1'>1</option>
                <option value='2'>2</option>
                <option value='3'>3</option>
              </select>
            </div>
            <div  className='form-group col-12'>
              <label htmlFor='sex'>Sex: </label>
              <select id='sex' className='form-control'
                value={this.state.sex} onChange={this.handleChange}>
                <option value='male'>Male</option>
                <option value='female'>Female</option>
              </select>
            </div>
            <div  className='form-group col-12'>
              <label htmlFor='age'>Age: </label>
              <input type='number' id='age' min='0' max='150'
                value={this.state.age} onChange={this.handleChange}
                placeholder='Age' className='form-control' />
              { this.state.age === '' ? <small className='text-danger'>Can't be empty.</small> : '' }
            </div>
            <div  className='form-group col-12'>
              <label htmlFor='sibsp'>Number of Siblings/Spouses Aboard: </label>
              <input type='number' id='sibsp' min='0'
                value={this.state.sibsp} onChange={this.handleChange}
                placeholder='Number of Siblings/Spouses Aboard'
                className='form-control' />
              { this.state.sibsp === '' ? <small className='text-danger'>Can't be empty.</small> : '' }
            </div>
            <div  className='form-group col-12'>
              <label htmlFor='sibsp'>Number of Parents/Children: </label>
              <input type='number' id='parch' min='0'
                value={this.state.parch} onChange={this.handleChange}
                placeholder='Number of Parents/Children Aboard'
                className='form-control' />
              { this.state.parch === '' ? <small className='text-danger'>Can't be empty.</small> : '' }
            </div>
            <div  className='form-group col-12'>
              <label htmlFor='fare'>Fare: </label>
              <input type='number' id='fare' min='0'
                placeholder='Fare'
                value={this.state.fare} onChange={this.handleChange}
                className='form-control' />
              { this.state.fare === '' ? <small className='text-danger'>Can't be empty.</small> : '' }
            </div>
            <div  className='form-group col-12'>
              <label htmlFor='embarked'>Port of Embarkation: </label>
              <select id='embarked' className='form-control'
                value={this.state.embarked} onChange={this.handleChange}>
                <option value='C'>Cherbourg</option>
                <option value='Q'>Queenstown</option>
                <option value='S'>Southampton</option>
              </select>
            </div>
            <div className='form-group col-12 col-md-4 offset-md-4'>
              <button className='btn btn-block btn-primary'
                type='submit'
                disabled={
                     this.state.pid === '' && this.state.pidTouched
                  || this.state.age === ''
                  || this.state.sibsp === ''
                  || this.state.parch === ''
                  || this.state.fare === ''
                }
                >Predict Survival</button>
            </div>
          </form>
          <div className='row pl-4 pr-4'>
            <div className='col-12'>
              <Prediction result={this.state.result} />
            </div>
          </div>
        </main>
      </div>
    );
  }
};

export default App;
