import { Link } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../contexts/AuthContext";
import { Button } from "./ui/button";

const Navbar = () => {
  const { user, login, logout } = useAuth();

  const handleGoogleSuccess = async (credentialResponse) => {
    await login(credentialResponse.credential);
  };

  return (
    <nav className="bg-[#002855] text-white py-4 shadow-md border-b border-[#001f3f]/50">
      <div className="container mx-auto px-4 flex justify-between items-center">
        {/* Branding */}
        <Link
          to="/"
          className="text-2xl font-black tracking-tight flex items-center gap-2 hover:text-[#FFBF00] transition"
        >
          {/* Optional logo/icon on the left */}
          <span className="hidden sm:inline-block">⚽</span>
          UCClip
        </Link>

        {/* Right side */}
        <div className="flex flex-wrap items-center gap-4 sm:gap-6">
          {user && (
            <Link
              to="/generator"
              className="text-base font-medium hover:text-[#FFBF00] transition-colors relative"
            >
              <span className="hover-underline">Generate Now</span>
            </Link>


          )}

          {/* Auth section */}
          {user ? (
            <div className="flex items-center gap-3">
              <span className="text-lg font-medium text-gray-200">{user.name.split(" ")[0]}</span>
              <Button
                onClick={logout}
                className="bg-[#FFBF00] text-[#002855] hover:bg-[#FFD700] font-semibold px-4 py-2"
              >
                Log Out
              </Button>
            </div>
          ) : (
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => console.log("Login Failed")}
            />
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
