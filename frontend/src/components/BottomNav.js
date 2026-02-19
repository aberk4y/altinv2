import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

const BottomNav = () => {
  const location = useLocation();
  const { language } = useLanguage();

  const navItems = [
    { 
      path: '/', 
      label: language === 'tr' ? 'Ana Sayfa' : 'Home',
      icon: '🏠'
    },
    { 
      path: '/converter', 
      label: language === 'tr' ? 'Çevirici' : 'Converter',
      icon: '🔄'
    },
    { 
      path: '/portfolio', 
      label: language === 'tr' ? 'Portföy' : 'Portfolio',
      icon: '💼'
    }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
      <div className="flex justify-around items-center h-16 max-w-md mx-auto">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
                isActive
                  ? 'text-[#1e3a2f] bg-yellow-50'
                  : 'text-gray-500 hover:text-[#1e3a2f]'
              }`}
            >
              <span className="text-2xl mb-1">{item.icon}</span>
              <span className="text-xs font-medium">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNav;