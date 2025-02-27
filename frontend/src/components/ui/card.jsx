import React from "react";
import { cn } from "../../lib/utils";

export const Card = ({ className, children, ...props }) => {
  return (
    <div className={cn("p-4 border rounded-md shadow-md", className)} {...props}>
      {children}
    </div>
  );
};
