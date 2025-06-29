// Типы данных для мобильного приложения
export interface Project {
  id: string
  name: string
  developer: string
  location: string
  price: string
  class: string
  completion: string
  image: string
  images: string[]
  rating: number
  reviews: number
  features: string[]
  status: string
  totalApartments: number
  sold: number
  available: number
  revenue: string
  leads: number
  isFavorite: boolean
  promotion: string
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
  rooms: number
  floor: number
}

export interface User {
  id: string
  name: string
  email: string
  avatar: string
}

export interface Property {
  $id: string
  name: string
  type: string
  description: string
  address: string
  price: number
  area: number
  bedrooms: number
  bathrooms: number
  rating: number
  facilities: string[]
  image: string
  agent: string
  reviews: string[]
  gallery: string[]
  geolocation: string
}

export interface Review {
  id: string
  author: string
  rating: number
  date: string
  text: string
  avatar: string
}

export interface FilterOptions {
  cities: string[]
  classes: string[]
  completion: string[]
  features: string[]
  promotions: string[]
} 