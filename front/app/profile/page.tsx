"use client"

import { useState } from "react"
import { Heart, FileText, Eye, UserCheck } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { projectsData, leadsData } from "@/lib/data"
import { ProfileHeader } from "@/components/profile/ProfileHeader"

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState("recommendations")

  const stats = [
    { label: "В избранном", value: "8", icon: Heart },
    { label: "Мои заявки", value: "3", icon: FileText },
    { label: "Просмотрено", value: "25", icon: Eye },
    { label: "Рекомендаций", value: "12", icon: UserCheck },
  ]

  const recommendations = [
    {
      name: "ЖК Солнечный Берег",
      location: "Краснодар",
      price: "от 4.8М ₽",
      match: "95%",
    },
    {
      name: "ЖК Зеленый Квартал",
      location: "СПб",
      price: "от 6.2М ₽",
      match: "87%",
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <ProfileHeader />

      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Панель покупателя</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index} className="text-center">
              <CardContent className="pt-6">
                <div className="flex flex-col items-center space-y-2">
                  <stat.icon className="w-6 h-6 text-gray-400" />
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 max-w-md">
            <TabsTrigger value="recommendations">Рекомендации</TabsTrigger>
            <TabsTrigger value="favorites">Избранное</TabsTrigger>
            <TabsTrigger value="applications">Мои заявки</TabsTrigger>
          </TabsList>

          <TabsContent value="recommendations" className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Рекомендации для вас</h2>
              <p className="text-gray-600 mb-6">Подобранные ИИ варианты на основе ваших предпочтений</p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {recommendations.map((rec, index) => (
                  <Card key={index} className="p-6">
                    <div className="space-y-2">
                      <h3 className="font-semibold text-lg">{rec.name}</h3>
                      <p className="text-gray-600">
                        {rec.location} • {rec.price}
                      </p>
                      <p className="text-green-600 text-sm font-medium">Совпадение: {rec.match}</p>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="favorites" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Избранные проекты</CardTitle>
                <CardDescription>Сохраненные вами жилые комплексы</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Название</TableHead>
                      <TableHead>Локация</TableHead>
                      <TableHead>Статус</TableHead>
                      <TableHead>Квартиры</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {projectsData
                      .filter((project) => project.isFavorite)
                      .map((project) => (
                        <TableRow key={project.id}>
                          <TableCell className="font-medium">{project.name}</TableCell>
                          <TableCell>{project.location}</TableCell>
                          <TableCell>
                            <Badge variant={project.status === "Активный" ? "default" : "secondary"}>
                              {project.status}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            {project.available}/{project.totalApartments}
                          </TableCell>
                          <TableCell>
                            <Button variant="outline" size="sm">
                              Подробнее
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="applications" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Мои заявки</CardTitle>
                <CardDescription>Ваши обращения к застройщикам</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Проект</TableHead>
                      <TableHead>Квартира</TableHead>
                      <TableHead>Статус</TableHead>
                      <TableHead>Дата</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {leadsData
                      .filter((lead) => lead.name === "Иван Петров")
                      .map((lead) => (
                        <TableRow key={lead.id}>
                          <TableCell className="font-medium">{lead.project}</TableCell>
                          <TableCell>{lead.apartment}</TableCell>
                          <TableCell>
                            <Badge variant={lead.status === "Новая" ? "default" : "secondary"}>{lead.status}</Badge>
                          </TableCell>
                          <TableCell>{lead.date}</TableCell>
                          <TableCell>
                            <Button variant="outline" size="sm">
                              Подробнее
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
