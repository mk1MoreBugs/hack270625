import type { Project, Apartment, Property, Review } from "./types"

// Изображения зданий (локальные)
export const buildingImages = [
  "https://images.unsplash.com/photo-1560185009-dddeb820c7b7?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1605146768851-eda79da39897?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1568605114967-8130f3a36994?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1561753757-d8880c5a3551?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1551241090-67de81d3541c?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1697299262049-e9b5fa1e9761?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  "https://images.unsplash.com/photo-1720432972486-2d53db5badf0?q=60&w=640&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
]

// Проекты ЖК
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
    promotion: "",
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

// Рекомендуемые квартиры
export const recommendedApartmentsData: Apartment[] = [
  {
    id: "1-a2",
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
    id: "1-a1",
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
    id: "1-a3",
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

// Конвертация проектов в формат Property для совместимости
export const propertiesData: Property[] = projectsData.map((project, index) => ({
  $id: project.id,
  name: project.name,
  type: project.class,
  description: `Современный ЖК ${project.name} от застройщика ${project.developer}`,
  address: project.location,
  price: parseInt(project.price.replace(/[^\d]/g, '')) * 1000 || 5000000,
  area: 65 + index * 10,
  bedrooms: Math.floor(Math.random() * 3) + 1,
  bathrooms: Math.floor(Math.random() * 2) + 1,
  rating: project.rating,
  facilities: project.features,
  image: project.image,
  agent: `agent-${index + 1}`,
  reviews: [`review-${index + 1}`, `review-${index + 2}`],
  gallery: project.images,
  geolocation: `55.${753000 + index * 1000}, 37.${622000 + index * 1000}`,
}))

export const reviewsData: Review[] = [
  {
    id: "1",
    author: "Алексей Смирнов",
    rating: 5,
    date: "2024-07-15",
    text: "Отличная платформа! Нашли квартиру мечты без риелторов и скрытых комиссий. Все прозрачно и понятно. Рекомендую!",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
  },
  {
    id: "2",
    author: "Ольга Кузнецова",
    rating: 5,
    date: "2024-07-12",
    text: "ИИ-подбор — это просто магия! Сэкономила кучу времени, система предложила варианты, о которых я даже не думала. Спасибо!",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b332b8d4?w=150&h=150&fit=crop&crop=face",
  },
]

// Изображения для галереи
export const galleryImages = buildingImages

// Агенты (для совместимости)
export const agentImages = [
  "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1494790108755-2616b332b8d4?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
]

export const reviewImages = [
  "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1494790108755-2616b332b8d4?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
  "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
]

export const propertiesImages = buildingImages

// Функция для получения случайного изображения ЖК
export const getRandomBuildingImage = () => {
  return buildingImages[Math.floor(Math.random() * buildingImages.length)]
}

// Функция для получения 3 случайных изображений ЖК
export const getRandomBuildingImages = (count = 3) => {
  const shuffled = [...buildingImages].sort(() => 0.5 - Math.random())
  return shuffled.slice(0, count)
}
