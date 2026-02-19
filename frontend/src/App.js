import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import { LanguageProvider } from './context/LanguageContext';
import Header from './components/Header';
import BottomNav from './components/BottomNav';
import HomePage from './components/HomePage';
import ConverterPage from './components/ConverterPage';
import SplashScreen from './components/SplashScreen';
import { Toaster } from './components/ui/toaster';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';

const MobileApp = () => {
  return (
    <div className="App min-h-screen bg-gray-50 pb-20">
      <Header />
      <main className="max-w-[480px] mx-auto">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/converter" element={<ConverterPage />} />
        </Routes>
      </main>
      <BottomNav />
      <Toaster />
    </div>
  );
};

// Auth Guard Component
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <AdminLogin />;
  }
  return children;
};

function App() {
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    // Show splash screen for 2 seconds
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 2000);
    
    return () => clearTimeout(timer);
  }, []);

  if (showSplash) {
    return <SplashScreen />;
  }

  return (
    <LanguageProvider>
      <Router>
        <Routes>
          <Route path="/adminyonetim_log_tr" element={<AdminLogin />} />
          <Route 
            path="/admin/dashboard" 
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            } 
          />
          <Route path="/*" element={<MobileApp />} />
        </Routes>
      </Router>
    </LanguageProvider>
  );
}

export default App;
