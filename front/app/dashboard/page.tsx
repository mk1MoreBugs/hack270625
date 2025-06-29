"use client"

import { useAppContext } from "@/contexts/AppContext"
import { projectsData, leadsData } from "@/lib/data"

export default function DashboardPage() {
  const { userRole, setUserRole } = useAppContext()

  const projects = projectsData.slice(0, 2)
  const leads = leadsData

  const buyerLinks = [
    { href: "/dashboard", label: "Панель управления", active: true },
    { href: "/catalog", label: "Каталог" },
  ]

  return null
}
