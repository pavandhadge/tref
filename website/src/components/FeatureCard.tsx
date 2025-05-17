
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import React from "react";

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  command: string;
}

const FeatureCard = ({ icon, title, description, command }: FeatureCardProps) => {
  return (
    <Card className={cn(
      "border border-slate-200 bg-white/95 backdrop-blur-sm",
      "transition-all duration-300 hover:border-[#8B5CF6] hover:shadow-lg hover:shadow-[#8B5CF6]/10",
      "p-6 rounded-lg"
    )}>
      <div className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] p-3 rounded-lg w-12 h-12 flex items-center justify-center mb-4 text-white shadow-sm">
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-2 text-slate-800">{title}</h3>
      <p className="text-slate-600 mb-4">{description}</p>
      <div className="font-mono bg-slate-100 p-2 rounded text-sm text-slate-800 border border-slate-200">
        <span className="text-[#8B5CF6]">$</span> {command}
      </div>
    </Card>
  );
};

export default FeatureCard;
