"use client"

import { useState } from "react"
import { Button } from "../components/ui/button"
import { Card } from "../components/ui/card"
import { Input } from "../components/ui/input"
import { Send, Upload } from "lucide-react"

export default function Generator() {
  const [message, setMessage] = useState("")
  const [file, setFile] = useState(null)

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]
    setFile(selectedFile)
  }

  const handleDrop = (event) => {
    event.preventDefault()
    const droppedFile = event.dataTransfer.files[0]
    setFile(droppedFile)
  }

  const handleDragOver = (event) => {
    event.preventDefault()
  }

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
                    <Button onClick={() => document.getElementById("video-upload").click()}>Choose File</Button>
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
              <Button size="icon" className="bg-[#002855] hover:bg-[#003366]" disabled={!file || !message}>
                <Send className="h-4 w-4" />
                <span className="sr-only">Send</span>
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}

