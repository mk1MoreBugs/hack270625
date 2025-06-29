"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Download, Eye, Edit, Phone, Mail, Plus } from "lucide-react"
import { projectsData, leadsData } from "@/lib/data"
import { DashboardHeader } from "@/components/dashboard/DashboardHeader"

interface NewProject {
  city: string
  name: string
  status: "Сдан" | "Продаётся" | "Застройка"
  apartments: number
}

export default function DeveloperDashboardPage() {
  const [isAddProjectOpen, setIsAddProjectOpen] = useState(false)
  const [newProject, setNewProject] = useState<NewProject>({
    city: "",
    name: "",
    status: "Продаётся",
    apartments: 0,
  })
  const [projects, setProjects] = useState(projectsData)

  const handleAddProject = () => {
    if (newProject.city && newProject.name && newProject.apartments > 0) {
      const project = {
        ...projectsData[0], // Копируем структуру существующего проекта
        id: Date.now().toString(),
        name: newProject.name,
        location: newProject.city,
        status: newProject.status,
        totalApartments: newProject.apartments,
        available: newProject.apartments,
        sold: 0,
        revenue: "0 ₽",
        leads: 0,
      }
      setProjects([...projects, project])
      setNewProject({ city: "", name: "", status: "Продаётся", apartments: 0 })
      setIsAddProjectOpen(false)
    }
  }

  const getStatusVariant = (status: string) => {
    switch (status) {
      case "Сдан":
        return "secondary"
      case "Продаётся":
        return "default"
      case "Застройка":
        return "outline"
      default:
        return "default"
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader links={[]} userName="ЗС" isLogoLink={false} />
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
              <Dialog open={isAddProjectOpen} onOpenChange={setIsAddProjectOpen}>
                <DialogTrigger asChild>
                  <Button>
                    <Plus className="w-4 h-4 mr-2" />
                    Добавить проект
                  </Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-[425px]">
                  <DialogHeader>
                    <DialogTitle>Добавить новый проект</DialogTitle>
                    <DialogDescription>Заполните информацию о новом жилом комплексе</DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid gap-2">
                      <Label htmlFor="city">Город</Label>
                      <Input
                        id="city"
                        value={newProject.city}
                        onChange={(e) => setNewProject({ ...newProject, city: e.target.value })}
                        placeholder="Например: Краснодар"
                      />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="name">Название ЖК</Label>
                      <Input
                        id="name"
                        value={newProject.name}
                        onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                        placeholder="Например: ЖК Солнечный"
                      />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="status">Статус ЖК</Label>
                      <Select
                        value={newProject.status}
                        onValueChange={(value: "Сдан" | "Продаётся" | "Застройка") =>
                          setNewProject({ ...newProject, status: value })
                        }
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="Сдан">Сдан</SelectItem>
                          <SelectItem value="Продаётся">Продаётся</SelectItem>
                          <SelectItem value="Застройка">Застройка</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="apartments">Количество квартир</Label>
                      <Input
                        id="apartments"
                        type="number"
                        value={newProject.apartments || ""}
                        onChange={(e) =>
                          setNewProject({ ...newProject, apartments: Number.parseInt(e.target.value) || 0 })
                        }
                        placeholder="Например: 150"
                        min="1"
                      />
                    </div>
                  </div>
                  <div className="flex justify-end space-x-2">
                    <Button variant="outline" onClick={() => setIsAddProjectOpen(false)}>
                      Отмена
                    </Button>
                    <Button onClick={handleAddProject}>Добавить проект</Button>
                  </div>
                </DialogContent>
              </Dialog>
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
                      <TableHead>Город</TableHead>
                      <TableHead>Название ЖК</TableHead>
                      <TableHead>Статус ЖК</TableHead>
                      <TableHead>Кол-во квартир</TableHead>
                      <TableHead>Действия</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {projects.map((project) => (
                      <TableRow key={project.id}>
                        <TableCell className="font-medium">{project.location.split(",")[0]}</TableCell>
                        <TableCell>{project.name}</TableCell>
                        <TableCell>
                          <Badge variant={getStatusVariant(project.status || "Продаётся")}>
                            {project.status || "Продаётся"}
                          </Badge>
                        </TableCell>
                        <TableCell>{project.totalApartments}</TableCell>
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
