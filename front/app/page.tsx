"use client"

import { useState } from "react"
import { Star, Home, Users, TrendingUp } from "lucide-react"
import { HeroSection } from "@/components/home/HeroSection"
import { StatsSection } from "@/components/home/StatsSection"
import { FeaturedProjects } from "@/components/home/FeaturedProjects"
import { MapPlaceholder } from "@/components/home/MapPlaceholder"
import { BenefitsSection } from "@/components/home/BenefitsSection"

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
      {/* Hero Section */}
      <HeroSection />

      {/* Stats */}
      <StatsSection />

      {/* Featured Projects */}
      <FeaturedProjects />

      {/* Interactive Map Section */}
      <MapPlaceholder />

      {/* Benefits Section */}
      <BenefitsSection />
    </div>
  )
}
