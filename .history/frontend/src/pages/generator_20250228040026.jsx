"use client";

import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Send, Upload } from "lucide-react";
import axios from "axios";

export default function Generator() {
  const [message, setMessage] = useState("");
  const [file, setFile] = useState(null);
  const [generatedVideo, setGeneratedVideo] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setFile(event.dataTransfer.files[0]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleSubmit = async () => {
    if (!file || !message) return;
    const formData = new FormData();
    formData.append("video_file", file);
    formData.append("text_string", message);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/generate_video/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (response.data.video_url) {
        // Append a timestamp for cache busting
        const videoUrl = response.data.video_url + `?t=${Date.now()}`;
        console.log("Received video URL:", videoUrl);
        setGeneratedVideo(videoUrl);
      } else {
        console.error("Error generating video", response.data);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };
  

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-[#002855] mb-8">Highlight Generator</h1>
        <Card className="max-w-3xl mx-auto">
          <div className="p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-semibold mb-4 text-[#002855]">Create Highlights</h2>
              <div
                className="border-2 border-dashed border-[#002855] rounded-lg p-8 text-center"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
              >
                {file ? (
                  <div className="text-center">
                    <p className="text-green-600 mb-2">File selected: {file.name}</p>
                    <Button onClick={() => setFile(null)} variant="outline">
                      Remove File
                    </Button>
                  </div>
                ) : (
                  <>
                    <Upload className="w-12 h-12 mx-auto text-[#002855] mb-4" />
                    <p className="text-gray-600 mb-2">Drag and drop your video files here</p>
                    <p className="text-sm text-gray-500 mb-4">or</p>
                    <input
                      type="file"
                      accept="video/*"
                      onChange={handleFileChange}
                      className="hidden"
                      id="video-upload"
                    />
                    <Button onClick={() => document.getElementById("video-upload").click()}>
                      Choose File
                    </Button>
                  </>
                )}
              </div>
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="Type your instructions for the highlight clip..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="flex-1"
              />
              <Button
                size="icon"
                className="bg-[#002855] hover:bg-[#003366]"
                disabled={!file || !message}
                onClick={handleSubmit}
              >
                <Send className="h-4 w-4" />
                <span className="sr-only">Send</span>
              </Button>
            </div>
          </div>
        </Card>

        {generatedVideo && (
          <div className="mt-8 text-center">
            <h2 className="text-xl font-semibold text-[#002855] mb-4">Generated Video</h2>
            <video
              key={generatedVideo}
              crossOrigin="anonymous"
              controls
              preload="auto"
              className="w-full max-w-4xl mx-auto"
              onLoadedData={() => console.log("Video loaded")}
              onError={(e) => console.error("Video error:", e.target.error)}
            >
              <source src={generatedVideo} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        )}

      </div>
    </div>
  );
}
