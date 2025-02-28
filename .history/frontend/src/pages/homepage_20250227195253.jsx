import { Link } from "react-router-dom"
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Upload, Camera, Send } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="relative h-[60vh] bg-[#002855]">
        {/* <img
          src="/images/placeholder-hero.jpg"
          alt="UC Davis Men's Soccer Team"
          className="w-full h-full object-cover opacity-50"
        /> */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-white">
            <h1 className="text-5xl font-bold mb-4">UC Davis Soccer Highlights AI</h1>
            <p className="text-xl mb-8">Transform your game footage into engaging highlights</p>
            <Link to="/generator">
              <Button size="lg" className="bg-[#FFBF00] text-[#002855] hover:bg-[#FFD700]">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-[#002855]">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <Card className="p-6 border-2 border-[#002855]">
            <Upload className="w-12 h-12 text-[#002855] mb-4 mx-auto" />
            <h3 className="text-xl font-semibold mb-2 text-center">Upload Game Footage</h3>
            <p className="text-gray-600 text-center">
              Simply upload your soccer match recordings using mp4 format
            </p>
          </Card>
          <Card className="p-6 border-2 border-[#002855]">
            <Camera className="w-12 h-12 text-[#002855] mb-4 mx-auto" />
            <h3 className="text-xl font-semibold mb-2 text-center">AI Processing</h3>
            <p className="text-gray-600 text-center">
              Our AI automatically identifies key moments and creates highlight clips
            </p>
          </Card>
          <Card className="p-6 border-2 border-[#002855]">
            <Send className="w-12 h-12 text-[#002855] mb-4 mx-auto" />
            <h3 className="text-xl font-semibold mb-2 text-center">Share Instantly</h3>
            <p className="text-gray-600 text-center">
              Download and share your highlights across social media platforms
            </p>
          </Card>
        </div>
      </div>

      {/* Team Showcase */}
      <div className="bg-gray-100 py-16">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-[#002855]">UC Davis Men's Soccer Team</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="relative h-64">
                <img
                  src={`/images/player-${i}.jpg`}
                  alt={`UC Davis Soccer Player ${i}`}
                  className="w-full h-full object-cover rounded-lg"
                />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-[#002855] text-white py-16">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Create Amazing Highlights?</h2>
          <p className="mb-8">Join MediaIt and take your UC Davis soccer content to the next level</p>
          <Link to="/generator">
            <Button size="lg" className="bg-[#FFBF00] text-[#002855] hover:bg-[#FFD700]">
              Start Generating Highlights
            </Button>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-200 py-8">
        <div className="container mx-auto text-center">
          <img src="/images/uc-davis-athletics-logo.png" alt="UC Davis Athletics" className="mx-auto mb-4 h-16" />
          <p className="text-sm text-gray-600">
            © 2025 MediaIt - Official highlight generation tool for UC Davis Men's Soccer by Aggie Sports Analytics
          </p>
        </div>
      </footer>
    </div>
  )
}

