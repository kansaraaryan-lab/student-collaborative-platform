import React, {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";
import api from "../api/api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("campus_user");
    return stored ? JSON.parse(stored) : null;
  });

  const login = useCallback ( async (credential) => {
    try {
      const response = await api.post("/auth/google", {
        credential,
      });

      const student = response.data.student;

      const authenticatedUser = {
        id: student.id,
        name: student.name,
        email: student.college_email,
        roomId: student.room_id,
        avatar: student.name?.charAt(0)?.toUpperCase() || "S",
      };

      localStorage.setItem(
        "campus_user",
        JSON.stringify(authenticatedUser)
      );

      setUser(authenticatedUser);

      return {
        success: true,
        user: authenticatedUser,
      };
    } catch (error) {
      console.error("Google login failed:", error);

      const message =
        error.response?.data?.detail ||
        "Google login failed. Please try again.";

      return {
        success: false,
        error: message,
      };
    }
  } , []);

  const logout = () => {
    localStorage.removeItem("campus_user");
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      login,
      logout,
      isAuthenticated: Boolean(user),
    }),
    [user]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
} 

export function useAuth() {
  return useContext(AuthContext);
}