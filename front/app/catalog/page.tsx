"use client"

import type React from "react"
import { Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { useState, useMemo, useEffect } from "react"
import { Filter, ArrowUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Checkbox } from "@/components/ui/checkbox"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { projectsData, filterOptions } from "@/lib/data"
import { ProjectCard } from "@/components/projects/ProjectCard"

function CatalogContent() {
  const searchParams = useSearchParams()

  const [searchQuery, setSearchQuery] = useState(searchParams.get("q") || "")
  const [priceRange, setPriceRange] = useState<[number, number]>([
    Number(searchParams.get("minPrice")) || 1000000,
    Number(searchParams.get("maxPrice")) || 30000000,
  ])
  const [selectedRegion, setSelectedRegion] = useState(searchParams.get("region") || "all")
  const [selectedClasses, setSelectedClasses] = useState<string[]>(
    searchParams.get("class") ? [searchParams.get("class")!] : [],
  )
  const [selectedCompletion, setSelectedCompletion] = useState<string[]>(
    searchParams.get("completion") ? [searchParams.get("completion")!] : [],
  )
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([])
  const [selectedPromotions, setSelectedPromotions] = useState<string[]>([])

  useEffect(() => {
    if (searchParams.get("promo") === "true") {
      setSelectedPromotions(filterOptions.promotions)
    }
  }, [searchParams])

  const [sortBy, setSortBy] = useState("price-asc")

  const handleCheckboxChange = (setter: React.Dispatch<React.SetStateAction<string[]>>, value: string) => {
    setter((prev) => (prev.includes(value) ? prev.filter((item) => item !== value) : [...prev, value]))
  }

  const resetFilters = () => {
    setSearchQuery("")
    setPriceRange([1000000, 30000000])
    setSelectedRegion("all")
    setSelectedClasses([])
    setSelectedCompletion([])
    setSelectedFeatures([])
    setSelectedPromotions([])
    setSortBy("price-asc")
  }

  const displayedProjects = useMemo(() => {
    let filtered = [...projectsData]

    if (searchQuery) {
      const lowercasedQuery = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (p) =>
          p.name.toLowerCase().includes(lowercasedQuery) ||
          p.developer.toLowerCase().includes(lowercasedQuery) ||
          p.location.toLowerCase().includes(lowercasedQuery),
      )
    }

    const numericPrice = (priceStr: string): number => {
      const priceMatch = priceStr.match(/(\d+([.,]\d+)?)/)
      if (!priceMatch) return 0
      const price = Number.parseFloat(priceMatch[0].replace(",", ".")) * 1000000
      return price
    }

    filtered = filtered.filter((p) => {
      const price = numericPrice(p.price)
      return price >= priceRange[0] && price <= priceRange[1]
    })

    if (selectedRegion !== "all") {
      filtered = filtered.filter((p) => p.location.includes(selectedRegion))
    }

    if (selectedClasses.length > 0) {
      filtered = filtered.filter((p) => selectedClasses.includes(p.class))
    }

    if (selectedCompletion.length > 0) {
      filtered = filtered.filter((p) => selectedCompletion.includes(p.completion))
    }

    if (selectedFeatures.length > 0) {
      filtered = filtered.filter((p) => p.features?.some((feature) => selectedFeatures.includes(feature)))
    }

    if (selectedPromotions.length > 0) {
      filtered = filtered.filter((p) => p.promotion && selectedPromotions.includes(p.promotion))
    }

    switch (sortBy) {
      case "price-asc":
        filtered.sort((a, b) => numericPrice(a.price) - numericPrice(b.price))
        break
      case "price-desc":
        filtered.sort((a, b) => numericPrice(b.price) - numericPrice(a.price))
        break
      case "rating":
        filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0))
        break
      case "completion":
        filtered.sort((a, b) => a.completion.localeCompare(b.completion))
        break
    }

    return filtered
  }, [
    searchQuery,
    priceRange,
    selectedRegion,
    selectedClasses,
    selectedCompletion,
    selectedFeatures,
    selectedPromotions,
    sortBy,
  ])

  const filterContentProps = {
    priceRange,
    setPriceRange,
    selectedRegion,
    setSelectedRegion,
    selectedClasses,
    handleClassChange: (value: string) => handleCheckboxChange(setSelectedClasses, value),
    selectedCompletion,
    handleCompletionChange: (value: string) => handleCheckboxChange(setSelectedCompletion, value),
    selectedFeatures,
    handleFeatureChange: (value: string) => handleCheckboxChange(setSelectedFeatures, value),
    selectedPromotions,
    handlePromotionChange: (value: string) => handleCheckboxChange(setSelectedPromotions, value),
    resetFilters,
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
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
                    <SheetDescription>Настройте параметры для поиска идеального жилья</SheetDescription>
                  </SheetHeader>
                  <FilterContent {...filterContentProps} />
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
                  <FilterContent {...filterContentProps} />
                </CardContent>
              </Card>
            </div>
          </aside>

          <main className="flex-1">
            <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
              <div className="flex flex-col md:flex-row gap-4 mb-4">
                <div className="flex-1">
                  <Input
                    placeholder="Поиск по названию, застройщику или району..."
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
                    <SelectItem value="rating">По рейтингу</SelectItem>
                    <SelectItem value="completion">По сроку сдачи</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-gray-600">Найдено {displayedProjects.length} проектов</p>
              </div>
            </div>

            {displayedProjects.length > 0 ? (
              <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
                {displayedProjects.map((project) => (
                  <ProjectCard key={project.id} project={project} />
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

export default function CatalogPage() {
  return (
    <Suspense fallback={<div>Загрузка каталога...</div>}>
      <CatalogContent />
    </Suspense>
  )
}

function FilterContent({
  priceRange,
  setPriceRange,
  selectedRegion,
  setSelectedRegion,
  selectedClasses,
  handleClassChange,
  selectedCompletion,
  handleCompletionChange,
  selectedFeatures,
  handleFeatureChange,
  selectedPromotions,
  handlePromotionChange,
  resetFilters,
}: any) {
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
        <label className="block text-sm font-medium text-gray-700 mb-3">Акции и скидки</label>
        <div className="space-y-2">
          {filterOptions.promotions.map((promo) => (
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
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Регион</label>
        <Select value={selectedRegion} onValueChange={setSelectedRegion}>
          <SelectTrigger>
            <SelectValue placeholder="Выберите регион" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Все регионы</SelectItem>
            {filterOptions.regions.map((region) => (
              <SelectItem key={region} value={region}>
                {region}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Класс жилья</label>
        <div className="space-y-2">
          {filterOptions.classes.map((cls) => (
            <div key={cls} className="flex items-center space-x-2">
              <Checkbox
                id={`class-${cls}`}
                checked={selectedClasses.includes(cls)}
                onCheckedChange={() => handleClassChange(cls)}
              />
              <label
                htmlFor={`class-${cls}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {cls}
              </label>
            </div>
          ))}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Срок сдачи</label>
        <div className="space-y-2">
          {filterOptions.completion.map((year) => (
            <div key={year} className="flex items-center space-x-2">
              <Checkbox
                id={`completion-${year}`}
                checked={selectedCompletion.includes(year)}
                onCheckedChange={() => handleCompletionChange(year)}
              />
              <label
                htmlFor={`completion-${year}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {year}
              </label>
            </div>
          ))}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">Удобства</label>
        <div className="space-y-2">
          {filterOptions.features.map((feature) => (
            <div key={feature} className="flex items-center space-x-2">
              <Checkbox
                id={`feature-${feature}`}
                checked={selectedFeatures.includes(feature)}
                onCheckedChange={() => handleFeatureChange(feature)}
              />
              <label
                htmlFor={`feature-${feature}`}
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                {feature}
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
