"use client";

import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Send, Upload } from "lucide-react";
import axios from "axios";
import { useAuth } from "../contexts/AuthContext";
import VideoLoadingScreen from "../components/VideoLoadingScreen";

// Template preview images
import template1 from "../templates/template1.png";
import template2 from "../templates/template2.png";
import template3 from "../templates/template3.png";
import template4 from "../templates/template4.png";
import template5 from "../templates/template5.png";

// Instagram logo PNG
import instagramIcon from "../templates/instagram.png";

export default function Generator() {
  const [message, setMessage] = useState("");
  const [file, setFile] = useState(null);
  const [generatedVideo, setGeneratedVideo] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState("template1");
  const { user } = useAuth();

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type.startsWith("video/")) {
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
    if (droppedFile && droppedFile.type.startsWith("video/")) {
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
    if (!file || !message.trim()) {
      setError("Please upload a video file and enter a prompt.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setGeneratedVideo(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("prompt", message);
      formData.append("template", selectedTemplate);
      formData.append("negative_prompt", "");
      formData.append("num_inference_steps", "20");
      formData.append("guidance_scale", "7.5");
      formData.append("num_frames", "24");
      formData.append("fps", "24");
      formData.append("seed", Math.floor(Math.random() * 1000000));

      const token = localStorage.getItem("token");
      if (!token) throw new Error("No authentication token found. Please log in.");

      const response = await axios.post("http://127.0.0.1:8000/api/video/generate", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.data?.video_url) {
        setGeneratedVideo(response.data.video_url);
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      const msg = error.response?.data?.detail || error.message || "Failed to generate video.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const templates = [
    { id: "template1", label: "Classic UC Davis", image: template1 },
    { id: "template2", label: "Play of the Week", image: template2 },
    { id: "template3", label: "Senior Spotlight", image: template3 },
    { id: "template4", label: "Player of the Week", image: template4 },
    { id: "template5", label: "Blank Template", image: template5 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-10">
        <h2 className="text-4xl font-extrabold text-[#002855] text-center">Highlight Generator</h2>
        <p className="text-lg font-bold text-[#002855] text-center leading-snug mt-2 mb-10 max-w-2xl mx-auto">
          Upload your game footage, pick a highlight style, and enter a prompt. <br />
          Our AI will generate a shareable soccer highlight in seconds.
        </p>

        <Card className="max-w-3xl mx-auto shadow-xl border-[#002855]">
          <div className="p-6">
            {/* File Upload Section */}
            <div
              className="border-2 border-dashed rounded-xl p-8 text-center"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              {file ? (
                <>
                  <p className="text-green-600 font-medium mb-2">📁 {file.name}</p>
                  <Button variant="outline" onClick={() => setFile(null)} disabled={isLoading}>
                    Remove File
                  </Button>
                </>
              ) : (
                <>
                  <Upload className="w-10 h-10 mx-auto text-[#002855]" />
                  <p className="text-sm text-gray-600 mt-2 mb-4">Drag & drop a video or click below</p>
                  <input type="file" accept="video/*" onChange={handleFileChange} className="hidden" id="video-upload" />
                  <Button onClick={() => document.getElementById("video-upload").click()} disabled={isLoading}>
                    Choose File
                  </Button>
                </>
              )}
            </div>

            {/* Template Selection */}
            <div className="mt-6">
              <label className="block text-sm font-medium text-[#002855] mb-2">Choose Template</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {templates.map((template) => (
                  <div
                    key={template.id}
                    onClick={() => setSelectedTemplate(template.id)}
                    className={`cursor-pointer border-2 rounded-lg overflow-hidden transition hover:shadow-md ${
                      selectedTemplate === template.id ? "border-[#FFBF00] ring-2 ring-[#002855]" : "border-gray-300"
                    }`}
                  >
                    <img src={template.image} alt={template.label} className="w-full h-40 object-contain bg-white" />
                    <div className="text-center p-2 bg-white text-sm font-semibold text-[#002855]">
                      {template.label}
                    </div>
                  </div>
                ))}

                {/* Dummy "Add Your Own Template" */}
                <div
                  onClick={() => alert("Coming soon!")}
                  className="col-span-1 sm:col-span-2 lg:col-span-1 mx-auto cursor-not-allowed border-2 border-dashed rounded-lg overflow-hidden flex items-center justify-center h-40 bg-gray-100 text-[#002855] text-center font-semibold hover:opacity-75 transition"
                >
                  + Add Your Own Template
                </div>
              </div>
            </div>

            {/* Prompt + Submit */}
            <div className="flex justify-center mt-6">
              <div className="flex w-full max-w-2xl gap-2">
                <Input
                  placeholder="Write your caption prompt..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  disabled={isLoading}
                  className="flex-1"
                />
                <Button size="icon" onClick={handleSubmit} disabled={!file || !message || isLoading}>
                  <Send className="w-5 h-5" />
                </Button>
              </div>
            </div>

            {/* Error / Loading / Result */}
            {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
            {isLoading && <VideoLoadingScreen />}

            {generatedVideo && !isLoading && (
              <div className="mt-6 flex flex-col items-center gap-4">
                <video controls className="w-full rounded-lg">
                  <source src={generatedVideo} type="video/mp4" />
                </video>

                {/* Download + Instagram buttons */}
                <div className="flex items-center gap-4 mt-2">
                  <a
                    href={generatedVideo}
                    download
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-5 py-2 bg-[#FFBF00] text-[#002855] font-semibold rounded hover:bg-[#FFD700] transition"
                  >
                    Download
                  </a>

                  <a
                    href="https://www.instagram.com/"
                    download
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center w-10 h-10"
                    aria-label="Download for Instagram"
                  >
                    <img src={instagramIcon} alt="Instagram" className="w-11 h-11" />
                  </a>
                </div>

                <p className="text-sm text-gray-600 text-center max-w-sm">
                  Once downloaded, open Instagram and upload your video as a Reel or Story.
                </p>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
