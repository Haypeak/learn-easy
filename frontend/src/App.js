import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Context
import { AuthProvider } from './context/AuthContext';

// Pages
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import CourseList from './pages/CourseList';
import CourseDetail from './pages/CourseDetail';
import Profile from './pages/Profile';
import Quiz from './pages/Quiz';

// Components
import PrivateRoute from './components/PrivateRoute';
import Layout from './components/Layout';
import LandingPage from './pages/LandingPage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <ToastContainer position="top-right" autoClose={3000} />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            {/* Public routes */}
            <Route path="/signin" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            
            {/* Protected routes */}
            <Route element={<Layout />}>
              <Route path="/dashboard" element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } />
              <Route path="/courses" element={
                <PrivateRoute>
                  <CourseList />
                </PrivateRoute>
              } />
              <Route path="/course/:courseId" element={
                <PrivateRoute>
                  <CourseDetail />
                </PrivateRoute>
              } />
              <Route path="/quiz/:quizId" element={
                <PrivateRoute>
                  <Quiz />
                </PrivateRoute>
              } />
              <Route path="/profile" element={
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
              } />
              <Route path="/quiz" element={
                <PrivateRoute>
                  <Quiz />
                </PrivateRoute>
              } />
            </Route>
            
            {/* Redirect all other routes to dashboard */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;

// import React from 'react';
// import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import { AuthProvider } from './context/AuthContext';
// import LandingPage from './pages/LandingPage';
// import SignIn from './pages/SignIn';
// import SignUp from './pages/SignUp';
// import ProfileForm from './pages/ProfileForm';
// import Dashboard from './pages/Dashboard';
// import Features from './pages/Features';
// import About from './pages/About';
// import { Navigate } from 'react-router-dom';
// import { useAuth } from './context/AuthContext';



// function App() {
//   function PrivateRoute({ children }) {
//     const { user } = useAuth();
//     return user ? children : <Navigate to="/" />;
//   }

//   return (
//     <AuthProvider>
//       <Router>
//         <Routes>
//           <Route path="/" element={<LandingPage />} />
//           <Route path="/signin" element={<SignIn />} />
//           <Route path="/signup" element={<SignUp />} />
//           <Route path="/profile-setup" element={<ProfileForm />} />
//           <Route
//             path="/dashboard"
//             element={
//               <PrivateRoute>
//                 <Dashboard />
//               </PrivateRoute>
//             }
//           />
//           <Route path="/features" element={<Features />} />
//           <Route path="/about" element={<About />} />
//         </Routes>
//       </Router>
//     </AuthProvider>
//   );
// }

// export default App;