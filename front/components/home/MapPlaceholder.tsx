import { Button } from "@/components/ui/button"
import { MapPin } from "lucide-react"

export function MapPlaceholder() {
  return (
    <section className="py-16 px-4">
      <div className="container mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Интерактивная карта новостроек</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Найдите идеальное расположение для вашего будущего дома. Все проекты на одной карте с подробной информацией.
          </p>
        </div>
        <div className="bg-gray-200 rounded-2xl h-96 flex items-center justify-center">
          <div className="text-center">
            <MapPin className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">Интерактивная карта загружается...</p>
            <Button>Открыть полную карту</Button>
          </div>
        </div>
      </div>
    </section>
  )
}
