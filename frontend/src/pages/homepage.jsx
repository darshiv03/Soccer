import { Link } from "react-router-dom"
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { Upload, Camera, Send } from "lucide-react"
import { useAuth } from "../contexts/AuthContext";

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-white font-sans">
      {/* Hero Section */}
      <div className="relative h-[60vh]">
        {/* Background Image with Dark Gradient Overlay */}
        <div className="absolute inset-0 bg-black/50 z-10"></div>
        <img
          src="/images/homepage_img.png"
          alt="UC Davis Men's Soccer Team"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 z-20 flex items-center justify-center px-4">
          <div className="text-center text-white">
            <h1 className="text-5xl font-extrabold mb-4">CLIP IT NOW</h1>
            <p className="text-2xl md:text-3xl mb-8 max-w-2xl mx-auto">
              Transform your game footage into engaging content
            </p>
            {user ? (
              <Link to="/generator">
                <Button
                  size="lg"
                  className="bg-[#FFBF00] text-[#002855] hover:scale-105 hover:bg-[#FFD700] transition-transform duration-200 text-xl px-8 py-4 rounded-xl"
                >
                  Get Started →
                </Button>
              </Link>
            ) : (
              <p className="text-lg font-semibold bg-white/30 p-4 rounded-xl inline-block">
                Log in to access the highlight generator
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Divider */}
      <div className="w-full h-12 bg-gradient-to-b from-white to-gray-100" />

      {/* Features Section */}
      <div className="container mx-auto py-16 px-6">
        <h2 className="text-3xl font-bold text-center mb-12 text-[#002855]">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[{
            icon: <Upload className="w-12 h-12 text-[#002855] mb-4 mx-auto" />,
            title: "Upload Game Footage",
            desc: "Simply upload your soccer match recordings using mp4 format"
          }, {
            icon: <Camera className="w-12 h-12 text-[#002855] mb-4 mx-auto" />,
            title: "AI Processing",
            desc: "Our AI automatically identifies key moments and creates highlight clips"
          }, {
            icon: <Send className="w-12 h-12 text-[#002855] mb-4 mx-auto" />,
            title: "Share Instantly",
            desc: "Download and share your highlights across social media platforms"
          }].map((item, idx) => (
            <Card
              key={idx}
              className="p-6 border-2 border-[#002855] hover:shadow-xl transition-all duration-300 rounded-xl"
            >
              {item.icon}
              <h3 className="text-xl font-semibold mb-2 text-center">{item.title}</h3>
              <p className="text-gray-600 text-center">{item.desc}</p>
            </Card>
          ))}
        </div>
      </div>

      {/* Team Showcase Section */}
      <div className="bg-gray-100 py-16 px-6">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-[#002855]">UC Davis Men's Soccer Team</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="relative h-64 group overflow-hidden rounded-xl shadow-md hover:shadow-xl transition-shadow">
                <img
                  src={`/images/player-${i}.png`}
                  alt={`UC Davis Soccer Player ${i}`}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-[#002855] text-white py-20 px-6">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Create Amazing Highlights?</h2>
          <p className="mb-8 text-lg">
            Join UCClip and take your UC Davis soccer content to the next level
          </p>
          {user ? (
            <Link to="/generator">
              <Button size="lg" className="bg-[#FFBF00] text-[#002855] hover:bg-[#FFD700] px-8 py-4 text-lg rounded-xl">
                Start Generating Highlights →
              </Button>
            </Link>
          ) : (
            <p className="text-lg">Log in to get started</p>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-200 py-12 px-6">
        <div className="container mx-auto mb-6">
          <img
            src="/images/davismensteam.jpg"
            alt="UC Davis Athletics"
            className="w-full h-[300px] object-contain rounded-xl shadow"
          />
        </div>
        <div className="container mx-auto text-center">
          <p className="text-sm text-gray-600">
            © 2025 UCClip – Official content generation tool for UC Davis Men's Soccer by Aggie Sports Analytics
          </p>
        </div>
      </footer>
    </div>
  )
}
