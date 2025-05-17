
import React from 'react';

interface TerminalHeaderProps {
  command: string;
  flag?: string;
}

const TerminalHeader = ({ command, flag }: TerminalHeaderProps) => {
  return (
    <div className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] p-3 rounded-t-lg shadow-md mb-6 relative">
      <div className="flex space-x-1 absolute left-3 top-1/2 transform -translate-y-1/2">
        <div className="h-2.5 w-2.5 rounded-full bg-red-500"></div>
        <div className="h-2.5 w-2.5 rounded-full bg-yellow-500"></div>
        <div className="h-2.5 w-2.5 rounded-full bg-green-500"></div>
      </div>
      <h2 className="font-mono font-bold text-xl md:text-2xl text-center text-white">
        <span className="opacity-80">$</span> {command} <span className="opacity-80">{flag}</span>
      </h2>
    </div>
  );
};

export default TerminalHeader;
