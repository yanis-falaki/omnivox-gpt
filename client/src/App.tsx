import React, {useState, useEffect} from 'react';
import './App.css';
import { Header } from './components/Header';
import ChatContainer from './components/ChatContainer';

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
    <div className="App flex flex-col">
      <Header title='Omnivox-GPT'/>
      <ChatContainer/>
    </div>
  );
}

export default App;
