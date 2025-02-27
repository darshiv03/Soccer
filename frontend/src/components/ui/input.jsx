import React from "react";
import { cn } from "../../lib/utils";

export const Input = ({ className, ...props }) => {
  return (
    <input
      className={cn(
        "border px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
        className
      )}
      {...props}
    />
  );
};
