"use client"

import Link from "next/link"
import { Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { AiAssistantLink } from "@/components/search/AiAssistantLink"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"

export function Header() {
  const pathname = usePathname()
  const isDashboard = pathname.startsWith("/dashboard-") || pathname === "/profile"

  const navLinks = [
    { href: "/", label: "Главная" },
    { href: "/catalog", label: "Каталог" },
    { href: "/map", label: "Карта" },
    { href: "/about", label: "О нас" },
  ]

  if (isDashboard) {
    return null
  }

  return (
    <header className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Home className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">Недвижимость 5.0</span>
          </Link>

          <nav className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "font-medium transition-colors",
                  pathname === link.href ? "text-blue-600" : "text-gray-700 hover:text-blue-600",
                )}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="flex items-center space-x-4">
            <AiAssistantLink />
            <Link href="/login">
              <Button>Войти</Button>
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}
