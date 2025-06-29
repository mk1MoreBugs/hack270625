"use client"

import { useState } from "react"
import { Star, MapPin, Phone, Mail, Share2, Heart, Eye, Home, Square, ChefHat } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"
import Link from "next/link"
import { projectsData } from "@/lib/data"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

// Функция для получения данных квартиры по ID
const getApartmentById = (apartmentId: string) => {
  // Извлекаем projectId из apartmentId (формат: projectId-apartmentId)
  const projectId = apartmentId.split("-")[0]
  const project = projectsData.find((p) => p.id === projectId)

  if (!project) return null

  // Генерируем данные квартиры на основе ID в соответствии с новой структурой
  const apartmentData = {
    "1-a1": {
      number: "101",
      floor: 5,
      rooms: 0,
      area_total: 28.5,
      area_living: 18,
      area_kitchen: 10.5,
      base_price: 4200000,
      current_price: 4200000,
      balcony: true,
      loggia: false,
      parking: false,
      layout_image_url: null,
      building_id: 1,
      status: "available" as const,
      name: "Студия",
      description:
        "Уютная студия с современной планировкой и панорамными окнами. Идеально подходит для молодых специалистов или студентов.",
      features: ["Балкон", "Кондиционер", "Встроенная кухня", "Высокие потолки"],
    },
    "1-a2": {
      number: "205",
      floor: 8,
      rooms: 1,
      area_total: 42.3,
      area_living: 18.5,
      area_kitchen: 12.8,
      base_price: 5800000,
      current_price: 5800000,
      balcony: true,
      loggia: false,
      parking: true,
      layout_image_url: null,
      building_id: 1,
      status: "available" as const,
      name: "1-комнатная",
      description: "Просторная однокомнатная квартира с отдельной кухней и большой гостиной. Отличный выбор для пары.",
      features: ["Балкон", "Гардеробная", "Кондиционер", "Встроенная техника", "Паркинг"],
    },
    "1-a3": {
      number: "312",
      floor: 12,
      rooms: 2,
      area_total: 65.7,
      area_living: 35.2,
      area_kitchen: 15.5,
      base_price: 7500000,
      current_price: 7500000,
      balcony: false,
      loggia: true,
      parking: true,
      layout_image_url: null,
      building_id: 1,
      status: "available" as const,
      name: "2-комнатная",
      description: "Двухкомнатная квартира с изолированными комнатами и просторной кухней-гостиной.",
      features: ["Лоджия", "Гардеробная", "Кондиционер", "Кладовая", "Встроенная техника", "Паркинг"],
    },
  }

  const apartmentInfo = apartmentData[apartmentId as keyof typeof apartmentData] || apartmentData["1-a1"]

  return {
    id: apartmentId,
    ...apartmentInfo,
    project: project.name,
    projectId: projectId,
    developer: project.developer,
    location: project.location,
    completion: project.completion,
    class: project.class,
    rating: project.rating || 4.8,
    image: "/placeholder.svg?height=600&width=800",
    gallery: [
      "/placeholder.svg?height=600&width=800",
      "/placeholder.svg?height=600&width=800",
      "/placeholder.svg?height=600&width=800",
      "/placeholder.svg?height=600&width=800",
    ],
    created_at: "2025-06-28T06:32:34.547929",
    updated_at: "2025-06-28T06:32:34.547931",
  }
}

