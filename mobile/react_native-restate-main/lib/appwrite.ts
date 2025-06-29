// Локальные данные вместо AppWrite
import { propertiesData, reviewsData, agentImages } from "./data"
import type { Property, User } from "./types"

// Мок пользователя
const mockUser: User = {
  id: "user-1",
  name: "Анна Иванова",
  email: "anna.ivanova@example.com",
  avatar: "https://images.unsplash.com/photo-1494790108755-2616b332b8d4?w=150&h=150&fit=crop&crop=face",
}

// Упрощенная функция входа - просто возвращает успех
export async function login(): Promise<boolean> {
  try {
    // Имитируем задержку для UX
    await new Promise(resolve => setTimeout(resolve, 1000))
    return true
  } catch (error) {
    console.error("Ошибка входа:", error)
    return false
  }
}

// Функция выхода - просто возвращает true
export async function logout(): Promise<boolean> {
  try {
    return true
  } catch (error) {
    console.error("Ошибка выхода:", error)
    return false
  }
}

// Получение текущего пользователя
export async function getCurrentUser(): Promise<User | null> {
  try {
    // Имитируем задержку
    await new Promise(resolve => setTimeout(resolve, 500))
    return mockUser
  } catch (error) {
    console.error("Ошибка получения пользователя:", error)
    return null
  }
}

// Получение последних объектов недвижимости
export async function getLatestProperties(): Promise<Property[]> {
  try {
    // Имитируем задержку
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // Возвращаем первые 5 объектов как "последние"
    return propertiesData.slice(0, 5)
  } catch (error) {
    console.error("Ошибка получения последних объектов:", error)
    return []
  }
}

// Получение объектов недвижимости с фильтрацией
export async function getProperties({
  filter,
  query,
  limit,
}: {
  filter?: string
  query?: string
  limit?: number
}): Promise<Property[]> {
  try {
    // Имитируем задержку
    await new Promise(resolve => setTimeout(resolve, 600))
    
    let filteredProperties = [...propertiesData]
    
    // Фильтрация по типу
    if (filter && filter !== "All" && filter !== "Все") {
      filteredProperties = filteredProperties.filter(property => 
        property.type.toLowerCase().includes(filter.toLowerCase())
      )
    }
    
    // Поиск по названию и адресу
    if (query && query.trim()) {
      const searchQuery = query.toLowerCase().trim()
      filteredProperties = filteredProperties.filter(property =>
        property.name.toLowerCase().includes(searchQuery) ||
        property.address.toLowerCase().includes(searchQuery) ||
        property.type.toLowerCase().includes(searchQuery)
      )
    }
    
    // Ограничение количества результатов
    if (limit && limit > 0) {
      filteredProperties = filteredProperties.slice(0, limit)
    }
    
    return filteredProperties
  } catch (error) {
    console.error("Ошибка получения объектов:", error)
    return []
  }
}

// Получение объекта недвижимости по ID
export async function getPropertyById({ id }: { id: string }): Promise<Property | null> {
  try {
    // Имитируем задержку
    await new Promise(resolve => setTimeout(resolve, 400))
    
    const property = propertiesData.find(p => p.$id === id)
    return property || null
  } catch (error) {
    console.error("Ошибка получения объекта по ID:", error)
    return null
  }
}

// Экспорт конфигурации (для совместимости)
export const config = {
  platform: "com.realestate.app",
  endpoint: "local",
  projectId: "local-project",
  databaseId: "local-db",
}
