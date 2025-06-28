import { homeStats } from "@/lib/data"

export function StatsSection() {
  return (
    <section className="container mx-auto px-4 pb-16">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {homeStats.map((stat, index) => (
          <div key={index} className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <stat.icon className="w-8 h-8 text-blue-600" />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-2">{stat.value}</div>
            <div className="text-gray-600">{stat.label}</div>
          </div>
        ))}
      </div>
    </section>
  )
}
