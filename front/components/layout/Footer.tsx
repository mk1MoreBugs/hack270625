"use client"

import Link from "next/link"
import { Home, Phone, Mail } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useAppContext } from "@/contexts/AppContext"

export function Footer() {
  const { userRole } = useAppContext()
  const isLoggedIn = userRole === "developer" || userRole === "admin"

  return (
    <footer className="bg-gray-900 text-white py-12 px-4">
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Home className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold">Недвижимость 5.0</span>
            </div>
            <p className="text-gray-400 mb-4">Платформа прямых продаж недвижимости от застройщиков</p>
            <div className="flex space-x-4">
              <Button
                variant="outline"
                size="icon"
                asChild
                className="group bg-transparent border-gray-600 hover:border-blue-500"
              >
                <a href="tel:+70000000000">
                  <Phone className="h-4 w-4 text-gray-300 transition-colors group-hover:text-blue-500" />
                </a>
              </Button>
              <Button
                variant="outline"
                size="icon"
                asChild
                className="group bg-transparent border-gray-600 hover:border-blue-500"
              >
                <a href="mailto:support@realestate5.com">
                  <Mail className="h-4 w-4 text-gray-300 transition-colors group-hover:text-blue-500" />
                </a>
              </Button>
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Покупателям</h3>
            <ul className="space-y-2 text-gray-400">
              <li>
                <Link href="/catalog" className="hover:text-white">
                  Каталог проектов
                </Link>
              </li>
              <li>
                <Link href="/map" className="hover:text-white">
                  Карта новостроек
                </Link>
              </li>
              <li>
                <Link href="/ai-assistant" className="hover:text-white">
                  ИИ-подбор
                </Link>
              </li>
              <li>
                <Link href="/catalog?promo=true" className="hover:text-white">
                  Акции и скидки
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Застройщикам</h3>
            <ul className="space-y-2 text-gray-400">
              <li>
                <Link href={isLoggedIn ? "/dashboard-developer" : "/login"} className="hover:text-white">
                  CRM-система
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-white">
                  Тарифы
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Поддержка</h3>
            <ul className="space-y-2 text-gray-400">
              <li>
                <Link href="/about" className="hover:text-white">
                  Помощь
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-white">
                  Контакты
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-white">
                  О платформе
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-white">
                  Документы
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 Недвижимость 5.0. Все права защищены.</p>
        </div>
      </div>
    </footer>
  )
}
