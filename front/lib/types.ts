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
  image: string
  discount?: string
  description?: string
  features?: string[]
}
