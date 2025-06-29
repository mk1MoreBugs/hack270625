import type React from "react"

export interface Project {
  id: string
  name: string
  location: string
  developer: string
  class: string
  completion: string
  price: string
  rating: number
  totalApartments: number
  image?: string
  images?: string[]
  discount?: string
  description?: string
  features?: string[]
  status?: string
  sold?: number
  available?: number
  revenue?: string
  leads?: number
  isFavorite?: boolean
  promotion?: string
  progress?: {
    foundation: number
    walls: number
    roof: number
    finishing: number
  }
}

export interface Apartment {
  id: string
  name: string
  project: string
  area: number
  price: string
  image: string
  promotion: string
  tourUrl: string
  rooms?: number
  floor?: number
  priceNum?: number
  projectId?: string
  description?: string
  features?: string[]
  developer?: string
  completion?: string
  class?: string
  // Новые поля в соответствии с API
  number?: string
  area_total?: number
  area_living?: number
  area_kitchen?: number
  base_price?: number
  current_price?: number
  balcony?: boolean
  loggia?: boolean
  parking?: boolean
  layout_image_url?: string | null
  building_id?: number
  status?: "available" | "sold" | "reserved"
  created_at?: string
  updated_at?: string
}

export interface Lead {
  id: string
  name: string
  phone: string
  email: string
  project: string
  apartment: string
  status: "Новая" | "В работе" | "Закрыта"
  date: string
  source?: string
  client?: string
}

export interface Review {
  id: string
  author: string
  rating: number
  date: string
  text: string
  avatar?: string
}

export interface StatCard {
  label: string
  value: string
  icon: React.ComponentType<any>
  change?: string
}

export type UserRole = "developer" | "buyer" | "admin"

export interface FilterOptions {
  cities: string[]
  classes: string[]
  completion: string[]
  features: string[]
  promotions: string[]
}
