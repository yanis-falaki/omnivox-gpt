import React from 'react'
import HumanMessage from './HumanMessage'
import AIMessage from './AIMessage'

const Chatbox: React.FC = () => {
  return (
    <section className='flex-grow flex flex-col px-20 overflow-y-scroll'>
        <HumanMessage message="What is your name?"/>
        <AIMessage message="As an AI language model I don't have a name"/>
        <HumanMessage message="What is my grade in linear algebra"/>
        <AIMessage message="As an AI language model I don't have a name"/>
        <HumanMessage message="Can you download my assignment 3 from my calculus class?"/>
        <div className='mb-72'></div>
    </section>
  )
}

export default Chatbox