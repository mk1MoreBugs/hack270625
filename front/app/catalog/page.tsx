"use client"

import { useState } from "react"
import { Filter, MapPin, Star, Calendar, Home, Eye, Heart, Share2, ArrowUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Checkbox } from "@/components/ui/checkbox"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import Image from "next/image"
import Link from "next/link"

export default function CatalogPage() {
  const [priceRange, setPriceRange] = useState([2000000, 15000000])
  const [sortBy, setSortBy] = useState("price-asc")
  const [viewMode, setViewMode] = useState("grid")

  const projects = [
    {
      id: 1,
      name: "ЖК Северная Звезда",
      developer: "СтройИнвест",
      location: "Москва, САО",
      price: "от 8 500 000 ₽",
      pricePerSqm: "от 185 000 ₽/м²",
      completion: "Q4 2025",
      rating: 4.8,
      reviews: 124,
      image: "/placeholder.svg?height=300&width=400",
      gallery: ["/placeholder.svg?height=200&width=300", "/placeholder.svg?height=200&width=300"],
      discount: "5% скидка",
      class: "Комфорт+",
      apartments: 245,
      available: 89,
      features: ["Паркинг", "Детская площадка", "Фитнес-зал", "Консьерж"],
      metro: "Алтуфьево, 15 мин",
      floors: "25 этажей",
    },
    {
      id: 2,
      name: "ЖК Зеленый Квартал",
      developer: "ЭкоСтрой",
      location: "СПб, Приморский р-н",
      price: "от 6 200 000 ₽",
      pricePerSqm: "от 165 000 ₽/м²",
      completion: "Q2 2026",
      rating: 4.9,
      reviews: 89,
      image: "/placeholder.svg?height=300&width=400",
      gallery: ["/placeholder.svg?height=200&width=300", "/placeholder.svg?height=200&width=300"],
      discount: "3% скидка",
      class: "Бизнес",
      apartments: 180,
      available: 45,
      features: ["Паркинг", "Спа-центр", "Кафе", "Охрана"],
      metro: "Комендантский пр., 8 мин",
      floors: "18 этажей",
    },
    {
      id: 3,
      name: "ЖК Солнечный Берег",
      developer: "МегаДевелопмент",
      location: "Краснодар, Центр",
      price: "от 4 800 000 ₽",
      pricePerSqm: "от 145 000 ₽/м²",
      completion: "Q1 2025",
      rating: 4.7,
      reviews: 156,
      image: "/placeholder.svg?height=300&width=400",
      gallery: ["/placeholder.svg?height=200&width=300", "/placeholder.svg?height=200&width=300"],
      discount: "7% скидка",
      class: "Комфорт",
      apartments: 320,
      available: 127,
      features: ["Паркинг", "Детский сад", "Магазины", "Парк"],
      metro: "Центр города, 5 мин",
      floors: "16 этажей",
    },
    {
      id: 4,
      name: "ЖК Премиум Резиденс",
      developer: "Элит Строй",
      location: "Москва, ЦАО",
      price: "от 25 000 000 ₽",
      pricePerSqm: "от 450 000 ₽/м²",
      completion: "Q3 2025",
      rating: 4.9,
      reviews: 67,
      image: "/placeholder.svg?height=300&width=400",
      gallery: ["/placeholder.svg?height=200&width=300", "/placeholder.svg?height=200&width=300"],
      discount: "2% скидка",
      class: "Премиум",
      apartments: 85,
      available: 12,
      features: ["Консьерж", "Спа", "Ресторан", "Винный погреб"],
      metro: "Кропоткинская, 3 мин",
      floors: "12 этажей",
    },
  ]

  const filters = {
    regions: ["Москва", "Санкт-Петербург", "Краснодар", "Екатеринбург", "Новосибирск"],
    classes: ["Эконом", "Комфорт", "Комфорт+", "Бизнес", "Премиум"],
    completion: ["2024", "2025", "2026", "2027+"],
    features: ["Паркинг", "Детская площадка", "Фитнес-зал", "Консьерж", "Спа-центр", "Кафе/Ресторан"],
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b bg-white sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Home className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Недвижимость 4.0</span>
            </Link>

            <nav className="hidden md:flex items-center space-x-8">
              <Link href="/catalog" className="text-blue-600 font-medium">
                Каталог
              </Link>
              <Link href="#" className="text-gray-700 hover:text-blue-600 font-medium">
                Карта
              </Link>
              <Link href="#" className="text-gray-700 hover:text-blue-600 font-medium">
                Застройщикам
              </Link>
            </nav>

            <Button>Войти</Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filters Sidebar */}
          <div className="lg:w-80">
            <div className="lg:hidden mb-4">
              <Sheet>
                <SheetTrigger asChild>
                  <Button variant="outline" className="w-full bg-transparent">
                    <Filter className="w-4 h-4 mr-2" />
                    Фильтры
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="w-80">
                  <SheetHeader>
                    <SheetTitle>Фильтры поиска</SheetTitle>
                    <SheetDescription>Настройте параметры для поиска идеального жилья</SheetDescription>
                  </SheetHeader>
                  <FilterContent filters={filters} priceRange={priceRange} setPriceRange={setPriceRange} />
                </SheetContent>
              </Sheet>
            </div>

            <div className="hidden lg:block">
              <Card>
                <CardHeader>
                  <CardTitle>Фильтры поиска</CardTitle>
                  <CardDescription>Настройте параметры поиска</CardDescription>
                </CardHeader>
                <CardContent>
                  <FilterContent filters={filters} priceRange={priceRange} setPriceRange={setPriceRange} />
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Search and Sort */}
            <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
              <div className="flex flex-col md:flex-row gap-4 mb-4">
                <div className="flex-1">
                  <Input placeholder="Поиск по названию, застройщику или району..." className="h-12" />
                </div>
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="w-full md:w-48 h-12">
                    <ArrowUpDown className="w-4 h-4 mr-2" />
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="price-asc">Цена: по возрастанию</SelectItem>
                    <SelectItem value="price-desc">Цена: по убыванию</SelectItem>
                    <SelectItem value="rating">По рейтингу</SelectItem>
                    <SelectItem value="completion">По сроку сдачи</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="flex items-center justify-between">
                <p className="text-gray-600">Найдено {projects.length} проектов</p>
                <div className="flex items-center space-x-2">
                  <Button
                    variant={viewMode === "grid" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setViewMode("grid")}
                  >
                    Сетка
                  </Button>
                  <Button
                    variant={viewMode === "list" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setViewMode("list")}
                  >
                    Список
                  </Button>
                </div>
              </div>
            </div>

            {/* Projects Grid */}
            <div className={`grid gap-6 ${viewMode === "grid" ? "grid-cols-1 md:grid-cols-2" : "grid-cols-1"}`}>
              {projects.map((project) => (
                <Card key={project.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                  <div className={`${viewMode === "list" ? "flex" : ""}`}>
                    <div className={`relative ${viewMode === "list" ? "w-80 flex-shrink-0" : ""}`}>
                      <Image
                        src={project.image || "/placeholder.svg"}
                        alt={project.name}
                        width={400}
                        height={300}
                        className={`object-cover ${viewMode === "list" ? "h-full" : "w-full h-48"}`}
                      />
                      <Badge className="absolute top-4 left-4 bg-red-500 hover:bg-red-600">{project.discount}</Badge>
                      <Badge variant="secondary" className="absolute top-4 right-4">
                        {project.class}
                      </Badge>
                      <div className="absolute bottom-4 right-4 flex space-x-2">
                        <Button size="sm" variant="secondary" className="h-8 w-8 p-0">
                          <Heart className="w-4 h-4" />
                        </Button>
                        <Button size="sm" variant="secondary" className="h-8 w-8 p-0">
                          <Share2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>

                    <div className="flex-1">
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div>
                            <CardTitle className="text-lg mb-1">{project.name}</CardTitle>
                            <CardDescription className="flex items-center mb-2">
                              <MapPin className="w-4 h-4 mr-1" />
                              {project.location}
                            </CardDescription>
                            <p className="text-sm text-gray-600">{project.metro}</p>
                          </div>
                          <div className="flex items-center">
                            <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                            <span className="text-sm font-medium">{project.rating}</span>
                            <span className="text-xs text-gray-500 ml-1">({project.reviews})</span>
                          </div>
                        </div>
                      </CardHeader>

                      <CardContent>
                        <div className="space-y-3">
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>
                              <span className="text-gray-600">Застройщик:</span>
                              <p className="font-medium">{project.developer}</p>
                            </div>
                            <div>
                              <span className="text-gray-600">Этажность:</span>
                              <p className="font-medium">{project.floors}</p>
                            </div>
                            <div>
                              <span className="text-gray-600">Квартир:</span>
                              <p className="font-medium">
                                {project.apartments} (свободно: {project.available})
                              </p>
                            </div>
                            <div>
                              <span className="text-gray-600">Сдача:</span>
                              <p className="font-medium flex items-center">
                                <Calendar className="w-4 h-4 mr-1" />
                                {project.completion}
                              </p>
                            </div>
                          </div>

                          <div className="flex flex-wrap gap-1">
                            {project.features.slice(0, 4).map((feature, index) => (
                              <Badge key={index} variant="outline" className="text-xs">
                                {feature}
                              </Badge>
                            ))}
                            {project.features.length > 4 && (
                              <Badge variant="outline" className="text-xs">
                                +{project.features.length - 4}
                              </Badge>
                            )}
                          </div>

                          <div className="pt-3 border-t">
                            <div className="flex justify-between items-center mb-4">
                              <div>
                                <div className="text-2xl font-bold text-blue-600">{project.price}</div>
                                <div className="text-sm text-gray-600">{project.pricePerSqm}</div>
                              </div>
                            </div>
                            <div className="flex space-x-2">
                              <Button className="flex-1">Подробнее</Button>
                              <Button variant="outline" className="flex items-center bg-transparent">
                                <Eye className="w-4 h-4 mr-1" />
                                3D-тур
                              </Button>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center mt-8">
              <div className="flex space-x-2">
                <Button variant="outline">Предыдущая</Button>
                <Button>1</Button>
                <Button variant="outline">2</Button>
                <Button variant="outline">3</Button>
                <Button variant="outline">Следующая</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function FilterContent({ filters, priceRange, setPriceRange }: any) {
  return (
    <div className="space-y-6">
      {/* Price Range */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Цена: {priceRange[0].toLocaleString()} - {priceRange[1].toLocaleString()} ₽
        </label>
        <Slider
          value={priceRange}
          onValueChange={setPriceRange}
          max={30000000}
          min={1000000}
          step={100000}
          className="w-full"
        />
      </div>

      {/* Region */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Регион</label>
        <Select>
          <SelectTrigger>
            <SelectValue placeholder="Выберите регион" />
          </SelectTrigger>
          <SelectContent>
            {filters.regions.map((region: string) => (
              <SelectItem key={region} value={region.toLowerCase()}>
                {region}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Class */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Класс жилья</label>
        <div className="space-y-2">
          {filters.classes.map((cls: string) => (
            <div key={cls} className="flex items-center space-x-2">
              <Checkbox id={cls} />
              <label htmlFor={cls} className="text-sm">
                {cls}
              </label>
            </div>
          ))}
        </div>
      </div>

      {/* Completion */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Срок сдачи</label>
        <div className="space-y-2">
          {filters.completion.map((year: string) => (
            <div key={year} className="flex items-center space-x-2">
              <Checkbox id={year} />
              <label htmlFor={year} className="text-sm">
                {year}
              </label>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Удобства</label>
        <div className="space-y-2">
          {filters.features.map((feature: string) => (
            <div key={feature} className="flex items-center space-x-2">
              <Checkbox id={feature} />
              <label htmlFor={feature} className="text-sm">
                {feature}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-4 border-t">
        <Button className="w-full mb-2">Применить фильтры</Button>
        <Button variant="outline" className="w-full bg-transparent">
          Сбросить
        </Button>
      </div>
    </div>
  )
}
