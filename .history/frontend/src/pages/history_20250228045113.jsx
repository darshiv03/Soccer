"use client";

import { useEffect, useState } from "react";
import { Card } from "../components/ui/card";
import axios from "axios";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Fetch history from the backend
    const fetchHistory = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/history/");
        setHistory(response.data);
      } catch (error) {
        console.error("Error fetching history:", error);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-[#002855] mb-8">Generation History</h1>
        {history.length === 0 ? (
          <p className="text-gray-600 text-center">No videos generated yet.</p>
        ) : (
          <div className="space-y-4">
            {history.map((item, index) => (
              <Card key={index} className="p-4">
                <h3 className="font-semibold text-[#002855]">{item.query}</h3>
                <p className="text-gray-600">Clips generated: {item.num_clips}</p>
                <a 
                  href={item.video_url} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-blue-500 underline"
                >
                  Watch Video
                </a>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
