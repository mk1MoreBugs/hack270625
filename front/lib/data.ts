import type React from "react"
import {
  Users,
  Home,
  DollarSign,
  Building,
  Heart,
  FileText,
  ShieldCheck,
  UserCheck,
  Gavel,
  BarChart2,
  Eye,
  Star,
} from "lucide-react"
import type { Project, Lead, StatCard, FilterOptions, UserRole, Apartment, Review } from "./types"

/* ---------------- دستیار صوتی هوشمن  --------------------------- */
export const homeStats = [
  { label: "Проверенных застройщиков", value: "16", icon: Building },
  { label: "Активных проектов", value: "500+", icon: Home },
  { label: "Довольных покупателей", value: "12 000+", icon: Users },
  { label: "Экономия на комиссии", value: "до 6%", icon: Star },
] satisfies { label: string; value: string; icon: React.ComponentType<any> }[]

export const filterOptions: FilterOptions = {
  cities: ["Краснодар", "Сочи", "Новороссийск", "Анапа"],
  classes: ["Эконом", "Комфорт", "Бизнес", "Элит"],
  completion: ["Сдан", "2024", "2025", "2026"],
  features: ["Паркинг", "Детская площадка", "Закрытая территория", "Рядом с парком"],
  promotions: ["Скидка 10%", "Паркинг в подарок", "Ипотека 0.1%"],
}

// Массив изображений ЖК для использования в проектах и ИИ-генерации
export const buildingImages = [
  "/images/building-1.jpeg",
  "/images/building-2.jpeg",
  "/images/building-3.jpeg",
  "/images/building-4.jpeg",
  "/images/building-5.jpeg",
  "/images/building-6.jpeg",
  "/images/building-7.jpeg",
  "/images/building-8.jpeg",
  "/images/building-9.jpeg",
]

// Функция для получения случайного изображения ЖК
export const getRandomBuildingImage = () => {
  return buildingImages[Math.floor(Math.random() * buildingImages.length)]
}

// Функция для получения 3 случайных изображений ЖК
export const getRandomBuildingImages = (count = 3) => {
  const shuffled = [...buildingImages].sort(() => 0.5 - Math.random())
  return shuffled.slice(0, count)
}

export const projectsData: Project[] = [
  {
    id: "1",
    name: "ЖК Солнечный Берег",
    developer: "ЮгСтройИмпериал",
    location: "Краснодар, р-н Гидростроителей",
    price: "от 4.8М ₽",
    class: "Комфорт",
    completion: "2025",
    image: buildingImages[0],
    images: [buildingImages[0], buildingImages[1], buildingImages[2]],
    rating: 4.9,
    reviews: 124,
    features: ["Паркинг", "Детская площадка", "Рядом с парком"],
    status: "Активный",
    totalApartments: 500,
    sold: 250,
    available: 250,
    revenue: "1.25 млрд ₽",
    leads: 120,
    isFavorite: true,
    promotion: "Ипотека 0.1%",
  },
  {
    id: "2",
    name: "ЖК Зеленый Квартал",
    developer: "Setl Group",
    location: "Санкт-Петербург, Московский р-н",
    price: "от 6.2М ₽",
    class: "Бизнес",
    completion: "Сдан",
    image: buildingImages[3],
    images: [buildingImages[3], buildingImages[4]],
    rating: 4.7,
    reviews: 88,
    features: ["Паркинг", "Закрытая территория"],
    status: "Активный",
    totalApartments: 300,
    sold: 280,
    available: 20,
    revenue: "1.7 млрд ₽",
    leads: 45,
    isFavorite: false,
    promotion: "Скидка 10%",
  },
  {
    id: "3",
    name: "ЖК Морская Симфония",
    developer: "Альпика Групп",
    location: "Сочи, Адлерский р-н",
    price: "от 12.5М ₽",
    class: "Элит",
    completion: "2024",
    image: buildingImages[5],
    images: [buildingImages[5], buildingImages[6]],
    rating: 4.9,
    reviews: 210,
    features: ["Паркинг", "Закрытая территория", "Рядом с парком"],
    status: "Завершен",
    totalApartments: 150,
    sold: 145,
    available: 5,
    revenue: "1.8 млрд ₽",
    leads: 30,
    isFavorite: true,
  },
  {
    id: "4",
    name: "ЖК Центральный",
    developer: "ССК",
    location: "Краснодар, Центральный р-н",
    price: "от 5.1М ₽",
    class: "Комфорт",
    completion: "2024",
    image: buildingImages[7],
    images: [buildingImages[7], buildingImages[8]],
    rating: 4.6,
    reviews: 150,
    features: ["Паркинг", "Детская площадка"],
    status: "Активный",
    totalApartments: 800,
    sold: 400,
    available: 400,
    revenue: "2 млрд ₽",
    leads: 250,
    isFavorite: false,
    promotion: "Паркинг в подарок",
  },
]

