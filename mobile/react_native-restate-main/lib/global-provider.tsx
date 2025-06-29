import React, { createContext, useContext, ReactNode, useState, useEffect } from "react";
import type { User } from "./types";

interface GlobalContextType {
  isLogged: boolean;
  user: User | null;
  loading: boolean;
  login: () => void;
  logout: () => void;
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

interface GlobalProviderProps {
  children: ReactNode;
}

export const GlobalProvider = ({ children }: GlobalProviderProps) => {
  const [isLogged, setIsLogged] = useState(false);
  const [loading, setLoading] = useState(true);
  
  // Мок пользователя
  const mockUser: User = {
    id: "user-1",
    name: "Анна Иванова",
    email: "anna.ivanova@example.com",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b332b8d4?w=150&h=150&fit=crop&crop=face",
  };

  useEffect(() => {
    // Имитируем проверку авторизации при запуске
    const checkAuth = async () => {
      try {
        // Имитируем задержку
        await new Promise(resolve => setTimeout(resolve, 1000));
        // По умолчанию пользователь не авторизован
        setIsLogged(false);
      } catch (error) {
        console.error("Ошибка проверки авторизации:", error);
        setIsLogged(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogin = () => {
    setIsLogged(true);
  };

  const handleLogout = () => {
    setIsLogged(false);
  };

  return (
    <GlobalContext.Provider
      value={{
        isLogged,
        user: isLogged ? mockUser : null,
        loading,
        login: handleLogin,
        logout: handleLogout,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = (): GlobalContextType => {
  const context = useContext(GlobalContext);
  if (!context)
    throw new Error("useGlobalContext must be used within a GlobalProvider");

  return context;
};

export default GlobalProvider;
