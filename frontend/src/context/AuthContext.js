import React, { createContext, useContext, useState } from 'react';

// Create a context
const AuthContext = createContext();

// Create a provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Default user state

  const login = (userData) => {
    setUser(userData); // Set user data on login
  };

  const signIn = async (email, password) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Failed to sign in');
      }

      const userData = await response.json();
      login(userData); // Call login to set user data
    } catch (error) {
      console.error('Error signing in:', error);
    }
  };

  const signUp = async (email, password, fullName) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, fullName }),
      });

      if (!response.ok) {
        throw new Error('Failed to sign up');
      }

      const userData = await response.json();
      login(userData); // Call login to set user data
    } catch (error) {
      console.error('Error signing up:', error);
    }
  };

  const logout = () => {
    setUser(null); // Clear user data on logout
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signUp, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = () => {
  return useContext(AuthContext);
};
 