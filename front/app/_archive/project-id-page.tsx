"use client"

import { useState } from "react"
import {
  ArrowLeft,
  Star,
  MapPin,
  Calendar,
  Home,
  Phone,
  Mail,
  Share2,
  Heart,
  Eye,
  Car,
  Wifi,
  Dumbbell,
  Shield,
  Baby,
  ShoppingCart,
  Trees,
  Camera,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import Image from "next/image"
import Link from "next/link"

export default function ProjectPage() {
  const [selectedImage, setSelectedImage] = useState(0)
  const [selectedApartment, setSelectedApartment] = useState("")

  const project = {
    id: 1,
    name: "ЖК Северная Звезда",
    developer: "СтройИнвест",
    location: "Москва, САО, ул. Дубнинская, 73А",
    price: "от 8 500 000 ₽",
    pricePerSqm: "от 185 000 ₽/м²",
    completion: "Q4 2025",
    rating: 4.8,
    reviews: 124,
    discount: "5% скидка до 31 декабря",
    class: "Комфорт+",
    totalApartments: 245,
    available: 89,
    floors: "25 этажей",
    metro: "м. Алтуфьево, 15 мин пешком",
    description:
      "Современный жилой комплекс в экологически чистом районе Москвы. Продуманная планировка, качественная отделка и развитая инфраструктура делают этот проект идеальным для комфортной жизни.",
    features: [
      { icon: Car, name: "Подземный паркинг", description: "300 машиномест" },
      { icon: Baby, name: "Детская площадка", description: "Современное оборудование" },
      { icon: Dumbbell, name: "Фитнес-зал", description: "Полностью оборудован" },
      { icon: Shield, name: "Охрана 24/7", description: "Видеонаблюдение" },
      { icon: Wifi, name: "Высокоскоростной интернет", description: "До 1 Гбит/с" },
      { icon: ShoppingCart, name: "Торговая галерея", description: "Магазины и кафе" },
      { icon: Trees, name: "Ландшафтный дизайн", description: "Зеленые зоны" },
      { icon: Camera, name: "Консьерж-сервис", description: "Круглосуточно" },
    ],
    gallery: [
      "/placeholder.svg?height=600&width=800",
      "/placeholder.svg?height=600&width=800",
      "/placeholder.svg?height=600&width=800",
      "/placeholder.svg?height=600&width=800",
      "/placeholder.svg?height=600&width=800",
    ],
    layouts: [
      { type: "Студия", area: "25-30 м²", price: "от 4 625 000 ₽", available: 12 },
      { type: "1-комнатная", area: "35-45 м²", price: "от 6 475 000 ₽", available: 28 },
      { type: "2-комнатная", area: "55-70 м²", price: "от 10 175 000 ₽", available: 35 },
      { type: "3-комнатная", area: "75-95 м²", price: "от 13 875 000 ₽", available: 14 },
    ],
    progress: {
      foundation: 100,
      walls: 85,
      roof: 60,
      finishing: 25,
    },
  }

  const reviews = [
    {
      id: 1,
      author: "Анна Петрова",
      rating: 5,
      date: "15 декабря 2024",
      text: "Отличный проект! Купили квартиру в этом ЖК, очень довольны качеством строительства и планировкой.",
      avatar: "/placeholder.svg?height=40&width=40",
    },
    {
      id: 2,
      author: "Михаил Сидоров",
      rating: 4,
      date: "10 декабря 2024",
      text: "Хорошее расположение, развитая инфраструктура. Единственный минус - далековато от метро.",
      avatar: "/placeholder.svg?height=40&width=40",
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b bg-white sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/catalog">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Назад к каталогу
                </Button>
              </Link>
              <div className="hidden md:block">
                <Link href="/" className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                    <Home className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xl font-bold text-gray-900">Недвижимость 4.0</span>
                </Link>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                <Share2 className="w-4 h-4 mr-2" />
                Поделиться
              </Button>
              <Button variant="outline" size="sm">
                <Heart className="w-4 h-4 mr-2" />В избранное
              </Button>
              <Button>Войти</Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Project Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{project.name}</h1>
              <div className="flex items-center space-x-4 text-gray-600 mb-2">
                <div className="flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  {project.location}
                </div>
                <div className="flex items-center">
                  <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                  {project.rating} ({project.reviews} отзывов)
                </div>
              </div>
              <p className="text-gray-600">{project.metro}</p>
            </div>
            <div className="mt-4 md:mt-0">
              <Badge className="bg-red-500 hover:bg-red-600 mb-2">{project.discount}</Badge>
              <div className="text-right">
                <div className="text-3xl font-bold text-blue-600">{project.price}</div>
                <div className="text-gray-600">{project.pricePerSqm}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Gallery */}
            <Card>
              <CardContent className="p-0">
                <div className="relative">
                  <Image
                    src={project.gallery[selectedImage] || "/placeholder.svg"}
                    alt={project.name}
                    width={800}
                    height={600}
                    className="w-full h-96 object-cover rounded-t-lg"
                  />
                  <Button className="absolute top-4 right-4" variant="secondary">
                    <Eye className="w-4 h-4 mr-2" />
                    3D-тур
                  </Button>
                </div>
                <div className="p-4">
                  <div className="flex space-x-2 overflow-x-auto">
                    {project.gallery.map((image, index) => (
                      <button
                        key={index}
                        onClick={() => setSelectedImage(index)}
                        className={`flex-shrink-0 w-20 h-16 rounded-lg overflow-hidden border-2 ${
                          selectedImage === index ? "border-blue-500" : "border-gray-200"
                        }`}
                      >
                        <Image
                          src={image || "/placeholder.svg"}
                          alt={`Gallery ${index + 1}`}
                          width={80}
                          height={64}
                          className="w-full h-full object-cover"
                        />
                      </button>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Tabs */}
            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Обзор</TabsTrigger>
                <TabsTrigger value="apartments">Квартиры</TabsTrigger>
                <TabsTrigger value="progress">Ход строительства</TabsTrigger>
                <TabsTrigger value="reviews">Отзывы</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>О проекте</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-700 mb-6">{project.description}</p>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{project.totalApartments}</div>
                        <div className="text-sm text-gray-600">Квартир</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{project.available}</div>
                        <div className="text-sm text-gray-600">Доступно</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{project.floors}</div>
                        <div className="text-sm text-gray-600">Этажность</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{project.class}</div>
                        <div className="text-sm text-gray-600">Класс</div>
                      </div>
                    </div>

                    <h3 className="text-lg font-semibold mb-4">Инфраструктура и удобства</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {project.features.map((feature, index) => (
                        <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                          <feature.icon className="w-6 h-6 text-blue-600 mt-1" />
                          <div>
                            <div className="font-medium">{feature.name}</div>
                            <div className="text-sm text-gray-600">{feature.description}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="apartments" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Доступные планировки</CardTitle>
                    <CardDescription>Выберите подходящий тип квартиры</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-4">
                      {project.layouts.map((apt, index) => (
                        <div key={index} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                          <div className="flex items-center justify-between">
                            <div>
                              <h3 className="font-semibold text-lg">{apt.type}</h3>
                              <p className="text-gray-600">{apt.area}</p>
                              <p className="text-sm text-gray-500">Доступно: {apt.available} квартир</p>
                            </div>
                            <div className="text-right">
                              <div className="text-xl font-bold text-blue-600">{apt.price}</div>
                              <Button className="mt-2">Выбрать</Button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="progress" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Ход строительства</CardTitle>
                    <CardDescription>Актуальная информация о стадии строительства</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">Фундамент</span>
                        <span className="text-sm text-gray-600">{project.progress.foundation}%</span>
                      </div>
                      <Progress value={project.progress.foundation} className="h-2" />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">Стены и перекрытия</span>
                        <span className="text-sm text-gray-600">{project.progress.walls}%</span>
                      </div>
                      <Progress value={project.progress.walls} className="h-2" />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">Кровля</span>
                        <span className="text-sm text-gray-600">{project.progress.roof}%</span>
                      </div>
                      <Progress value={project.progress.roof} className="h-2" />
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">Отделочные работы</span>
                        <span className="text-sm text-gray-600">{project.progress.finishing}%</span>
                      </div>
                      <Progress value={project.progress.finishing} className="h-2" />
                    </div>

                    <div className="bg-blue-50 p-4 rounded-lg">
                      <div className="flex items-center mb-2">
                        <Calendar className="w-5 h-5 text-blue-600 mr-2" />
                        <span className="font-medium">Планируемая сдача: {project.completion}</span>
                      </div>
                      <p className="text-sm text-gray-600">
                        Строительство идет по графику. Ключи планируется выдать в декабре 2025 года.
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="reviews" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Отзывы покупателей</CardTitle>
                    <CardDescription>
                      Средняя оценка: {project.rating} из 5 ({project.reviews} отзывов)
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {reviews.map((review) => (
                      <div key={review.id} className="border-b pb-6 last:border-b-0">
                        <div className="flex items-start space-x-4">
                          <Avatar>
                            <AvatarImage src={review.avatar || "/placeholder.svg"} />
                            <AvatarFallback>
                              {review.author
                                .split(" ")
                                .map((n) => n[0])
                                .join("")}
                            </AvatarFallback>
                          </Avatar>
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="font-medium">{review.author}</h4>
                              <div className="flex items-center">
                                {[...Array(5)].map((_, i) => (
                                  <Star
                                    key={i}
                                    className={`w-4 h-4 ${
                                      i < review.rating ? "text-yellow-400 fill-current" : "text-gray-300"
                                    }`}
                                  />
                                ))}
                                <span className="ml-2 text-sm text-gray-600">{review.date}</span>
                              </div>
                            </div>
                            <p className="text-gray-700">{review.text}</p>
                          </div>
                        </div>
                      </div>
                    ))}

                    <Button variant="outline" className="w-full bg-transparent">
                      Показать все отзывы
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Contact Form */}
            <Card>
              <CardHeader>
                <CardTitle>Забронировать квартиру</CardTitle>
                <CardDescription>Оставьте заявку и получите персональное предложение</CardDescription>
              </CardHeader>
              <CardContent>
                <form className="space-y-4">
                  <div>
                    <Input placeholder="Ваше имя" />
                  </div>
                  <div>
                    <Input placeholder="Телефон" type="tel" />
                  </div>
                  <div>
                    <Input placeholder="Email" type="email" />
                  </div>
                  <div>
                    <Select value={selectedApartment} onValueChange={setSelectedApartment}>
                      <SelectTrigger>
                        <SelectValue placeholder="Тип квартиры" />
                      </SelectTrigger>
                      <SelectContent>
                        {project.layouts.map((apt, index) => (
                          <SelectItem key={index} value={apt.type}>
                            {apt.type} ({apt.area})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Textarea placeholder="Дополнительные пожелания" rows={3} />
                  </div>
                  <Button className="w-full">Отправить заявку</Button>
                  <p className="text-xs text-gray-500 text-center">
                    Нажимая кнопку, вы соглашаетесь с обработкой персональных данных
                  </p>
                </form>
              </CardContent>
            </Card>

            {/* Developer Info */}
            <Card>
              <CardHeader>
                <CardTitle>Застройщик</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-lg">{project.developer}</h3>
                    <p className="text-sm text-gray-600">На рынке с 2010 года</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-blue-600">45</div>
                      <div className="text-xs text-gray-600">Проектов</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-blue-600">4.7</div>
                      <div className="text-xs text-gray-600">Рейтинг</div>
                    </div>
                  </div>

                  <div className="flex space-x-2">
                    <Button variant="outline" className="flex-1 bg-transparent">
                      <Phone className="w-4 h-4 mr-2" />
                      Позвонить
                    </Button>
                    <Button variant="outline" className="flex-1 bg-transparent">
                      <Mail className="w-4 h-4 mr-2" />
                      Написать
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Быстрые действия</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start bg-transparent">
                  <Eye className="w-4 h-4 mr-2" />
                  Виртуальный тур
                </Button>
                <Button variant="outline" className="w-full justify-start bg-transparent">
                  <MapPin className="w-4 h-4 mr-2" />
                  Показать на карте
                </Button>
                <Button variant="outline" className="w-full justify-start bg-transparent">
                  <Calendar className="w-4 h-4 mr-2" />
                  Записаться на показ
                </Button>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="w-full justify-start bg-transparent">
                      <Camera className="w-4 h-4 mr-2" />
                      Заказать фото отчет
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Заказать фото отчет</DialogTitle>
                      <DialogDescription>Получите актуальные фотографии хода строительства на email</DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4">
                      <Input placeholder="Ваш email" type="email" />
                      <Button className="w-full">Заказать отчет</Button>
                    </div>
                  </DialogContent>
                </Dialog>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
