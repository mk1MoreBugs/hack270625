import { projectsData } from "@/lib/data"
import { ProjectCard } from "@/components/projects/ProjectCard"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export function FeaturedProjects() {
  const featuredProjects = projectsData.slice(0, 3)

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
          {featuredProjects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </div>
    </section>
  )
}
