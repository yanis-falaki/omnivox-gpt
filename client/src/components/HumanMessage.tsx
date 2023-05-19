import React from 'react'
import defaultAvatar from '../images/default-avatar.png'

interface MessageProps {
    message: string
}

const HumanMessage: React.FC<MessageProps> = (props) => {
  return (
    <div className='ml-auto'>
    <div className='bg-gray-100 px-5 py-3 mt-10 rounded-xl inline'>{props.message}</div>
    <img src={defaultAvatar}
    className='h-16 w-16 inline rounded-full object-cover shadow-lg ml-5'/>
    </div>
  )
}

export default HumanMessage