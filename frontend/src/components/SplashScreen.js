import React from 'react';

const SplashScreen = () => {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-gray-50 via-white to-yellow-50 flex flex-col items-center justify-center z-50">
      {/* Logo */}
      <div className="mb-6 animate-pulse">
        <div className="w-32 h-32 rounded-full overflow-hidden ring-4 ring-yellow-400 shadow-2xl">
          <img 
            src="/logo.jpg" 
            alt="Aslanoğlu Logo" 
            className="w-full h-full object-cover"
          />
        </div>
      </div>
      
      {/* Brand Name */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-2 tracking-wide">
          ASLANOĞLU
        </h1>
        <p className="text-lg text-gray-600 font-medium">
          Kuyumculuk
        </p>
      </div>
      
      {/* Loading indicator */}
      <div className="mt-12">
        <div className="flex gap-2">
          <div className="w-3 h-3 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '0s'}}></div>
          <div className="w-3 h-3 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
          <div className="w-3 h-3 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;