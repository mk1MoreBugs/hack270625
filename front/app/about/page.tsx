export default function AboutPage() {
  return (
    <div className="bg-white">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-center mb-8 text-gray-900">О платформе «Недвижимость 5.0»</h1>
          <div className="prose lg:prose-xl max-w-none text-gray-700 space-y-6">
            <p>
              «Недвижимость 5.0» — это цифровая витрина первичного жилья, созданная, чтобы избавить рынок от
              посреднических наценок и фейковых объявлений. Мы соединяем покупателя напрямую с отделом продаж
              застройщика, показываем живую цену на каждый лот и помогаем оформить сделку быстрее и прозрачнее.
            </p>
            <h2 className="text-2xl font-semibold text-gray-800 mt-10">Партнёрство с отраслью</h2>
            <p>
              Платформа разработана при поддержке Ассоциации застройщиков Краснодарского края. Все объекты проходят
              верификацию Ассоциации: вы видите только официальные данные о разрешениях, стадиях строительства и
              реальном остатке квартир.
            </p>
            <h2 className="text-2xl font-semibold text-gray-800 mt-10">Что получаете вы</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="border-l-4 border-blue-500 pl-4">
                <h3 className="font-bold text-lg text-gray-800">Покупатель</h3>
                <p>
                  — честную стоимость без 5 % риелторской надбавки, ИИ-подбор лучших вариантов и один визит в МФЦ вместо
                  недель бумажной волокиты.
                </p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <h3 className="font-bold text-lg text-gray-800">Девелопер</h3>
                <p>
                  — динамическое ценообразование, сквозную аналитику и маркетинг «из одного окна», экономя до 40 %
                  бюджета на рекламе.
                </p>
              </div>
            </div>
            <p className="pt-6 text-center text-lg">
              Мы верим, что прозрачный рынок выгоден всем участникам и помогает городам развиваться быстрее и
              качественнее.
              <br />
              <strong>Добро пожаловать в «Недвижимость 5.0»!</strong>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
