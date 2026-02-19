import React from 'react';
import { useLanguage } from '../context/LanguageContext';

const Header = () => {
  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-[#1e3a2f] to-[#2d5a3d] shadow-lg">
      <div className="flex items-center justify-center px-4 py-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-yellow-400 shadow-md">
            <img 
              src="/logo.jpg" 
              alt="Aslanoğlu Logo" 
              className="w-full h-full object-cover"
            />
          </div>
          <h1 className="text-2xl font-bold text-yellow-400">
            ASLANOĞLU
          </h1>
        </div>
      </div>
    </header>
  );
};

export default Header;