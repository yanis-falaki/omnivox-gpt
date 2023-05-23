import React from 'react'
import HumanMessage from './HumanMessage'
import AIMessage from './AIMessage'
import { Message } from './ChatContainer';

interface ChatboxProps {
    messages: Message[]
  }

const Chatbox: React.FC<ChatboxProps> = ({ messages }) => {
  return (
    <section className='flex-grow flex flex-col px-20 overflow-y-scroll'>
        {messages.map((message, index) => message.AI 
          ? <AIMessage key={index} message={message.message} />
          : <HumanMessage key={index} message={message.message} />)}
        <div className='mb-72'></div>
    </section>
  )
}

export default Chatbox