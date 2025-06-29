"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"

export function HeroSection() {
  const router = useRouter()
  const [priceRange, setPriceRange] = useState([2000000, 15000000])
  const [selectedRegion, setSelectedRegion] = useState("")
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedClass, setSelectedClass] = useState("")
  const [selectedCompletion, setSelectedCompletion] = useState("")

  const handleSearch = () => {
    const params = new URLSearchParams()
    if (searchQuery) {
      params.set("q", searchQuery)
    }
    if (selectedRegion) {
      params.set("region", selectedRegion)
    }
    if (selectedClass) {
      params.set("class", selectedClass)
    }
    if (selectedCompletion) {
      params.set("completion", selectedCompletion)
    }
    params.set("minPrice", priceRange[0].toString())
    params.set("maxPrice", priceRange[1].toString())

    router.push(`/catalog?${params.toString()}`)
  }

  return (
    <section className="py-20 px-4">
      <div className="container mx-auto text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          Покупайте квартиры
          <span className="text-blue-600 block">напрямую от застройщиков</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Без посредников, с гарантиями и лучшими ценами. Более 500 проектов от проверенных застройщиков по всей России.
        </p>

        <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-6">
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
                <SelectValue placeholder="Город" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Москва">Москва</SelectItem>
                <SelectItem value="Санкт-Петербург">Санкт-Петербург</SelectItem>
                <SelectItem value="Екатеринбург">Екатеринбург</SelectItem>
                <SelectItem value="Казань">Казань</SelectItem>
              </SelectContent>
            </Select>
            <Button size="lg" className="h-12" onClick={handleSearch}>
              <Search className="w-5 h-5 mr-2" />
              Найти
            </Button>
          </div>

          <div className="mt-6 pt-6 border-t">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
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
              <Select value={selectedClass} onValueChange={setSelectedClass}>
                <SelectTrigger>
                  <SelectValue placeholder="Класс жилья" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Эконом">Эконом</SelectItem>
                  <SelectItem value="Комфорт">Комфорт</SelectItem>
                  <SelectItem value="Бизнес">Бизнес</SelectItem>
                  <SelectItem value="Элитный">Элитный</SelectItem>
                </SelectContent>
              </Select>
              <Select value={selectedCompletion} onValueChange={setSelectedCompletion}>
                <SelectTrigger>
                  <SelectValue placeholder="Срок сдачи" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Сдан">Сдан</SelectItem>
                  <SelectItem value="2024">2024</SelectItem>
                  <SelectItem value="2025">2025</SelectItem>
                  <SelectItem value="2026">2026</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
