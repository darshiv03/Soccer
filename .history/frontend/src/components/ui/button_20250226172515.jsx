import React from "react";
import { cn } from "../../lib/utils";

export const Button = ({ className, children, ...props }) => {
  return (
    <button
      className={cn("px-4 py-2 bg-blue-600 text-white rounded-md", className)}
      {...props}
    >
      {children}
    </button>
  );
};
