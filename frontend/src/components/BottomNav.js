import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { Home, RefreshCcw } from 'lucide-react';

const BottomNav = () => {
  const location = useLocation();
  const { language } = useLanguage();

  const navItems = [
    { 
      path: '/', 
      label: language === 'tr' ? 'Ana Sayfa' : 'Home',
      icon: Home
    },
    { 
      path: '/converter', 
      label: language === 'tr' ? 'Çevirici' : 'Converter',
      icon: RefreshCcw
    }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-md border-t border-gray-200/50 shadow-lg z-50">
      <div className="flex justify-around items-center h-20 max-w-md mx-auto px-4">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          const IconComponent = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center justify-center flex-1 h-full transition-all duration-200 rounded-xl ${
                isActive
                  ? 'text-yellow-500 -translate-y-1'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <IconComponent 
                size={26} 
                strokeWidth={isActive ? 2.5 : 2}
                className="mb-1" 
              />
              <span className={`text-xs font-medium ${
                isActive ? 'text-yellow-500' : 'text-gray-500'
              }`}>
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNav;