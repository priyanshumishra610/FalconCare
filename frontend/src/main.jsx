import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

// Lazy-load new pages to keep initial bundle small
const Blog = React.lazy(() => import('./pages/Blog.jsx'))
const BlogPost = React.lazy(() => import('./pages/BlogPost.jsx'))
const FAQ = React.lazy(() => import('./pages/FAQ.jsx'))
const Forum = React.lazy(() => import('./pages/Forum.jsx'))
const Profile = React.lazy(() => import('./pages/Profile.jsx'))
const Quiz = React.lazy(() => import('./pages/Quiz.jsx'))
const Alerts = React.lazy(() => import('./pages/Alerts.jsx'))
const Hospitals = React.lazy(() => import('./pages/Hospitals.jsx'))
const Tips = React.lazy(() => import('./pages/Tips.jsx'))
const Diary = React.lazy(() => import('./pages/Diary.jsx'))
const WomenChild = React.lazy(() => import('./pages/WomenChild.jsx'))
const MentalHealth = React.lazy(() => import('./pages/MentalHealth.jsx'))

const router = createBrowserRouter([
  { path: '/', element: <App /> },
  { path: '/blog', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Blog /></React.Suspense> },
  { path: '/blog/:id', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><BlogPost /></React.Suspense> },
  { path: '/faq', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><FAQ /></React.Suspense> },
  { path: '/forum', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Forum /></React.Suspense> },
  { path: '/profile', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Profile /></React.Suspense> },
  { path: '/quiz', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Quiz /></React.Suspense> },
  { path: '/alerts', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Alerts /></React.Suspense> },
  { path: '/hospitals', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Hospitals /></React.Suspense> },
  { path: '/tips', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Tips /></React.Suspense> },
  { path: '/diary', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><Diary /></React.Suspense> },
  { path: '/women-child', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><WomenChild /></React.Suspense> },
  { path: '/mental-health', element: <React.Suspense fallback={<div className="p-8">Loading...</div>}><MentalHealth /></React.Suspense> },
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
