"use client";

import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Send, Upload, Loader2 } from "lucide-react";
import axios from "axios";
import { useAuth } from "../contexts/AuthContext";

export default function Generator() {
  const [message, setMessage] = useState("");
  const [file, setFile] = useState(null);
  const [generatedVideo, setGeneratedVideo] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type.startsWith('video/')) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("Please select a valid video file");
      setFile(null);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith('video/')) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError("Please drop a valid video file");
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a video file");
      return;
    }

    if (!message.trim()) {
      setError("Please enter a prompt");
      return;
    }

    setIsLoading(true);
    setError(null);
    setGeneratedVideo(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("prompt", message);
      formData.append("negative_prompt", "");
      formData.append("num_inference_steps", "20");
      formData.append("guidance_scale", "7.5");
      formData.append("num_frames", "24");
      formData.append("fps", "24");
      formData.append("seed", Math.floor(Math.random() * 1000000));

      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found. Please log in.');
      }

      const response = await axios.post(
        "http://127.0.0.1:8000/api/video/generate",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "Authorization": `Bearer ${token}`
          },
        }
      );

      if (response.data && response.data.video_url) {
        setGeneratedVideo(response.data.video_url);
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      console.error("Error generating video:", error);
      if (error.response?.status === 403) {
        setError("Authentication failed. Please log in again.");
      } else if (error.response?.status === 401) {
        setError("Your session has expired. Please log in again.");
      } else if (error.response?.data?.detail) {
        setError(error.response.data.detail);
      } else {
        setError(error.message || "Failed to generate video. Please try again.");
      }
    } finally {
      setIsLoading(false);
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
                className={`border-2 border-dashed rounded-lg p-8 text-center ${
                  error && !file ? 'border-red-500' : 'border-[#002855]'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
              >
                {file ? (
                  <div className="text-center">
                    <p className="text-green-600 mb-2">File selected: {file.name}</p>
                    <Button onClick={() => setFile(null)} variant="outline" disabled={isLoading}>
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
                      disabled={isLoading}
                    />
                    <Button onClick={() => document.getElementById("video-upload").click()} disabled={isLoading}>
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
                disabled={isLoading}
              />
              <Button
                size="icon"
                className="bg-[#002855] hover:bg-[#003366]"
                disabled={!file || !message || isLoading}
                onClick={handleSubmit}
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
                <span className="sr-only">Send</span>
              </Button>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600">{error}</p>
              </div>
            )}

            {isLoading && (
              <div className="mt-8 text-center">
                <Loader2 className="h-8 w-8 animate-spin mx-auto text-[#002855]" />
                <p className="mt-2 text-gray-600">Generating your highlight video...</p>
              </div>
            )}

            {generatedVideo && !isLoading && (
              <div className="mt-8">
                <h3 className="text-xl font-semibold text-[#002855] mb-4">Generated Video</h3>
                <video controls className="w-full rounded-lg shadow-lg">
                  <source src={generatedVideo} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
