import React from 'react'
import Chatbox from './Chatbox'
import QueryBox from './QueryBox'

const ChatContainer: React.FC = () => {
  return (
    <div className='flex-grow flex flex-col h-screen'>
        <Chatbox/>
        <QueryBox/>
    </div>
  )
}

export default ChatContainer