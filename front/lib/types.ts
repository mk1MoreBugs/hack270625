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
  gallery?: string[]
  progress?: {
    [key: string]: number
  }
  status?: string
}

export interface ApiProject {
  id: number
  name: string
  address: string
  developer_id: number
  developer_name: string
  building_class: string
  completion_date: string
  min_price: number
  rating: number
  total_apartments: number
  image_url: string | null
  description: string
  latitude: number
  longitude: number
  status: string
  created_at: string
  updated_at: string
}

export interface FilterOptions {
  regions: string[]
  classes: string[]
  completion: string[]
  status: string[]
}

export const mapApiProjectToProject = (apiProject: ApiProject): Project => ({
  id: apiProject.id.toString(),
  name: apiProject.name,
  location: apiProject.address,
  developer: apiProject.developer_name,
  class: apiProject.building_class,
  completion: new Date(apiProject.completion_date).toLocaleDateString('ru-RU'),
  price: `от ${apiProject.min_price.toLocaleString('ru-RU')} ₽`,
  rating: apiProject.rating,
  totalApartments: apiProject.total_apartments,
  image: apiProject.image_url || '/placeholder.svg',
  description: apiProject.description,
  status: apiProject.status
})

export interface Review {
  id: string;
  author: string;
  text: string;
  rating: number;
  date: string;
  avatar?: string;
}

export interface ApiReview {
  id: number;
  author_name: string;
  text: string;
  rating: number;
  created_at: string;
  avatar_url?: string;
}

export const mapApiReviewToReview = (apiReview: ApiReview): Review => ({
  id: apiReview.id.toString(),
  author: apiReview.author_name,
  text: apiReview.text,
  rating: apiReview.rating,
  date: new Date(apiReview.created_at).toLocaleDateString('ru-RU'),
  avatar: apiReview.avatar_url
});
