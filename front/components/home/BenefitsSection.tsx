import { Home, Star, TrendingUp, Bot } from "lucide-react"

const benefits = [
  { icon: Home, title: "Прямые продажи", description: "Без посредников и лишних комиссий" },
  { icon: Star, title: "Проверенные застройщики", description: "Только надежные компании с гарантиями" },
  { icon: TrendingUp, title: "Лучшие цены", description: "Динамическое ценообразование и скидки" },
  { icon: Bot, title: "ИИ-подбор", description: "Умный помощник найдет идеальный вариант" },
]

export function BenefitsSection() {
  return (
    <section className="py-16 px-4 bg-blue-600 text-white">
      <div className="container mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Почему выбирают нас?</h2>
          <p className="text-blue-100 max-w-2xl mx-auto">
            Мы революционизируем рынок недвижимости, делая покупку квартир простой, прозрачной и выгодной
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {benefits.map((benefit, index) => (
            <div key={index} className="text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <benefit.icon className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{benefit.title}</h3>
              <p className="text-blue-100">{benefit.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
