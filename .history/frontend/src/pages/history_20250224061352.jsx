import { Card } from "../components/ui/card"

export default function History() {
  // This is a mock-up of previous generations
  const mockHistory = [
    { id: 1, query: "Show all goals from the last game", result: "3 highlights generated" },
    { id: 2, query: "Compile all saves by our goalkeeper", result: "5 highlights generated" },
    { id: 3, query: "Show team celebrations after scoring", result: "2 highlights generated" },
  ]

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-[#002855] mb-8">Generation History</h1>
        <div className="space-y-4">
          {mockHistory.map((item) => (
            <Card key={item.id} className="p-4">
              <h3 className="font-semibold text-[#002855]">{item.query}</h3>
              <p className="text-gray-600">{item.result}</p>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}