export default function ApartmentPage({ params }: { params: { id: string } }) {
  const [selectedImage, setSelectedImage] = useState(0)
  const apartment = getApartmentById(params.id)

  if (!apartment) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Квартира не найдена</h1>
          <Link href="/catalog">
            <Button>Вернуться к каталогу</Button>
          </Link>
        </div>
      </div>
    )
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("ru-RU", {
      style: "currency",
      currency: "RUB",
      maximumFractionDigits: 0,
    }).format(price)
  }

  const pricePerSqm = Math.round(apartment.current_price! / apartment.area_total!)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6 flex justify-between items-center">
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href="/">Недвижимость 5.0</Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href="/catalog">Каталог</Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href={`/real_estates/${apartment.projectId}`}>{apartment.project}</Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage>Квартира №{apartment.number}</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="icon">
              <Share2 className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon">
              <Heart className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            {/* Gallery */}
            <Card>
              <CardContent className="p-0">
                <div className="relative">
                  <Image
                    src={apartment.gallery[selectedImage] || "/placeholder.svg"}
                    alt={`Квартира №${apartment.number} - изображение ${selectedImage + 1}`}
                    width={800}
                    height={600}
                    className="w-full h-96 object-cover rounded-t-lg"
                  />
                  <Button className="absolute top-4 right-4" variant="secondary">
                    <Eye className="w-4 h-4 mr-2" />
                    3D-тур
                  </Button>
                  <Badge
                    className={`absolute top-4 left-4 ${
                      apartment.status === "available"
                        ? "bg-green-500 hover:bg-green-600"
                        : apartment.status === "reserved"
                          ? "bg-yellow-500 hover:bg-yellow-600"
                          : "bg-red-500 hover:bg-red-600"
                    }`}
                  >
                    {apartment.status === "available"
                      ? "Доступна"
                      : apartment.status === "reserved"
                        ? "Забронирована"
                        : "Продана"}
                  </Badge>
                </div>
                <div className="p-4">
                  <div className="flex space-x-2 overflow-x-auto">
                    {apartment.gallery.map((image, index) => (
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

            {/* Description */}
            <Card>
              <CardHeader>
                <CardTitle>Описание квартиры</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed mb-6">{apartment.description}</p>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{apartment.area_total}</div>
                    <div className="text-sm text-gray-600">м² общая</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{apartment.area_living}</div>
                    <div className="text-sm text-gray-600">м² жилая</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{apartment.area_kitchen}</div>
                    <div className="text-sm text-gray-600">м² кухня</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{apartment.floor}</div>
                    <div className="text-sm text-gray-600">этаж</div>
                  </div>
                </div>

                <h3 className="text-lg font-semibold mb-4">Характеристики</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Home className="w-5 h-5 text-blue-600" />
                      <span>Комнат</span>
                    </div>
                    <span className="font-medium">{apartment.rooms === 0 ? "Студия" : apartment.rooms}</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Square className="w-5 h-5 text-blue-600" />
                      <span>Балкон</span>
                    </div>
                    <span className="font-medium">{apartment.balcony ? "Есть" : "Нет"}</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Square className="w-5 h-5 text-blue-600" />
                      <span>Лоджия</span>
                    </div>
                    <span className="font-medium">{apartment.loggia ? "Есть" : "Нет"}</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <ChefHat className="w-5 h-5 text-blue-600" />
                      <span>Паркинг</span>
                    </div>
                    <span className="font-medium">{apartment.parking ? "Включен" : "Не включен"}</span>
                  </div>
                </div>

                <h3 className="text-lg font-semibold mb-4">Особенности квартиры</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {apartment.features?.map((feature, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                      <Star className="w-6 h-6 text-blue-600 mt-1" />
                      <div>
                        <div className="font-medium">{feature}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Project Info */}
            <Card>
              <CardHeader>
                <CardTitle>О жилом комплексе</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Застройщик:</span>
                    <span className="font-medium">{apartment.developer}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Адрес:</span>
                    <span className="font-medium">{apartment.location}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Срок сдачи:</span>
                    <span className="font-medium">{apartment.completion}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Рейтинг проекта:</span>
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                      <span className="font-medium">{apartment.rating}</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="lg:sticky lg:top-24 self-start">
            <Card>
              <CardHeader>
                <h1 className="text-2xl font-bold">
                  {apartment.name} №{apartment.number}
                </h1>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <MapPin className="h-4 w-4" />
                  <span>{apartment.project}</span>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-3xl font-bold text-blue-600">{formatPrice(apartment.current_price!)}</div>
                <div className="text-lg text-gray-600">{pricePerSqm.toLocaleString()} ₽/м²</div>
                {apartment.base_price !== apartment.current_price && (
                  <div className="text-sm text-gray-500 line-through">{formatPrice(apartment.base_price!)}</div>
                )}
                <Separator />
                <div className="space-y-4">
                  <h3 className="font-semibold">Купить квартиру</h3>
                  <div className="space-y-3">
                    <Input placeholder="Ваше имя" />
                    <Input placeholder="Телефон" type="tel" />
                    <Input placeholder="Email" type="email" />
                    <Textarea placeholder="Дополнительные пожелания" rows={3} />
                  </div>
                </div>
                <Separator />
                <Button size="lg" className="w-full" disabled={apartment.status !== "available"}>
                  <Phone className="h-5 w-5 mr-2" />
                  {apartment.status === "available" ? "Купить" : "Недоступна"}
                </Button>
                <Button size="lg" variant="outline" className="w-full bg-transparent">
                  <Mail className="h-5 w-5 mr-2" />
                  Получить консультацию
                </Button>
                <Button size="lg" variant="outline" className="w-full bg-transparent">
                  <Eye className="h-5 w-5 mr-2" />
                  3D-тур квартиры
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
