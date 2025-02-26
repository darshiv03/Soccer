import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <BrowserRouter>
          <div className="flex-grow">
            <Routes>
              {/* <Route path="/" element={<Homepage />} /> */}
            </Routes>
          </div>
      </BrowserRouter>
    </div>
  );
}

export default App;