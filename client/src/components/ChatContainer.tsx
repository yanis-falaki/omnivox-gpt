import React, { useState } from 'react'
import Chatbox from './Chatbox'
import QueryBox from './QueryBox'
import {v4} from 'uuid';

export interface Message{
  AI: boolean;
  message: string;
  messageId: string;
}

const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false)

  return (
    <div className='flex-grow flex flex-col h-screen'>
        <Chatbox messages={messages} loading={loading}/>
        <QueryBox setMessages={setMessages} setLoading={setLoading} loading={loading}/>
    </div>
  )
}

export default ChatContainer