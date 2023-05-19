import React, { useState, ChangeEvent } from 'react'

const QueryBox: React.FC = () => {

    const [text, setText] = useState('')

    const handleTextChange = (e: ChangeEvent<HTMLInputElement>) => {
        setText(e.target.value);
    }

    const handleSubmit = () => {
        console.log(text);
    }

    return (
        <div className='sticky bottom-0 -my-20 py-12 bg-gradient-to-t from-gray-200  to-transparent'>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={text}
                    onChange={handleTextChange}
                    className="border border-gray-300 px-6 py-2 mx-auto w-1/3 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </form>
        </div>
    )
}

export default QueryBox