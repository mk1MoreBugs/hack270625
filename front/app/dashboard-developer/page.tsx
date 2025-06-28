"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Download, Eye, Edit, Phone, Mail, Plus } from "lucide-react"
import { projectsData, leadsData } from "@/lib/data"
import { DashboardHeader } from "@/components/dashboard/DashboardHeader"

export default function DeveloperDashboardPage() {
  const developerLinks = [
    { href: "/dashboard-developer", label: "Панель управления", active: true },
    { href: "/catalog", label: "Каталог" },
    { href: "#", label: "Аналитика" },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader links={developerLinks} userName="ЗС" />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Панель застройщика</h1>
        <Tabs defaultValue="projects" className="space-y-6">
          <TabsList>
            <TabsTrigger value="projects">Проекты</TabsTrigger>
            <TabsTrigger value="leads">Заявки</TabsTrigger>
            <TabsTrigger value="analytics">Аналитика</TabsTrigger>
          </TabsList>

          <TabsContent value="projects" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold">Мои проекты</h2>
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Добавить проект
              </Button>
            </div>
            <Card>
              <CardHeader>
                <CardTitle>Список проектов</CardTitle>
                <CardDescription>Управление вашими жилыми комплексами</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Название</TableHead>
                      <TableHead>Локация</TableHead>
                      <TableHead>Статус</TableHead>
                      <TableHead>Продано</TableHead>
                      <TableHead>Выручка</TableHead>
                      <TableHead>Заявки</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {projectsData.map((project) => (
                      <TableRow key={project.id}>
                        <TableCell className="font-medium">{project.name}</TableCell>
                        <TableCell>{project.location}</TableCell>
                        <TableCell>
                          <Badge variant={project.status === "Активный" ? "default" : "secondary"}>
                            {project.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {project.sold}/{project.totalApartments}
                        </TableCell>
                        <TableCell>{project.revenue}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{project.leads}</Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button variant="outline" size="sm">
                              <Eye className="w-4 h-4" />
                            </Button>
                            <Button variant="outline" size="sm">
                              <Edit className="w-4 h-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="leads" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold">Заявки покупателей</h2>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Экспорт
              </Button>
            </div>
            <Card>
              <CardHeader>
                <CardTitle>Все заявки</CardTitle>
                <CardDescription>Обращения от потенциальных покупателей</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Клиент</TableHead>
                      <TableHead>Контакты</TableHead>
                      <TableHead>Проект</TableHead>
                      <TableHead>Квартира</TableHead>
                      <TableHead>Статус</TableHead>
                      <TableHead>Дата</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {leadsData.map((lead) => (
                      <TableRow key={lead.id}>
                        <TableCell className="font-medium">{lead.name}</TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm">{lead.phone}</div>
                            <div className="text-xs text-gray-600">{lead.email}</div>
                          </div>
                        </TableCell>
                        <TableCell>{lead.project}</TableCell>
                        <TableCell>{lead.apartment}</TableCell>
                        <TableCell>
                          <Badge variant={lead.status === "Новая" ? "default" : "secondary"}>{lead.status}</Badge>
                        </TableCell>
                        <TableCell>{lead.date}</TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button variant="outline" size="sm">
                              <Phone className="w-4 h-4" />
                            </Button>
                            <Button variant="outline" size="sm">
                              <Mail className="w-4 h-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Аналитика</CardTitle>
              </CardHeader>
              <CardContent>
                <p>Раздел аналитики находится в разработке.</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
