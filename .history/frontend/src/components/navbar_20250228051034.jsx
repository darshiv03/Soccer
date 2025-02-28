import { Link } from "react-router-dom"

const Navbar = () => {
  return (
    <nav className="bg-[#002855] text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">
          MediaIt
        </Link>
        <div className="space-x-4">
          <Link to="/generator" className="hover:text-[#FFBF00]">
            Generator
          </Link>
          {/* <Link to="/history" className="hover:text-[#FFBF00]">
            History
          </Link> */}
        </div>
      </div>
    </nav>
  )
}

export default Navbar

