import React from 'react'
import HumanMessage from './HumanMessage'
import AIMessage from './AIMessage'
import { Message } from './ChatContainer';

interface ChatboxProps {
    messages: Message[];
    loading: boolean;
  }

const APILoading: React.FC = () => {
  return (
    <div className='flex px-5'>
      <h3 className='text-3xl font-bold text-gray-500'>Loading</h3>
      <div className='bg-orange-600 h-7 w-7 rounded-xl animate-jump ml-4 shadow-3xl'/>
      <div className='bg-orange-400 h-7 w-7 rounded-xl animate-jump-delay-1 ml-2 shadow-3xl'/>
      <div className='bg-yellow-400 h-7 w-7 rounded-xl animate-jump-delay-2 ml-2 shadow-3xl'/>
    </div>
  )
}

const Chatbox: React.FC<ChatboxProps> = ({ messages, loading }) => {
  return (
    <section className='flex-grow flex flex-col px-20 overflow-y-scroll'>
        {messages.map((message, index) => message.AI 
          ? <AIMessage key={index} message={message.message} />
          : <HumanMessage key={index} message={message.message} />)}
        {loading ? <APILoading/> : null}
        <div className='mb-72'></div>
    </section>
  )
}



export default Chatbox