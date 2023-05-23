import React, { useState, ChangeEvent } from 'react'
import { Message } from './ChatContainer'
import { v4 } from 'uuid'

interface QueryProps{
    setMessages: React.Dispatch<React.SetStateAction<Message[]>>
}


const QueryBox: React.FC<QueryProps> = ({ setMessages }) => {

    const [text, setText] = useState('')

    const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setText(e.target.value);
    }

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const newMessage: Message = {AI: false, message: text, messageId: v4()}
        setMessages((prev) => [...prev, newMessage])
        setText('')
    }

    return (
        <div className='sticky bottom-0 h-32 bg-gradient-to-t from-gray-200 to-transparent flex flex-col justify-center'>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={text}
                    onChange={handleTextChange}
                    className="border border-gray-300 py-2 mt-8 w-full lg:w-1/2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </form>
        </div>
    )
}

export default QueryBox