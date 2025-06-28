"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Eye, Edit } from "lucide-react"
import { projectsData } from "@/lib/data"
import { DashboardHeader } from "@/components/dashboard/DashboardHeader"

export default function AdminDashboardPage() {
  const adminLinks = [
    { href: "/dashboard-admin", label: "Панель управления", active: true },
    { href: "/catalog", label: "Каталог" },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader links={adminLinks} userName="АД" />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Панель администратора</h1>
        <Tabs defaultValue="developers" className="space-y-6">
          <TabsList>
            <TabsTrigger value="developers">Застройщики</TabsTrigger>
            <TabsTrigger value="moderation">Модерация</TabsTrigger>
            <TabsTrigger value="reports">Отчеты</TabsTrigger>
          </TabsList>

          <TabsContent value="developers" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Список застройщиков</CardTitle>
                <CardDescription>Управление застройщиками на платформе</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Название</TableHead>
                      <TableHead>Локация</TableHead>
                      <TableHead>Статус</TableHead>
                      <TableHead>Проекты</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {projectsData.map((project) => (
                      <TableRow key={project.id}>
                        <TableCell className="font-medium">{project.developer}</TableCell>
                        <TableCell>{project.location}</TableCell>
                        <TableCell>
                          <Badge variant="default">Активен</Badge>
                        </TableCell>
                        <TableCell>1</TableCell>
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

          <TabsContent value="moderation" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Модерация</CardTitle>
                <CardDescription>Объекты, ожидающие проверки</CardDescription>
              </CardHeader>
              <CardContent>
                <p>Нет объектов для модерации.</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reports" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Отчеты</CardTitle>
                <CardDescription>Системные отчеты и аналитика</CardDescription>
              </CardHeader>
              <CardContent>
                <p>Раздел отчетов находится в разработке.</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