export const recommendedApartmentsData: Apartment[] = [
  {
    id: "1-a2", // Изменено с "a1" на "1-a2"
    name: "2-комнатная",
    project: "ЖК Солнечный Берег",
    area: 65,
    price: "5.2 млн ₽",
    image: buildingImages[0],
    promotion: "Ипотека 0.1%",
    tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
    rooms: 2,
    floor: 8,
  },
  {
    id: "1-a1", // Изменено с "a2" на "1-a1"
    name: "Студия",
    project: "ЖК Зеленый Квартал",
    area: 28,
    price: "6.2 млн ₽",
    image: buildingImages[3],
    promotion: "Скидка 10%",
    tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
    rooms: 0,
    floor: 5,
  },
  {
    id: "1-a3", // Изменено с "a3" на "1-a3"
    name: "1-комнатная",
    project: "ЖК Центральный",
    area: 42,
    price: "5.5 млн ₽",
    image: buildingImages[7],
    promotion: "Паркинг в подарок",
    tourUrl: "https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default",
    rooms: 1,
    floor: 12,
  },
]

export const leadsData: Lead[] = [
  {
    id: "1",
    name: "Иван Петров",
    phone: "+7 (918) 123-45-67",
    email: "ivan.p@example.com",
    project: "ЖК Солнечный Берег",
    apartment: "2-комнатная, 65м²",
    status: "Новая",
    date: "2024-07-21",
  },
  {
    id: "2",
    name: "Елена Сидорова",
    phone: "+7 (928) 765-43-21",
    email: "elena.s@example.com",
    project: "ЖК Центральный",
    apartment: "Студия, 28м²",
    status: "В работе",
    date: "2024-07-20",
  },
  {
    id: "3",
    name: "Сергей Иванов",
    phone: "+7 (999) 555-12-34",
    email: "sergey.i@example.com",
    project: "ЖК Зеленый Квартал",
    apartment: "3-комнатная, 88м²",
    status: "Закрыта",
    date: "2024-07-19",
  },
]

export const reviewsData: Review[] = [
  {
    id: "1",
    author: "Алексей Смирнов",
    rating: 5,
    date: "2024-07-15",
    text: "Отличная платформа! Нашли квартиру мечты без риелторов и скрытых комиссий. Все прозрачно и понятно. Рекомендую!",
    avatar: "/placeholder.svg?height=48&width=48",
  },
  {
    id: "2",
    author: "Ольга Кузнецова",
    rating: 5,
    date: "2024-07-12",
    text: "ИИ-подбор — это просто магия! Сэкономила кучу времени, система предложила варианты, о которых я даже не думала. Спасибо!",
    avatar: "/placeholder.svg?height=48&width=48",
  },
]

export const dashboardStats: Record<UserRole, StatCard[]> = {
  developer: [
    { label: "Активных проектов", value: "5", icon: Building, change: "+1" },
    { label: "Новых заявок", value: "28", icon: Users, change: "+15%" },
    { label: "Продаж за месяц", value: "12", icon: Home, change: "+8%" },
    { label: "Выручка", value: "72.4М ₽", icon: DollarSign, change: "+12%" },
  ],
  buyer: [
    { label: "В избранном", value: "8", icon: Heart },
    { label: "Мои заявки", value: "3", icon: FileText },
    { label: "Просмотрено", value: "25", icon: Eye },
    { label: "Рекомендаций", value: "12", icon: UserCheck },
  ],
  admin: [
    { label: "Всего застройщиков", value: "32", icon: Building },
    { label: "На модерации", value: "3", icon: ShieldCheck },
    { label: "Жалобы", value: "1", icon: Gavel },
    { label: "Общий оборот", value: "1.8Б ₽", icon: BarChart2 },
  ],
}
