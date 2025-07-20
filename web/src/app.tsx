import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Card from './components/Card'
import ThemeToggle from './components/ThemeToggle'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100 py-8 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex justify-end pb-4">
          <ThemeToggle />
        </div>
        <div className="flex justify-center space-x-8">
          <a
            href="https://vite.dev"
            target="_blank"
            className="transition-transform hover:scale-110"
          >
            <img src={viteLogo} className="h-24 w-24" alt="Vite logo" />
          </a>
          <a
            href="https://react.dev"
            target="_blank"
            className="transition-transform hover:scale-110"
          >
            <img
              src={reactLogo}
              className="animate-spin-slow h-24 w-24"
              alt="React logo"
            />
          </a>
        </div>

        <h1 className="my-8 text-center text-4xl font-bold text-gray-900 dark:text-white">
          Vite + React + TypeScript + TailwindCSS
        </h1>

        <div className="mb-8 flex justify-center">
          <button
            onClick={() => setCount((count) => count + 1)}
            className="rounded-md bg-indigo-600 px-4 py-2 text-white transition-colors hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-none"
          >
            Count is {count}
          </button>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <Card
            title="Vite"
            description="Next Generation Frontend Tooling. Lightning fast HMR and optimized build."
          />
          <Card
            title="React"
            description="A JavaScript library for building user interfaces with a declarative and component-based approach."
          />
          <Card
            title="TypeScript"
            description="A strongly typed programming language that builds on JavaScript, giving you better tooling."
          />
          <Card
            title="TailwindCSS"
            description="A utility-first CSS framework packed with classes that can be composed to build any design."
          />
          <Card
            title="Prettier"
            description="An opinionated code formatter that enforces a consistent style by parsing your code."
          />
          <Card
            title="ESLint"
            description="A static code analysis tool for identifying problematic patterns in JavaScript code."
          />
        </div>

        <p className="mt-8 text-center text-gray-500 dark:text-gray-400">
          Edit{' '}
          <code className="rounded bg-gray-200 px-1 py-0.5 font-mono text-sm dark:bg-gray-700">
            src/app.tsx
          </code>{' '}
          and save to test HMR
        </p>
      </div>
    </div>
  )
}

export default App
