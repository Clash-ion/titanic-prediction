import React, { Component } from 'react';
import { generateModel } from '../services/prediction';
import Loader from 'react-loader-spinner';

const featNames = {
  Survived: 'Survived or not',
  Pclass: 'Class',
  Sex: 'Sex',
  Age: 'Age',
  SibSp: 'Number of Siblings/Spouses Aboard',
  Parch: 'Number of Parents/Children',
  Fare: 'Fare',
  Embarked: 'Port of Embarkation'
};

const LocalResults = ({ resp }) => {
  if (resp === null)
    return (
      <div className='col-12 text-center'>
        <h4>Generating model...</h4>
        <Loader type='TailSpin' color='black' />
      </div>
    );
  
  if (resp.status === 'FAIL')
    return <h4 className='text-danger'>Error: { resp.error }</h4>;
  
  if (resp.status !== 'SUCCESS')
    return <h4 className='text-danger'>Error: Unknown error.</h4>;
  
  let histograms = [], i = 0;

  for (const k in resp.result.plots.histograms) {
    histograms.push(
      <div key={i++} className='col-12 col-md-6 text-center'>
        <img src={`data:image/png;base64,${ resp.result.plots.histograms[k] }`} className='img-fluid' />
        <h4>{ featNames[k] }</h4>
      </div>
    );
  }
  
  let value_counts = []; i = 0;

  for (const k in resp.result.plots.value_counts) {
    value_counts.push(
      <div key={i++} className='col-12 col-md-6 text-center'>
        <img src={`data:image/png;base64,${ resp.result.plots.value_counts[k] }`} className='img-fluid' />
        <h4>{ featNames[k] }</h4>
      </div>
    );
  }

  let tests = []; i = 0;

  for (let test_i of resp.result.tests) {
    tests.push(
      <div key={i++} className='col-12 col-md-3 mt-2 mb-2'>
        <h4>Test { i + 1 }</h4>
        <h6>Prediction: { test_i[0] ? 'Survives' : "Doesn't survive" }</h6>
        <h6>Actual: { test_i[1] ? 'Survives' : "Doesn't survive" }</h6>
      </div>
    );
  }

  let scores = []; i = 0;

  for (const sctype in resp.result.scores) {
    let sco = [], j = 0;

    for (const scrit in resp.result.scores[sctype]) {
      sco.push(
        <h6 key={j}>{scrit}: {resp.result.scores[sctype][scrit]}</h6>
      );
    }

    scores.push(
      <div key={i++} className='col-12 col-md-6 text-center mt-2 mb-2'>
        <h4>{ sctype }</h4>
        { sco }
      </div>
    );
  }

  return (
    <>
      <div className='col-12 text-center'>
        <h2>Scores</h2>
      </div>
      { scores }
      <div className='col-12 text-center'>
        <h2>Tests</h2>
      </div>
      { tests }
      <div className='col-12 text-center mt-2'>
        <h2>Numeric Features</h2>
      </div>
      { histograms }
      <div className='col-12 text-center'>
        <h2>Scatter plot</h2>
        <img src={`data:image/png;base64,${ resp.result.plots.scatter }`} className='img-fluid' />
      </div>
      <div className='col-12 text-center'>
        <h2>Categorical Features</h2>
      </div>
      { value_counts }
    </>
  );
};

class ModelGen extends Component {
  constructor(props) {
    super(props);

    this.state = {
      resp: null
    };
  }

  render() {
    if (this.state.resp === null)
      generateModel()
        .then(resp => this.setState({ resp: resp.data }))
        .catch(resp => this.setState({
          resp: {
            status: 'FAIL',
            statusCode: 404,
            error: 'Request failed.'
          }
        }));

    return (
      <main className='container-fluid mt-3 mb-4'>
        <div className='row'>
          <h1 className='col-12'>Titanic Survival Prediction</h1>
        </div>
        <div className='row pl-4 pr-4 mt-1'>
          <LocalResults resp={this.state.resp} />
        </div>
      </main>
    );
  }
}

export default ModelGen;