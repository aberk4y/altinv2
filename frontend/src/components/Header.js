import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Globe } from 'lucide-react';

const Header = () => {
  const { language, toggleLanguage, t } = useLanguage();

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-[#1e3a2f] to-[#2d5a3d] shadow-lg">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-yellow-400 shadow-md">
            <img 
              src="/logo.jpg" 
              alt="Aslanoğlu Logo" 
              className="w-full h-full object-cover"
            />
          </div>
          <div className="flex flex-col">
            <h1 className="text-lg font-bold text-yellow-400 leading-tight">
              ASLANOĞLU
            </h1>
            <p className="text-xs text-yellow-200">
              Kuyumculuk
            </p>
          </div>
        </div>
        <button
          onClick={toggleLanguage}
          className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-yellow-400 hover:bg-yellow-500 transition-colors"
        >
          <Globe size={16} className="text-[#1e3a2f]" />
          <span className="text-sm font-semibold text-[#1e3a2f]">{language.toUpperCase()}</span>
        </button>
      </div>
    </header>
  );
};

export default Header;