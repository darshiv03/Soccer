import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Navbar from "./components/navbar"
import Home from "./pages/Home"
import Generator from "./pages/generator"
import History from "./pages/history"

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/generator" element={<Generator />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

