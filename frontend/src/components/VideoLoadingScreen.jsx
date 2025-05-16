import React from 'react';
import { Loader2 } from 'lucide-react';

const VideoLoadingScreen = () => {
  return (
    <div className="mt-8 relative">
      {/* Background blur effect */}
      <div className="absolute inset-0 bg-white/80 backdrop-blur-sm rounded-lg" />
      
      {/* Loading content */}
      <div className="relative z-10 flex flex-col items-center justify-center p-8">
        {/* Animated circles */}
        <div className="relative w-24 h-24 mb-6">
          <div className="absolute inset-0 border-4 border-[#002855] rounded-full animate-ping opacity-20" />
          <div className="absolute inset-0 border-4 border-[#002855] rounded-full animate-pulse" />
          <div className="absolute inset-0 flex items-center justify-center">
            <Loader2 className="w-12 h-12 text-[#002855] animate-spin" />
          </div>
        </div>

        {/* Loading text with typing animation */}
        <div className="text-center">
          <h3 className="text-xl font-semibold text-[#002855] mb-2">
            Creating Your Highlight
          </h3>
          <p className="text-gray-600 max-w-md">
            We're processing your video with AI to create the perfect highlight clip.
            This may take a few moments...
          </p>
        </div>

        {/* Progress dots */}
        <div className="flex space-x-2 mt-6">
          {[1, 2, 3].map((dot) => (
            <div
              key={dot}
              className="w-2 h-2 bg-[#002855] rounded-full animate-bounce"
              style={{ animationDelay: `${dot * 0.2}s` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default VideoLoadingScreen; 