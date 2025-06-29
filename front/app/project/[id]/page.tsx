"use client"

import { MapPin, Star, Share2, Heart, Phone, Mail } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { useProject, useProjectReviews } from "@/lib/api-hooks"
import { mapApiProjectToProject, mapApiReviewToReview, type Review } from "@/lib/types"

interface PageProps {
  params: {
    id: string;
  };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default function ProjectPage({ params, searchParams }: PageProps) {
  const { data: apiProject, error: projectError } = useProject(params.id)
  const { data: apiReviews, error: reviewsError } = useProjectReviews(params.id)
  
  if (projectError || reviewsError) {
    return <div className="text-center text-red-500">Ошибка загрузки данных</div>
  }

  if (!apiProject) {
    return <div className="text-center">Загрузка...</div>
  }

  const project = mapApiProjectToProject(apiProject)
  const reviews = apiReviews ? apiReviews.map(mapApiReviewToReview) : []

  return (
    <div className="bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6 flex justify-between items-center">
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href="/">Недвижимость 5.0</Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href="/catalog">Каталог</Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator />
              <BreadcrumbItem>
                <BreadcrumbPage>{project.name}</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="icon">
              <Share2 className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon">
              <Heart className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Card className="overflow-hidden">
              <CardContent className="p-0">
                <Carousel>
                  <CarouselContent>
                    {project.gallery?.map((img, index) => (
                      <CarouselItem key={index}>
                        <Image
                          src={img || "/placeholder.svg"}
                          alt={`${project.name} - изображение ${index + 1}`}
                          width={800}
                          height={500}
                          className="w-full h-auto object-cover"
                        />
                      </CarouselItem>
                    )) || (
                      <CarouselItem>
                        <Image
                          src={project.image || "/placeholder.svg"}
                          alt={project.name}
                          width={800}
                          height={500}
                          className="w-full h-auto object-cover"
                        />
                      </CarouselItem>
                    )}
                  </CarouselContent>
                  <CarouselPrevious className="absolute left-4" />
                  <CarouselNext className="absolute right-4" />
                </Carousel>
              </CardContent>
            </Card>

            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Описание</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed">{project.description}</p>
              </CardContent>
            </Card>

            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Особенности</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-2 md:grid-cols-3 gap-6">
                {project.features?.map((feature, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <div className="bg-blue-100 text-blue-600 p-2 rounded-full">
                      <Star className="h-5 w-5" />
                    </div>
                    <span className="font-medium">{feature}</span>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Ход строительства</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {project.progress &&
                  Object.entries(project.progress).map(([key, value]) => (
                    <div key={key}>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700">
                          {
                            {
                              foundation: "Фундамент",
                              walls: "Возведение стен",
                              roof: "Кровля",
                              finishing: "Отделка",
                            }[key]
                          }
                        </span>
                        <span className="text-sm font-medium text-blue-600">{value}%</span>
                      </div>
                      <Progress value={value} />
                    </div>
                  ))}
              </CardContent>
            </Card>

            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Отзывы</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {reviews.map((review: Review) => (
                  <div key={review.id} className="flex gap-4">
                    <Avatar>
                      <AvatarImage src={review.avatar || "/placeholder-user.jpg"} />
                      <AvatarFallback>{review.author.charAt(0)}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="flex justify-between items-center">
                        <p className="font-semibold">{review.author}</p>
                        <div className="flex items-center gap-1">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`h-4 w-4 ${
                                i < review.rating ? "text-yellow-400 fill-current" : "text-gray-300"
                              }`}
                            />
                          ))}
                        </div>
                      </div>
                      <p className="text-sm text-gray-500 mb-2">{review.date}</p>
                      <p className="text-gray-700">{review.text}</p>
                    </div>
                  </div>
                ))}
                {reviews.length === 0 && (
                  <p className="text-center text-gray-500">Пока нет отзывов</p>
                )}
              </CardContent>
            </Card>
          </div>

          <div className="lg:sticky lg:top-24 self-start">
            <Card>
              <CardHeader>
                <h1 className="text-2xl font-bold">{project.name}</h1>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <MapPin className="h-4 w-4" />
                  <span>{project.location}</span>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-3xl font-bold text-blue-600">{project.price}</div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Застройщик</span>
                  <span className="font-medium">{project.developer}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Класс</span>
                  <Badge variant="secondary">{project.class}</Badge>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Срок сдачи</span>
                  <span className="font-medium">{project.completion}</span>
                </div>
                <Separator />
                <Button size="lg" className="w-full">
                  <Phone className="h-5 w-5 mr-2" />
                  Узнать об акции
                </Button>
                <Button size="lg" variant="outline" className="w-full bg-transparent">
                  <Mail className="h-5 w-5 mr-2" />
                  Получить консультацию
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
