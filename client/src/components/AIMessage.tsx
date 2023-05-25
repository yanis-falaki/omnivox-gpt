import React from 'react'

interface MessageProps {
  message: string;
}

const AIMessage: React.FC<MessageProps> = (props) => {
  return (
    <div className='mr-auto flex flex-col lg:flex-row lg:items-center mt-10'> 
    <img src='https://i.pinimg.com/originals/35/9d/1d/359d1d33ca0cca4e58b7a8113c2977c1.jpg'
    className='h-16 w-16 inline-block rounded-full object-cover shadow-lg lg:mr-5 mr-auto mb-2 lg:mb-0 '/>
    <div className=' bg-gray-100 px-5 py-3 rounded-xl inline-block max-w-6xl text-left'>
    {props.message}
    </div>
    </div>
  )
}

export default AIMessage