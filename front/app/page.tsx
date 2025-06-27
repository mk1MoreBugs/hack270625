"use client"

import { useState } from "react"
import { Search, MapPin, Star, Calendar, Home, Users, TrendingUp, Bot, Phone, Mail } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import Link from "next/link"
import Image from "next/image"

export default function HomePage() {
  const [priceRange, setPriceRange] = useState([2000000, 15000000])
  const [selectedRegion, setSelectedRegion] = useState("")
  const [searchQuery, setSearchQuery] = useState("")

  const featuredProjects = [
    {
      id: 1,
      name: "ЖК Северная Звезда",
      developer: "СтройИнвест",
      location: "Москва, САО",
      price: "от 8 500 000 ₽",
      completion: "Q4 2025",
      rating: 4.8,
      image: "/placeholder.svg?height=300&width=400",
      discount: "5% скидка",
      class: "Комфорт+",
      apartments: 245,
    },
    {
      id: 2,
      name: "ЖК Зеленый Квартал",
      developer: "ЭкоСтрой",
      location: "СПб, Приморский р-н",
      price: "от 6 200 000 ₽",
      completion: "Q2 2026",
      rating: 4.9,
      image: "/placeholder.svg?height=300&width=400",
      discount: "3% скидка",
      class: "Бизнес",
      apartments: 180,
    },
    {
      id: 3,
      name: "ЖК Солнечный Берег",
      developer: "МегаДевелопмент",
      location: "Краснодар, Центр",
      price: "от 4 800 000 ₽",
      completion: "Q1 2025",
      rating: 4.7,
      image: "/placeholder.svg?height=300&width=400",
      discount: "7% скидка",
      class: "Комфорт",
      apartments: 320,
    },
  ]

  const stats = [
    { label: "Проверенных застройщиков", value: "150+", icon: Home },
    { label: "Активных проектов", value: "500+", icon: TrendingUp },
    { label: "Довольных покупателей", value: "12 000+", icon: Users },
    { label: "Средняя экономия", value: "8%", icon: Star },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Home className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Недвижимость 4.0</span>
            </div>

            <nav className="hidden md:flex items-center space-x-8">
              <Link href="#" className="text-gray-700 hover:text-blue-600 font-medium">
                Каталог
              </Link>
              <Link href="#" className="text-gray-700 hover:text-blue-600 font-medium">
                Карта
              </Link>
              <Link href="#" className="text-gray-700 hover:text-blue-600 font-medium">
                Застройщикам
              </Link>
              <Link href="#" className="text-gray-700 hover:text-blue-600 font-medium">
                О нас
              </Link>
            </nav>

            <div className="flex items-center space-x-4">
              <Dialog>
                <DialogTrigger asChild>
                  <Button variant="outline" size="sm" className="hidden sm:flex bg-transparent">
                    <Bot className="w-4 h-4 mr-2" />
                    ИИ-подбор
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-md">
                  <DialogHeader>
                    <DialogTitle>ИИ-помощник по подбору жилья</DialogTitle>
                    <DialogDescription>
                      Расскажите о ваших предпочтениях, и я подберу идеальные варианты
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-start space-x-3">
                        <Avatar className="w-8 h-8">
                          <AvatarFallback className="bg-blue-100 text-blue-600">ИИ</AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <p className="text-sm text-gray-700">
                            Привет! Я помогу найти идеальную квартиру. Какой у вас бюджет и в каком районе ищете?
                          </p>
                        </div>
                      </div>
                    </div>
                    <Input placeholder="Напишите ваш запрос..." />
                    <Button className="w-full">Начать подбор</Button>
                  </div>
                </DialogContent>
              </Dialog>

              <Button>Войти</Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Покупайте квартиры
            <span className="text-blue-600 block">напрямую от застройщиков</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Без посредников, с гарантиями и лучшими ценами. Более 500 проектов от проверенных застройщиков по всей
            России.
          </p>

          {/* Search Bar */}
          <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-6 mb-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2">
                <Input
                  placeholder="Поиск по городу, району или ЖК..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="h-12"
                />
              </div>
              <Select value={selectedRegion} onValueChange={setSelectedRegion}>
                <SelectTrigger className="h-12">
                  <SelectValue placeholder="Регион" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="moscow">Москва</SelectItem>
                  <SelectItem value="spb">Санкт-Петербург</SelectItem>
                  <SelectItem value="krasnodar">Краснодар</SelectItem>
                  <SelectItem value="ekaterinburg">Екатеринбург</SelectItem>
                </SelectContent>
              </Select>
              <Button size="lg" className="h-12">
                <Search className="w-5 h-5 mr-2" />
                Найти
              </Button>
            </div>

            {/* Advanced Filters */}
            <div className="mt-6 pt-6 border-t">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Цена: {priceRange[0].toLocaleString()} - {priceRange[1].toLocaleString()} ₽
                  </label>
                  <Slider
                    value={priceRange}
                    onValueChange={setPriceRange}
                    max={20000000}
                    min={1000000}
                    step={100000}
                    className="w-full"
                  />
                </div>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Класс жилья" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="economy">Эконом</SelectItem>
                    <SelectItem value="comfort">Комфорт</SelectItem>
                    <SelectItem value="comfort-plus">Комфорт+</SelectItem>
                    <SelectItem value="business">Бизнес</SelectItem>
                    <SelectItem value="premium">Премиум</SelectItem>
                  </SelectContent>
                </Select>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Срок сдачи" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2024">2024</SelectItem>
                    <SelectItem value="2025">2025</SelectItem>
                    <SelectItem value="2026">2026</SelectItem>
                    <SelectItem value="2027">2027+</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <stat.icon className="w-8 h-8 text-blue-600" />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">{stat.value}</div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Projects */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Рекомендуемые проекты</h2>
              <p className="text-gray-600">Лучшие предложения с эксклюзивными скидками</p>
            </div>
            <Button variant="outline">Смотреть все</Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredProjects.map((project) => (
              <Card key={project.id} className="overflow-hidden hover:shadow-xl transition-shadow">
                <div className="relative">
                  <Image
                    src={project.image || "/placeholder.svg"}
                    alt={project.name}
                    width={400}
                    height={300}
                    className="w-full h-48 object-cover"
                  />
                  <Badge className="absolute top-4 left-4 bg-red-500 hover:bg-red-600">{project.discount}</Badge>
                  <Badge variant="secondary" className="absolute top-4 right-4">
                    {project.class}
                  </Badge>
                </div>

                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg mb-1">{project.name}</CardTitle>
                      <CardDescription className="flex items-center">
                        <MapPin className="w-4 h-4 mr-1" />
                        {project.location}
                      </CardDescription>
                    </div>
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                      <span className="text-sm font-medium">{project.rating}</span>
                    </div>
                  </div>
                </CardHeader>

                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Застройщик:</span>
                      <span className="font-medium">{project.developer}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Квартир:</span>
                      <span className="font-medium">{project.apartments}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Сдача:</span>
                      <span className="font-medium flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {project.completion}
                      </span>
                    </div>
                    <div className="pt-3 border-t">
                      <div className="flex justify-between items-center mb-4">
                        <span className="text-2xl font-bold text-blue-600">{project.price}</span>
                      </div>
                      <div className="flex space-x-2">
                        <Button className="flex-1">Подробнее</Button>
                        <Button variant="outline" size="icon">
                          <Phone className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive Map Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Интерактивная карта новостроек</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Найдите идеальное расположение для вашего будущего дома. Все проекты на одной карте с подробной
              информацией.
            </p>
          </div>

          <div className="bg-gray-200 rounded-2xl h-96 flex items-center justify-center">
            <div className="text-center">
              <MapPin className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">Интерактивная карта загружается...</p>
              <Button>Открыть полную карту</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16 px-4 bg-blue-600 text-white">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Почему выбирают нас?</h2>
            <p className="text-blue-100 max-w-2xl mx-auto">
              Мы революционизируем рынок недвижимости, делая покупку квартир простой, прозрачной и выгодной
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Home className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Прямые продажи</h3>
              <p className="text-blue-100">Без посредников и лишних комиссий</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Проверенные застройщики</h3>
              <p className="text-blue-100">Только надежные компании с гарантиями</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Лучшие цены</h3>
              <p className="text-blue-100">Динамическое ценообразование и скидки</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Bot className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">ИИ-подбор</h3>
              <p className="text-blue-100">Умный помощник найдет идеальный вариант</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <Home className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">Недвижимость 4.0</span>
              </div>
              <p className="text-gray-400 mb-4">Платформа прямых продаж недвижимости от застройщиков</p>
              <div className="flex space-x-4">
                <Button variant="outline" size="icon">
                  <Phone className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="icon">
                  <Mail className="w-4 h-4" />
                </Button>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Покупателям</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white">
                    Каталог проектов
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white">
                    Карта новостроек
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white">
                    ИИ-подбор
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white">
                    Акции и скидки
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold mb-4">Застройщикам</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white">
                    Разместить проект
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white">
                    CRM-система
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white">
                    Аналитика
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
                  <Link href="#" className="hover:text-white">
                    Помощь
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white">
                    Контакты
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white">
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
            <p>&copy; 2024 Недвижимость 4.0. Все права защищены.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
