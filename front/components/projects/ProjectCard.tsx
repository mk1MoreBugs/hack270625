import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MapPin, Star, Calendar, Eye } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import type { Project } from "@/lib/types"

interface ProjectCardProps {
  project: Project
}

export function ProjectCard({ project }: ProjectCardProps) {
  return (
    <Card className="overflow-hidden hover:shadow-xl transition-shadow">
      <div className="relative">
        <Image
          src={project.image || "/placeholder.svg"}
          alt={project.name}
          width={400}
          height={300}
          className="w-full h-48 object-cover"
        />
        {project.discount && (
          <Badge className="absolute top-4 left-4 bg-red-500 hover:bg-red-600">{project.discount}</Badge>
        )}
        <Badge variant="secondary" className="absolute top-4 right-4">
          {project.class}
        </Badge>
      </div>

      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-lg mb-1">{project.name}</CardTitle>
            <CardDescription className="flex items-center">
              <MapPin className="w-4 h-4 mr-1" />
              {project.location}
            </CardDescription>
          </div>
          <div className="flex items-center">
            <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
            <span className="text-sm font-medium">{project.rating}</span>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Застройщик:</span>
            <span className="font-medium">{project.developer}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Квартир:</span>
            <span className="font-medium">{project.totalApartments}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Сдача:</span>
            <span className="font-medium flex items-center">
              <Calendar className="w-4 h-4 mr-1" />
              {project.completion}
            </span>
          </div>
          <div className="pt-3 border-t">
            <div className="flex justify-between items-center mb-4">
              <span className="text-2xl font-bold text-blue-600">{project.price}</span>
            </div>
            <div className="flex space-x-2">
              <Link href={`/real_estates/${project.id}`} className="flex-1">
                <Button className="w-full">Подробнее</Button>
              </Link>
              <Link
                href="https://connector.eagle3dstreaming.com/v5/zvnd/Kubinka/default"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button variant="outline" className="flex items-center bg-transparent">
                  <Eye className="w-4 h-4 mr-1" />
                  3D-Тур ЖК
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
