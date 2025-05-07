import { Link } from "react-router-dom"
import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../contexts/AuthContext';
import { Button } from "./ui/button";

const Navbar = () => {
  const { user, login, logout } = useAuth();

  const handleGoogleSuccess = async (credentialResponse) => {
    await login(credentialResponse.credential);
  };

  return (
    <nav className="bg-[#002855] text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">
          UCClip
        </Link>
        <div className="space-x-4 flex items-center">
          {user && (
            <Link to="/generator" className="hover:text-[#FFBF00]">
              Generator
            </Link>
          )}
          {/* <Link to="/history" className="hover:text-[#FFBF00]">
            History
          </Link> */}
          {user ? (
            <div className="flex items-center space-x-4">
              <span className="text-sm">{user.name}</span>
              <Button 
                onClick={logout}
                className="bg-[#FFBF00] text-[#002855] hover:bg-[#FFD700]"
              >
                Log Out
              </Button>
            </div>
          ) : (
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => {
                console.log('Login Failed');
              }}
            />
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar

