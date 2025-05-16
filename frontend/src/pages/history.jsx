"use client";

import { useEffect, useState } from "react";
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import axios from "axios";
import { useAuth } from "../contexts/AuthContext";

export default function History() {
  const [history, setHistory] = useState([]);
  const [expandedVideo, setExpandedVideo] = useState(null); // Track expanded state
  const { user } = useAuth();

  useEffect(() => {
    // Fetch history from the backend
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get("http://127.0.0.1:8000/api/history/", {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.data && Array.isArray(response.data)) {
          setHistory(response.data);
        } else {
          console.error("Invalid history response:", response.data);
        }
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

                <Button
                  className="mt-2 text-blue-500"
                  onClick={() => setExpandedVideo(expandedVideo === index ? null : index)}
                >
                  {expandedVideo === index ? "Hide Video ▲" : "Show Video ▼"}
                </Button>

                {expandedVideo === index && (
                  <div className="mt-4 max-w-lg mx-auto">
                    <video controls className="w-full h-auto rounded-lg shadow-lg">
                      <source src={item.video_url} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  </div>
                )}
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
