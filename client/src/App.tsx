import React, {useState, useEffect} from 'react';
import './App.css';
import Header from './components/Header';

const App: React.FC = () => {
  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/members").then(
      res => res.text()
    ).then(
      data => {
        //setData(data);
        console.log(data);
    })
  }, [])

  return (
    <div className="App">
      <Header title='Omnivox-GPT'/>
    </div>
  );
}

export default App;
