import { z } from "zod"
import { NextResponse } from "next/server"

const MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
const apiKey = process.env.HACKB ?? ""

// Схема для одного предложения
const SuggestionSchema = z.object({
  id: z.number().optional(),
  address: z.string(),
  description: z.string(),
  price: z.number(),
  area: z.number(),
  rooms: z.number(),
  floor: z.number(),
  total_floors: z.number(),
  year_built: z.number(),
})

// Более гибкая схема для ответа от ИИ
const ApiResponseSchema = z.object({
  suggestions: z.array(SuggestionSchema),
})

export async function POST(req: Request) {
  if (!apiKey) {
    return NextResponse.json({ success: false, error: "Mistral API key не найден (HACKB)." }, { status: 500 })
  }

  try {
    const { prompt } = (await req.json()) as { prompt: string }

    // Проверяем, является ли запрос адекватным для поиска недвижимости
    if (!isValidRealEstateQuery(prompt)) {
      return NextResponse.json(
        {
          success: false,
          error:
            "Пожалуйста, опишите ваши требования к недвижимости более подробно. Например: 'Двухкомнатная квартира в Краснодаре до 10 млн ₽'.",
        },
        { status: 400 },
      )
    }

    const mistralRes = await fetch(MISTRAL_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${apiKey}`,
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
            content: prompt,
          },
        ],
        response_format: { type: "json_object" },
        temperature: 0.7,
      }),
    })

    if (!mistralRes.ok) {
      const text = await mistralRes.text()
      throw new Error(`Mistral API error ${mistralRes.status}: ${text}`)
    }

    const raw = await mistralRes.json()
    const content = raw.choices?.[0]?.message?.content ?? "{}"

    let parsedContent
    try {
      parsedContent = JSON.parse(content)
    } catch (parseError) {
      throw new Error("ИИ вернул некорректный JSON")
    }

    // Проверяем, что ответ содержит нужную структуру
    if (!parsedContent || typeof parsedContent !== "object") {
      throw new Error("ИИ вернул некорректную структуру данных")
    }

    // Если ИИ вернул массив вместо объекта, оборачиваем его
    if (Array.isArray(parsedContent)) {
      parsedContent = { suggestions: parsedContent }
    }

    // Если нет поля suggestions, создаем его
    if (!parsedContent.suggestions) {
      throw new Error("ИИ не смог подобрать подходящие варианты. Попробуйте уточнить ваш запрос.")
    }

    // Валидируем структуру
    const validated = ApiResponseSchema.parse(parsedContent)

    return NextResponse.json({ success: true, data: validated })
  } catch (err: any) {
    console.error("Ошибка при обработке запроса к ИИ:", err)

    // Возвращаем более понятные ошибки пользователю
    let userMessage = "Произошла ошибка при обработке запроса."

    if (err.message.includes("Expected object, received array")) {
      userMessage = "ИИ вернул некорректный формат данных. Попробуйте переформулировать запрос."
    } else if (err.message.includes("не смог подобрать")) {
      userMessage = err.message
    } else if (err.message.includes("некорректный JSON") || err.message.includes("некорректную структуру")) {
      userMessage = "ИИ вернул некорректные данные. Попробуйте еще раз."
    }

    return NextResponse.json({ success: false, error: userMessage }, { status: 500 })
  }
}

// Функция для проверки, является ли запрос адекватным для поиска недвижимости
function isValidRealEstateQuery(prompt: string): boolean {
  const lowercasePrompt = prompt.toLowerCase().trim()

  // Слишком короткие запросы
  if (lowercasePrompt.length < 5) {
    return false
  }

  // Простые приветствия
  const greetings = ["привет", "hello", "hi", "здравствуйте", "добрый день", "добрый вечер", "доброе утро"]
  if (greetings.some((greeting) => lowercasePrompt === greeting)) {
    return false
  }

  // Только цифры
  if (/^\d+$/.test(lowercasePrompt)) {
    return false
  }

  // Только символы
  if (/^[^\w\s]+$/.test(lowercasePrompt)) {
    return false
  }

  // Проверяем наличие ключевых слов, связанных с недвижимостью
  const realEstateKeywords = [
    "квартира",
    "дом",
    "комната",
    "студия",
    "жилье",
    "недвижимость",
    "купить",
    "снять",
    "аренда",
    "продажа",
    "цена",
    "стоимость",
    "район",
    "город",
    "метро",
    "этаж",
    "площадь",
    "м2",
    "кв.м",
    "рубл",
    "₽",
    "млн",
    "тыс",
    "миллион",
    "тысяч",
    "москва",
    "спб",
    "санкт-петербург",
    "краснодар",
    "сочи",
    "екатеринбург",
  ]

  const hasRealEstateKeywords = realEstateKeywords.some((keyword) => lowercasePrompt.includes(keyword))

  return hasRealEstateKeywords
}
