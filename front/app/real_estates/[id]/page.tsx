"use client"

import type React from "react"
import { Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { useState, useMemo } from "react"
import { Filter, ArrowUpDown, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Checkbox } from "@/components/ui/checkbox"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { projectsData } from "@/lib/data"
import { ApartmentCard } from "@/components/apartments/ApartmentCard"
import Link from "next/link"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

// Данные квартир для конкретного ЖК
const getApartmentsForProject = (projectId: string) => {
  const project = projectsData.find((p) => p.id === projectId)
  if (!project) return []

  // Генерируем квартиры для проекта
  return [
    {
      id: `${projectId}-a1`,
      name: "Студия",
      project: project.name,
      area: 28,
      price: "4.2 млн ₽",
      image: "/placeholder.svg?height=300&width=400",
      promotion: project.promotion || "Скидка 5%",
      tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
      rooms: 0,
      floor: 5,
      priceNum: 4200000,
      projectId: projectId,
      description: "Уютная студия с современной планировкой и панорамными окнами",
      features: ["Балкон", "Кондиционер", "Встроенная кухня"],
      developer: project.developer,
      completion: project.completion,
      class: project.class,
    },
    {
      id: `${projectId}-a2`,
      name: "1-комнатная",
      project: project.name,
      area: 42,
      price: "5.8 млн ₽",
      image: "/placeholder.svg?height=300&width=400",
      promotion: project.promotion || "Скидка 5%",
      tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
      rooms: 1,
      floor: 8,
      priceNum: 5800000,
      projectId: projectId,
      description: "Просторная однокомнатная квартира с отдельной кухней",
      features: ["Балкон", "Гардеробная", "Кондиционер"],
      developer: project.developer,
      completion: project.completion,
      class: project.class,
    },
    {
      id: `${projectId}-a3`,
      name: "2-комнатная",
      project: project.name,
      area: 65,
      price: "7.5 млн ₽",
      image: "/placeholder.svg?height=300&width=400",
      promotion: project.promotion || "Скидка 5%",
      tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
      rooms: 2,
      floor: 12,
      priceNum: 7500000,
      projectId: projectId,
      description: "Двухкомнатная квартира с изолированными комнатами",
      features: ["Лоджия", "Гардеробная", "Кондиционер", "Кладовая"],
      developer: project.developer,
      completion: project.completion,
      class: project.class,
    },
    {
      id: `${projectId}-a4`,
      name: "2-комнатная",
      project: project.name,
      area: 72,
      price: "8.2 млн ₽",
      image: "/placeholder.svg?height=300&width=400",
      promotion: project.promotion || "Скидка 5%",
      tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
      rooms: 2,
      floor: 15,
      priceNum: 8200000,
      projectId: projectId,
      description: "Улучшенная двухкомнатная квартира с большой кухней-гостиной",
      features: ["Лоджия", "Гардеробная", "Кондиционер", "Кладовая", "Панорамные окна"],
      developer: project.developer,
      completion: project.completion,
      class: project.class,
    },
    {
      id: `${projectId}-a5`,
      name: "3-комнатная",
      project: project.name,
      area: 88,
      price: "10.1 млн ₽",
      image: "/placeholder.svg?height=300&width=400",
      promotion: project.promotion || "Скидка 5%",
      tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
      rooms: 3,
      floor: 18,
      priceNum: 10100000,
      projectId: projectId,
      description: "Трехкомнатная квартира для большой семьи",
      features: ["Лоджия", "Гардеробная", "Кондиционер", "Кладовая", "Мастер-спальня"],
      developer: project.developer,
      completion: project.completion,
      class: project.class,
    },
    {
      id: `${projectId}-a6`,
      name: "3-комнатная",
      project: project.name,
      area: 95,
      price: "11.3 млн ₽",
      image: "/placeholder.svg?height=300&width=400",
      promotion: project.promotion || "Скидка 5%",
      tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
      rooms: 3,
      floor: 20,
      priceNum: 11300000,
      projectId: projectId,
      description: "Премиальная трехкомнатная квартира с видом на город",
      features: ["Лоджия", "Гардеробная", "Кондиционер", "Кладовая", "Мастер-спальня", "Панорамные окна"],
      developer: project.developer,
      completion: project.completion,
      class: project.class,
    },
  ]
}

function RealEstatesContent({ params }: { params: { id: string } }) {
  const searchParams = useSearchParams()
  const project = projectsData.find((p) => p.id === params.id)
  const apartments = getApartmentsForProject(params.id)

  const [searchQuery, setSearchQuery] = useState(searchParams.get("q") || "")
  const [priceRange, setPriceRange] = useState<[number, number]>([
    Number(searchParams.get("minPrice")) || 1000000,
    Number(searchParams.get("maxPrice")) || 30000000,
  ])
  const [selectedRooms, setSelectedRooms] = useState<string[]>([])
  const [selectedFloors, setSelectedFloors] = useState<string[]>([])
  const [selectedAreas, setSelectedAreas] = useState<string[]>([])
  const [selectedPromotions, setSelectedPromotions] = useState<string[]>([])

  const [sortBy, setSortBy] = useState("price-asc")

  const handleCheckboxChange = (setter: React.Dispatch<React.SetStateAction<string[]>>, value: string) => {
    setter((prev) => (prev.includes(value) ? prev.filter((item) => item !== value) : [...prev, value]))
  }

  const resetFilters = () => {
    setSearchQuery("")
    setPriceRange([1000000, 30000000])
    setSelectedRooms([])
    setSelectedFloors([])
    setSelectedAreas([])
    setSelectedPromotions([])
    setSortBy("price-asc")
  }

  const displayedApartments = useMemo(() => {
    let filtered = [...apartments]

    if (searchQuery) {
      const lowercasedQuery = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (a) => a.name.toLowerCase().includes(lowercasedQuery) || a.project.toLowerCase().includes(lowercasedQuery),
      )
    }

    filtered = filtered.filter((a) => {
      return a.priceNum! >= priceRange[0] && a.priceNum! <= priceRange[1]
    })

    if (selectedRooms.length > 0) {
      filtered = filtered.filter((a) => selectedRooms.includes(a.rooms!.toString()))
    }

    if (selectedFloors.length > 0) {
      filtered = filtered.filter((a) => {
        if (selectedFloors.includes("1-5") && a.floor! >= 1 && a.floor! <= 5) return true
        if (selectedFloors.includes("6-10") && a.floor! >= 6 && a.floor! <= 10) return true
        if (selectedFloors.includes("11-15") && a.floor! >= 11 && a.floor! <= 15) return true
        if (selectedFloors.includes("16+") && a.floor! >= 16) return true
        return false
      })
    }

    if (selectedAreas.length > 0) {
      filtered = filtered.filter((a) => {
        if (selectedAreas.includes("до 40") && a.area < 40) return true
        if (selectedAreas.includes("40-60") && a.area >= 40 && a.area <= 60) return true
        if (selectedAreas.includes("60-80") && a.area >= 60 && a.area <= 80) return true
        if (selectedAreas.includes("80+") && a.area >= 80) return true
        return false
      })
    }

    if (selectedPromotions.length > 0) {
      filtered = filtered.filter((a) => a.promotion && selectedPromotions.includes(a.promotion))
    }

    switch (sortBy) {
      case "price-asc":
        filtered.sort((a, b) => a.priceNum! - b.priceNum!)
        break
      case "price-desc":
        filtered.sort((a, b) => b.priceNum! - a.priceNum!)
        break
      case "area-asc":
        filtered.sort((a, b) => a.area - b.area)
        break
      case "area-desc":
        filtered.sort((a, b) => b.area - a.area)
        break
      case "floor":
        filtered.sort((a, b) => a.floor! - b.floor!)
        break
    }

    return filtered
  }, [searchQuery, priceRange, selectedRooms, selectedFloors, selectedAreas, selectedPromotions, sortBy, apartments])

  const filterContentProps = {
    priceRange,
    setPriceRange,
    selectedRooms,
    handleRoomsChange: (value: string) => handleCheckboxChange(setSelectedRooms, value),
    selectedFloors,
    handleFloorsChange: (value: string) => handleCheckboxChange(setSelectedFloors, value),
    selectedAreas,
    handleAreasChange: (value: string) => handleCheckboxChange(setSelectedAreas, value),
    selectedPromotions,
    handlePromotionChange: (value: string) => handleCheckboxChange(setSelectedPromotions, value),
    resetFilters,
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">ЖК не найден</h1>
          <Link href="/catalog">
            <Button>Вернуться к каталогу</Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
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
                <BreadcrumbPage>{project.name}</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>

        <div className="mb-8">
          <div className="flex items-center gap-4 mb-4">
            <Link href="/catalog">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Назад к каталогу
              </Button>
            </Link>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Квартиры в {project.name}</h1>
          <p className="text-gray-600">
            {project.location} • {project.developer}
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          <aside className="lg:w-80 lg:sticky lg:top-24 self-start">
            <div className="lg:hidden mb-4">
              <Sheet>
                <SheetTrigger asChild>
                  <Button variant="outline" className="w-full bg-transparent">
                    <Filter className="w-4 h-4 mr-2" />
                    Фильтры
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="w-80 overflow-y-auto">
                  <SheetHeader>
                    <SheetTitle>Фильтры поиска</SheetTitle>
                    <SheetDescription>Настройте параметры для поиска квартиры</SheetDescription>
                  </SheetHeader>
                  <ApartmentFilterContent {...filterContentProps} />
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
                  <ApartmentFilterContent {...filterContentProps} />
                </CardContent>
              </Card>
            </div>
          </aside>

          <main className="flex-1">
            <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
              <div className="flex flex-col md:flex-row gap-4 mb-4">
                <div className="flex-1">
                  <Input
                    placeholder="Поиск по типу квартиры..."
                    className="h-12"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="w-full md:w-48 h-12">
                    <ArrowUpDown className="w-4 h-4 mr-2" />
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="price-asc">Цена: по возрастанию</SelectItem>
                    <SelectItem value="price-desc">Цена: по убыванию</SelectItem>
                    <SelectItem value="area-asc">Площадь: по возрастанию</SelectItem>
                    <SelectItem value="area-desc">Площадь: по убыванию</SelectItem>
                    <SelectItem value="floor">По этажу</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-gray-600">Найдено {displayedApartments.length} квартир</p>
              </div>
            </div>

            {displayedApartments.length > 0 ? (
              <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
                {displayedApartments.map((apartment) => (
                  <ApartmentCard key={apartment.id} apartment={apartment} />
                ))}
              </div>
            ) : (
              <div className="text-center py-16 bg-white rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold">Ничего не найдено</h3>
                <p className="text-gray-500 mt-2">Попробуйте изменить параметры фильтра или сбросить их.</p>
                <Button onClick={resetFilters} className="mt-4">
                  Сбросить фильтры
                </Button>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}

export default function RealEstatesPage({ params }: { params: { id: string } }) {
  return (
    <Suspense fallback={<div>Загрузка квартир...</div>}>
      <RealEstatesContent params={params} />
    </Suspense>
  )
}

function ApartmentFilterContent({
  priceRange,
  setPriceRange,
  selectedRooms,
  handleRoomsChange,
  selectedFloors,
  handleFloorsChange,
  selectedAreas,
  handleAreasChange,
  selectedPromotions,
  handlePromotionChange,
  resetFilters,
}: any) {
  const roomOptions = ["0", "1", "2", "3", "4+"]
  const floorOptions = ["1-5", "6-10", "11-15", "16+"]
  const areaOptions = ["до 40", "40-60", "60-80", "80+"]
  const promotionOptions = ["Скидка 5%", "Скидка 10%", "Ипотека 0.1%", "Паркинг в подарок"]

  return (
    <div className="space-y-6 py-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Цена: {priceRange[0].toLocaleString()} - {priceRange[1].toLocaleString()} ₽
        </label>
        <Slider
          value={priceRange}
          onValueChange={(value: [number, number]) => setPriceRange(value)}
          max={30000000}
          min={1000000}
          step={100000}
          className="w-full"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Количество комнат</label>
        <div className="space-y-2">
          {roomOptions.map((rooms) => (
            <div key={rooms} className="flex items-center space-x-2">
              <Checkbox
                id={`rooms-${rooms}`}
                checked={selectedRooms.includes(rooms)}
                onCheckedChange={() => handleRoomsChange(rooms)}
              />
              <label
                htmlFor={`rooms-${rooms}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {rooms === "0" ? "Студия" : `${rooms} комн.`}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Этаж</label>
        <div className="space-y-2">
          {floorOptions.map((floor) => (
            <div key={floor} className="flex items-center space-x-2">
              <Checkbox
                id={`floor-${floor}`}
                checked={selectedFloors.includes(floor)}
                onCheckedChange={() => handleFloorsChange(floor)}
              />
              <label
                htmlFor={`floor-${floor}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {floor} этаж
              </label>
            </div>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Площадь (м²)</label>
        <div className="space-y-2">
          {areaOptions.map((area) => (
            <div key={area} className="flex items-center space-x-2">
              <Checkbox
                id={`area-${area}`}
                checked={selectedAreas.includes(area)}
                onCheckedChange={() => handleAreasChange(area)}
              />
              <label
                htmlFor={`area-${area}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {area} м²
              </label>
            </div>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Акции и скидки</label>
        <div className="space-y-2">
          {promotionOptions.map((promo) => (
            <div key={promo} className="flex items-center space-x-2">
              <Checkbox
                id={`promo-${promo}`}
                checked={selectedPromotions.includes(promo)}
                onCheckedChange={() => handlePromotionChange(promo)}
              />
              <label
                htmlFor={`promo-${promo}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {promo}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-4 border-t">
        <Button variant="outline" className="w-full bg-transparent" onClick={resetFilters}>
          Сбросить все фильтры
        </Button>
      </div>
    </div>
  )
}
