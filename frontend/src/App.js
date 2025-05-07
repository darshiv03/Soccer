import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from "./components/navbar"
import Home from "./pages/homepage"
import Generator from "./pages/generator"
import History from "./pages/history"
import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <Router>
        <AuthProvider>
          <div className="App">
            <Navbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route 
                path="/generator" 
                element={
                  <ProtectedRoute>
                    <Generator />
                  </ProtectedRoute>
                } 
              />
              <Route path="/history" element={<History />} />
            </Routes>
          </div>
        </AuthProvider>
      </Router>
    </GoogleOAuthProvider>
  )
}

export default App

