import React from 'react';

const SplashScreen = () => {
  return (
    <div className="fixed inset-0 bg-gradient-to-b from-[#1e3a2f] to-[#2d5a3d] flex flex-col items-center justify-center z-50">
      {/* Logo */}
      <div className="mb-8 animate-pulse">
        <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-yellow-500 shadow-2xl">
          <img 
            src="/logo.jpg" 
            alt="Aslanoğlu Logo" 
            className="w-full h-full object-cover"
          />
        </div>
      </div>
      
      {/* Brand Name */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-yellow-400 mb-2">
          ASLANOĞLU
        </h1>
        <p className="text-xl text-yellow-200">
          Kuyumculuk
        </p>
      </div>
      
      {/* Loading indicator */}
      <div className="mt-12">
        <div className="w-12 h-12 border-4 border-yellow-400 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
  );
};

export default SplashScreen;