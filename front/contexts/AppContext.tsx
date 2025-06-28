"use client"

import { createContext, useState, useContext, type ReactNode, type Dispatch, type SetStateAction } from "react"
import type { UserRole } from "@/lib/types"

interface AppContextType {
  userRole: UserRole
  setUserRole: Dispatch<SetStateAction<UserRole>>
}

const AppContext = createContext<AppContextType | undefined>(undefined)

export function AppProvider({ children }: { children: ReactNode }) {
  const [userRole, setUserRole] = useState<UserRole>("developer")

  return <AppContext.Provider value={{ userRole, setUserRole }}>{children}</AppContext.Provider>
}

export function useAppContext() {
  const context = useContext(AppContext)
  if (context === undefined) {
    throw new Error("useAppContext must be used within an AppProvider")
  }
  return context
}
