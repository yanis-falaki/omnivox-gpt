import React from 'react';

interface HeaderProps {
  title: string;
}

export const Header: React.FC<HeaderProps> = ({ title }) => {
  return (
    <header className='flex items-end justify-center sticky top-0 pt-16 h-14 bg-gradient-to-b from-gray-300 to-transparent text-transparent'>
      <h1 className='font-extrabold text-transparent mb-2 text-5xl bg-clip-text bg-gradient-to-r from-orange-500 to-yellow-400'>{title}</h1>
    </header>
  );
};