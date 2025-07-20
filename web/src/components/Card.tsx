import React from 'react'

interface CardProps {
  title: string
  description: string
}

const Card: React.FC<CardProps> = ({ title, description }) => {
  return (
    <div className="rounded-lg bg-white p-6 shadow-md transition-all hover:shadow-lg dark:bg-gray-800">
      <h2 className="mb-2 text-xl font-bold text-gray-800 dark:text-white">
        {title}
      </h2>
      <p className="text-gray-600 dark:text-gray-300">{description}</p>
      <button className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-white transition-colors hover:bg-blue-600">
        Learn More
      </button>
    </div>
  )
}

export default Card
