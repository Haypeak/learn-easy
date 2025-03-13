import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import LandingPage from './pages/LandingPage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import ProfileForm from './pages/ProfileForm';
import Dashboard from './pages/Dashboard';
import Features from './pages/Features';
import About from './pages/About';
import { Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';



function App() {
  function PrivateRoute({ children }) {
    const { user } = useAuth();
    return user ? children : <Navigate to="/" />;
  }

  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/profile-setup" element={<ProfileForm />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route path="/features" element={<Features />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;