"use client"

import { ProjectCard } from "@/components/projects/ProjectCard"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { useFeaturedProjects } from "@/lib/api-hooks"
import { mapApiProjectToProject, type Project } from "@/lib/types"

export function FeaturedProjects() {
  const { data: apiProjects, error } = useFeaturedProjects()

  if (error) {
    return null; // Скрываем секцию при ошибке
  }

  if (!apiProjects) {
    return (
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Рекомендуемые проекты</h2>
              <p className="text-gray-600">Загрузка...</p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  const featuredProjects = apiProjects.slice(0, 3).map(mapApiProjectToProject);

  if (featuredProjects.length === 0) {
    return null; // Скрываем секцию, если нет рекомендуемых проектов
  }

  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="container mx-auto">
        <div className="flex items-center justify-between mb-12">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Рекомендуемые проекты</h2>
            <p className="text-gray-600">Лучшие предложения с эксклюзивными скидками</p>
          </div>
          <Link href="/catalog">
            <Button variant="outline">Смотреть все</Button>
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredProjects.map((project: Project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </div>
    </section>
  )
}
