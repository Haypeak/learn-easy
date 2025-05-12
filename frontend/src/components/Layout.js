import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Home, BookOpen, User, LogOut, ClipboardList } from 'lucide-react';
import Header from './Header';

const Layout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/signin');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar
      <aside className="w-64 bg-white shadow-md">
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-center h-20 border-b bg-gray-100">
            <h1 className="text-2xl font-bold text-gray-800">Learn Easy</h1>
          </div>
          <nav className="flex-1 px-6 py-8 space-y-4">
            <Link
              to="/"
              className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-gray-200 transition"
            >
              <Home className="w-5 h-5 mr-3 text-gray-500" />
              <span className="font-medium">Dashboard</span>
            </Link>
            <Link
              to="/courses"
              className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-gray-200 transition"
            >
              <BookOpen className="w-5 h-5 mr-3 text-gray-500" />
              <span className="font-medium">Courses</span>
            </Link>
            <Link
              to="/profile"
              className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-gray-200 transition"
            >
              <User className="w-5 h-5 mr-3 text-gray-500" />
              <span className="font-medium">Profile</span>
            </Link>
            <Link
              to="/quiz"
              className="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-gray-200 transition"
            >
              <ClipboardList className="w-5 h-5 mr-3 text-gray-500" />
              <span className="font-medium">Quiz</span>
            </Link>
          </nav>
          <div className="p-6 border-t bg-gray-100">
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-4 py-3 text-gray-700 rounded-lg hover:bg-gray-200 transition"
            >
              <LogOut className="w-5 h-5 mr-3 text-gray-500" />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </aside> */}
      <Header />
      {/* Main content */}
      <div className="flex-1 overflow-auto">
        <header className="bg-white shadow-sm">
          <div className="px-8 py-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold text-gray-800">
                Welcome, {user?.name || 'Guest'}
              </h2>
            </div>
          </div>
        </header>

        <main className="p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
