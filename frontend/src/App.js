import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import { LanguageProvider } from './context/LanguageContext';
import Header from './components/Header';
import BottomNav from './components/BottomNav';
import HomePage from './components/HomePage';
import ConverterPage from './components/ConverterPage';
import PortfolioPage from './components/PortfolioPage';
import { Toaster } from './components/ui/toaster';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';

const MobileApp = () => {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="App min-h-screen bg-gray-50 pb-20">
      <Header />
      <main className="max-w-[480px] mx-auto">
        {activeTab === 'home' && <HomePage />}
        {activeTab === 'converter' && <ConverterPage />}
        {activeTab === 'portfolio' && <PortfolioPage />}
      </main>
      <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} />
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
