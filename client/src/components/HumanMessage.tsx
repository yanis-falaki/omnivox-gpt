import React from 'react'
import defaultAvatar from '../images/default-avatar.png'

interface MessageProps {
    message: string
}

const HumanMessage: React.FC<MessageProps> = (props) => {
  return (
    <div className='ml-auto flex flex-col lg:flex-row lg:items-center mt-10'>
      <div className='bg-gray-100 px-5 py-3 rounded-xl inline-block max-w-6xl text-left ml-auto lg:mb-0 lg:order-1 order-2'>{props.message}</div>
      <img src={defaultAvatar}
      className='h-16 w-16 inline-block rounded-full object-cover shadow-lg ml-auto order-1 mb-2 lg:mb-0 lg:ml-5 lg:order-2 '/>
    </div>
  )
}

export default HumanMessage