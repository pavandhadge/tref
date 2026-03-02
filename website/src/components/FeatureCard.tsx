import { Card } from "@/components/ui/card";
import React from "react";

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  command: string;
}

const FeatureCard = ({ icon, title, description, command }: FeatureCardProps) => {
  return (
    <Card className="h-full rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-sky-200 hover:shadow-md">
      <div className="mb-3 inline-flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100 text-sky-700">
        {icon}
      </div>
      <h3 className="text-base font-semibold leading-6 text-slate-900">{title}</h3>
      <p className="mt-2 min-h-[3.6rem] text-sm leading-6 text-slate-600">{description}</p>
      <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-3">
        <div className="mb-1 text-[10px] font-semibold uppercase tracking-wide text-slate-500">Command</div>
        <div className="overflow-x-auto whitespace-nowrap rounded-md border border-slate-800 bg-slate-950 px-2.5 py-2 font-mono text-xs text-slate-100">
          <span className="mr-1 text-emerald-300">$</span>
          {command}
        </div>
      </div>
    </Card>
  );
};

export default FeatureCard;
