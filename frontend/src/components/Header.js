import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Globe } from 'lucide-react';

const Header = () => {
  const { language, toggleLanguage, t } = useLanguage();

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center">
            <span className="text-white font-bold text-sm">BA</span>
          </div>
          <h1 className="text-lg font-bold">
            <span className="text-yellow-600">BERKAY</span>
            <span className="text-yellow-500">ALTIN</span>
          </h1>
        </div>
        <button
          onClick={toggleLanguage}
          className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
        >
          <Globe size={16} />
          <span className="text-sm font-semibold">{language.toUpperCase()}</span>
        </button>
      </div>
    </header>
  );
};

export default Header;