import React from 'react'

interface MessageProps {
  message: string;
}

const AIMessage: React.FC<MessageProps> = (props) => {
  return (
    <div className='mr-auto'> 
    <img src='https://i.pinimg.com/originals/35/9d/1d/359d1d33ca0cca4e58b7a8113c2977c1.jpg'
    className='h-16 w-16 inline rounded-full object-cover shadow-lg mr-5'/>
    <div className=' bg-gray-100 px-5 py-3 mt-10 rounded-xl inline'>
    {props.message}
    </div>
    </div>
  )
}

export default AIMessage