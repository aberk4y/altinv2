import React from 'react';

const Header = () => {
  return (
    <header className="sticky top-0 z-50 bg-gradient-to-b from-white to-gray-50 shadow-sm backdrop-blur-md bg-opacity-95">
      <div className="flex items-center justify-center px-4 py-4">
        <div className="flex flex-col items-center gap-2">
          <div className="w-14 h-14 rounded-full overflow-hidden ring-2 ring-yellow-400 shadow-lg">
            <img 
              src="/logo.jpg" 
              alt="Aslanoğlu Logo" 
              className="w-full h-full object-cover"
            />
          </div>
          <div className="text-center">
            <h1 className="text-xl font-semibold text-gray-800 tracking-wide">
              ASLANOĞLU
            </h1>
            <p className="text-xs text-gray-500 font-medium">
              Kuyumculuk
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;