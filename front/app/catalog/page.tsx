"use client"

import type React from "react"
import { Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { useState, useMemo } from "react"
import { Filter, ArrowUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Checkbox } from "@/components/ui/checkbox"
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { filterOptions } from "@/lib/data"
import { ProjectCard } from "@/components/projects/ProjectCard"
import { useProjects } from "@/lib/api-hooks"
import { mapApiProjectToProject, type Project } from "@/lib/types"

function CatalogContent() {
  const searchParams = useSearchParams()
  const { data: apiProjects, error } = useProjects()

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
  const [selectedStatus, setSelectedStatus] = useState<string[]>(
    searchParams.get("status") ? [searchParams.get("status")!] : [],
  )
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
    setSelectedStatus([])
    setSortBy("price-asc")
  }

  const displayedProjects = useMemo(() => {
    if (!apiProjects) return []
    
    let filtered = apiProjects.map(mapApiProjectToProject)

    if (searchQuery) {
      const lowercasedQuery = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (p: Project) =>
          p.name.toLowerCase().includes(lowercasedQuery) ||
          p.developer.toLowerCase().includes(lowercasedQuery) ||
          p.location.toLowerCase().includes(lowercasedQuery),
      )
    }

    filtered = filtered.filter((p: Project) => {
      const price = parseInt(p.price.replace(/[^\d]/g, ''))
      return price >= priceRange[0] && price <= priceRange[1]
    })

    if (selectedRegion !== "all") {
      filtered = filtered.filter((p: Project) => p.location.includes(selectedRegion))
    }

    if (selectedClasses.length > 0) {
      filtered = filtered.filter((p: Project) => selectedClasses.includes(p.class))
    }

    if (selectedCompletion.length > 0) {
      filtered = filtered.filter((p: Project) => selectedCompletion.includes(p.completion))
    }

    if (selectedStatus.length > 0) {
      filtered = filtered.filter((p: Project) => p.status && selectedStatus.includes(p.status))
    }

    switch (sortBy) {
      case "price-asc":
        filtered.sort((a: Project, b: Project) => parseInt(a.price.replace(/[^\d]/g, '')) - parseInt(b.price.replace(/[^\d]/g, '')))
        break
      case "price-desc":
        filtered.sort((a: Project, b: Project) => parseInt(b.price.replace(/[^\d]/g, '')) - parseInt(a.price.replace(/[^\d]/g, '')))
        break
      case "rating":
        filtered.sort((a: Project, b: Project) => (b.rating || 0) - (a.rating || 0))
        break
      case "completion":
        filtered.sort((a: Project, b: Project) => a.completion.localeCompare(b.completion))
        break
    }

    return filtered
  }, [
    apiProjects,
    searchQuery,
    priceRange,
    selectedRegion,
    selectedClasses,
    selectedCompletion,
    selectedStatus,
    sortBy,
  ])

  if (error) {
    return <div className="text-center text-red-500">Ошибка загрузки данных</div>
  }

  if (!apiProjects) {
    return <div className="text-center">Загрузка...</div>
  }

  const filterContentProps = {
    priceRange,
    setPriceRange,
    selectedRegion,
    setSelectedRegion,
    selectedClasses,
    handleClassChange: (value: string) => handleCheckboxChange(setSelectedClasses, value),
    selectedCompletion,
    handleCompletionChange: (value: string) => handleCheckboxChange(setSelectedCompletion, value),
    selectedStatus,
    handleStatusChange: (value: string) => handleCheckboxChange(setSelectedStatus, value),
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
                  <div className="mt-6">
                    <FilterContent {...filterContentProps} />
                  </div>
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
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {displayedProjects.map((project: Project) => (
                  <ProjectCard key={project.id} project={project} />
                ))}
                {displayedProjects.length === 0 && (
                  <div className="col-span-full text-center text-gray-500">
                    Ничего не найдено. Попробуйте изменить параметры поиска.
                  </div>
                )}
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
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
  selectedStatus,
  handleStatusChange,
  resetFilters,
}: any) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="font-medium mb-4">Цена</h3>
        <div className="space-y-4">
          <div className="flex justify-between">
            <span>{priceRange[0].toLocaleString('ru-RU')} ₽</span>
            <span>{priceRange[1].toLocaleString('ru-RU')} ₽</span>
          </div>
          <Slider
            value={priceRange}
            min={1000000}
            max={30000000}
            step={100000}
            onValueChange={setPriceRange}
          />
        </div>
      </div>

      <div>
        <h3 className="font-medium mb-4">Район</h3>
        <Select value={selectedRegion} onValueChange={setSelectedRegion}>
          <SelectTrigger>
            <SelectValue placeholder="Выберите район" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Все районы</SelectItem>
            {filterOptions.regions.map((region) => (
              <SelectItem key={region} value={region}>
                {region}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <h3 className="font-medium mb-4">Класс жилья</h3>
        <div className="space-y-2">
          {filterOptions.classes.map((cls) => (
            <div key={cls} className="flex items-center">
              <Checkbox
                id={`class-${cls}`}
                checked={selectedClasses.includes(cls)}
                onCheckedChange={() => handleClassChange(cls)}
              />
              <label htmlFor={`class-${cls}`} className="ml-2 text-sm">
                {cls}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="font-medium mb-4">Срок сдачи</h3>
        <div className="space-y-2">
          {filterOptions.completion.map((year) => (
            <div key={year} className="flex items-center">
              <Checkbox
                id={`completion-${year}`}
                checked={selectedCompletion.includes(year)}
                onCheckedChange={() => handleCompletionChange(year)}
              />
              <label htmlFor={`completion-${year}`} className="ml-2 text-sm">
                {year}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="font-medium mb-4">Статус</h3>
        <div className="space-y-2">
          {filterOptions.status.map((status) => (
            <div key={status} className="flex items-center">
              <Checkbox
                id={`status-${status}`}
                checked={selectedStatus.includes(status)}
                onCheckedChange={() => handleStatusChange(status)}
              />
              <label htmlFor={`status-${status}`} className="ml-2 text-sm">
                {status}
              </label>
            </div>
          ))}
        </div>
      </div>

      <Button variant="outline" className="w-full" onClick={resetFilters}>
        Сбросить фильтры
      </Button>
    </div>
  )
}

export default function CatalogPage() {
  return (
    <Suspense fallback={<div>Загрузка...</div>}>
      <CatalogContent />
    </Suspense>
  )
}
