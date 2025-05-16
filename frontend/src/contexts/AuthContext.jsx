import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => { 
  const [user, setUser] = useState(null) ;
  const [loading, setLoading] = useState(true);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const navigate = useNavigate();

  const handleTokenExpiration = () => {
    // Clear everything
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setShowLoginModal(true);
  };

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          // Set up axios default header
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          // Verify token with backend
          const response = await axios.post('http://127.0.0.1:8000/api/auth/verify', { token });
          if (response.data.valid) {
            setUser(response.data.user);
          } else {
            handleTokenExpiration();
          }
        }
      } catch (error) {
        console.error('Auth initialization failed:', error);
        handleTokenExpiration();
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Add axios interceptor to handle 401/403 responses
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401 || error.response?.status === 403) {
          handleTokenExpiration();
        }
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  const login = async (googleToken) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/google', {
        token: googleToken
      });
      
      const { access_token, user_info } = response.data;
      
      // Store token and set up axios default header
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setUser(user_info);
      setShowLoginModal(false);
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const logout = () => {
    // Clear everything
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setShowLoginModal(false);
    navigate('/');
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>;
  }

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      logout, 
      loading, 
      showLoginModal, 
      setShowLoginModal 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 