import { getRandomBuildingImages } from "./data";
import type { Property } from "./types";

const MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions";
const API_KEY = "advGDYdUZoBHTx00nTL769K6AJ6IH0pv"; // Ваш API ключ

interface AISuggestion {
  address: string;
  description: string;
  price: number;
  area: number;
  rooms: number;
  floor: number;
  total_floors: number;
  year_built: number;
}

interface AIResponse {
  suggestions: AISuggestion[];
}

// Функция для проверки валидности запроса о недвижимости
function isValidRealEstateQuery(prompt: string): boolean {
  const lowercasePrompt = prompt.toLowerCase().trim();

  // Слишком короткие запросы
  if (lowercasePrompt.length < 5) {
    return false;
  }

  // Простые приветствия
  const greetings = ["привет", "hello", "hi", "здравствуйте", "добрый день", "добрый вечер", "доброе утро"];
  if (greetings.some((greeting) => lowercasePrompt === greeting)) {
    return false;
  }

  // Только цифры или символы
  if (/^\d+$/.test(lowercasePrompt) || /^[^\w\s]+$/.test(lowercasePrompt)) {
    return false;
  }

  // Проверяем наличие ключевых слов недвижимости
  const realEstateKeywords = [
    "квартира", "дом", "комната", "студия", "жилье", "недвижимость",
    "купить", "снять", "аренда", "продажа", "цена", "стоимость",
    "район", "город", "метро", "этаж", "площадь", "м2", "кв.м",
    "рубл", "₽", "млн", "тыс", "миллион", "тысяч",
    "москва", "спб", "санкт-петербург", "краснодар", "сочи"
  ];

  return realEstateKeywords.some((keyword) => lowercasePrompt.includes(keyword));
}

// Функция для получения ИИ-предложений через Mistral API
export async function getAISuggestions(query: string): Promise<Property[]> {
  try {
    // Проверяем валидность запроса
    if (!isValidRealEstateQuery(query)) {
      throw new Error("Пожалуйста, опишите ваши требования к недвижимости более подробно. Например: 'Двухкомнатная квартира в Краснодаре до 10 млн ₽'.");
    }

    const response = await fetch(MISTRAL_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        model: "mistral-large-latest",
        messages: [
          {
            role: "system",
            content: `Ты — ИИ-помощник по подбору недвижимости в России. 
            
ВАЖНО: Ты ОБЯЗАТЕЛЬНО должен вернуть JSON-объект в следующем формате:
{
  "suggestions": [
    {
      "address": "строка с адресом",
      "description": "описание квартиры",
      "price": число_в_рублях,
      "area": число_площади_в_м2,
      "rooms": количество_комнат,
      "floor": этаж,
      "total_floors": общее_количество_этажей,
      "year_built": год_постройки
    }
  ]
}

Всегда возвращай массив из 3 предложений. Используй реальные районы российских городов и адекватные цены для рынка недвижимости.`,
          },
          {
            role: "user",
            content: query,
          },
        ],
        response_format: { type: "json_object" },
        temperature: 0.7,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Ошибка API: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    const content = data.choices?.[0]?.message?.content ?? "{}";

    let parsedContent: AIResponse;
    try {
      parsedContent = JSON.parse(content);
    } catch (parseError) {
      throw new Error("ИИ вернул некорректный JSON");
    }

    // Проверяем структуру ответа
    if (!parsedContent || typeof parsedContent !== "object") {
      throw new Error("ИИ вернул некорректную структуру данных");
    }

    // Если ИИ вернул массив вместо объекта, оборачиваем его
    if (Array.isArray(parsedContent)) {
      parsedContent = { suggestions: parsedContent };
    }

    // Если нет поля suggestions, создаем ошибку
    if (!parsedContent.suggestions || !Array.isArray(parsedContent.suggestions)) {
      throw new Error("ИИ не смог подобрать подходящие варианты. Попробуйте уточнить ваш запрос.");
    }

    // Добавляем изображения и конвертируем в формат Property
    const randomImages = getRandomBuildingImages(3);
    const properties: Property[] = parsedContent.suggestions.map((suggestion, index) => ({
      $id: `ai-${Date.now()}-${index}`,
      name: `ЖК ${suggestion.address.split(",")[0]}`,
      type: suggestion.rooms === 0 ? "Студия" : suggestion.rooms <= 2 ? "Комфорт" : "Бизнес",
      description: suggestion.description,
      address: suggestion.address,
      price: suggestion.price,
      area: suggestion.area,
      bedrooms: suggestion.rooms,
      bathrooms: Math.max(1, Math.floor(suggestion.rooms / 2)),
      rating: 4.5 + Math.random() * 0.4, // Рейтинг 4.5-4.9
      facilities: getRandomFacilities(),
      image: randomImages[index] || randomImages[0],
      agent: `agent-ai-${index}`,
      reviews: [],
      gallery: [randomImages[index] || randomImages[0]],
      geolocation: `55.${753000 + index * 1000}, 37.${622000 + index * 1000}`,
    }));

    return properties;

  } catch (error: any) {
    console.error("Ошибка ИИ-предложений:", error);
    
    // Возвращаем понятные ошибки пользователю
    if (error.message.includes("не смог подобрать") || 
        error.message.includes("опишите ваши требования")) {
      throw error;
    } else if (error.message.includes("некорректный JSON") || 
               error.message.includes("некорректную структуру")) {
      throw new Error("ИИ вернул некорректные данные. Попробуйте еще раз.");
    } else if (error.message.includes("Ошибка API")) {
      throw new Error("Не удалось связаться с сервисом ИИ. Проверьте интернет-соединение.");
    } else {
      throw new Error("Произошла ошибка при обработке запроса. Попробуйте еще раз.");
    }
  }
}

// Функция для получения случайных удобств
function getRandomFacilities(): string[] {
  const allFacilities = [
    "Паркинг", "Детская площадка", "Закрытая территория", 
    "Рядом с парком", "Спортзал", "Бассейн", "Wi-Fi"
  ];
  
  const count = Math.floor(Math.random() * 3) + 2; // 2-4 удобства
  const shuffled = [...allFacilities].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
} 