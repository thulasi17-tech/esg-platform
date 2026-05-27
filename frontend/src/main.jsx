import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import './index.css'

import Login from './pages/Login'
import Dashboard from './pages/Dashboard'

const token = localStorage.getItem("token");

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Login />} />

        <Route
          path="/dashboard"
          element={
            token ? <Dashboard /> : <Navigate to="/" />
          }
        />

      </Routes>

    </BrowserRouter>
  </React.StrictMode>,
)