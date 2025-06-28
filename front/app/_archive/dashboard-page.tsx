"use client"

import { useState } from "react"
import {
  Home,
  Users,
  Building,
  TrendingUp,
  Phone,
  Mail,
  Eye,
  Edit,
  Plus,
  BarChart3,
  Bell,
  Filter,
  Download,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import Link from "next/link"

export default function DashboardPage() {
  const [userRole, setUserRole] = useState("developer") // developer, buyer, admin

  const stats = {
    developer: [
      { label: "Активных проектов", value: "12", change: "+2", icon: Building },
      { label: "Заявок за месяц", value: "156", change: "+23%", icon: Users },
      { label: "Продано квартир", value: "89", change: "+15%", icon: Home },
      { label: "Средний чек", value: "8.5М ₽", change: "+5%", icon: TrendingUp },
    ],
    buyer: [
      { label: "Избранных проектов", value: "8", change: "+3", icon: Home },
      { label: "Просмотров", value: "24", change: "+12", icon: Eye },
      { label: "Заявок отправлено", value: "5", change: "+2", icon: Mail },
      { label: "Средняя цена", value: "7.2М ₽", change: "-3%", icon: TrendingUp },
    ],
    admin: [
      { label: "Всего застройщиков", value: "150", change: "+8", icon: Building },
      { label: "Активных проектов", value: "487", change: "+23", icon: Home },
      { label: "Сделок за месяц", value: "234", change: "+18%", icon: TrendingUp },
      { label: "Общий оборот", value: "1.8Б ₽", change: "+12%", icon: BarChart3 },
    ],
  }

  const projects = [
    {
      id: 1,
      name: "ЖК Северная Звезда",
      location: "Москва, САО",
      status: "Активный",
      completion: "Q4 2025",
      sold: 156,
      total: 245,
      revenue: "1.3Б ₽",
      leads: 23,
    },
    {
      id: 2,
      name: "ЖК Зеленый Квартал",
      location: "СПб, Приморский",
      status: "Строительство",
      completion: "Q2 2026",
      sold: 89,
      total: 180,
      revenue: "890М ₽",
      leads: 15,
    },
  ]

  const leads = [
    {
      id: 1,
      name: "Анна Петрова",
      phone: "+7 (999) 123-45-67",
      email: "anna@example.com",
      project: "ЖК Северная Звезда",
      apartment: "2-комнатная",
      status: "Новая",
      date: "2024-12-20",
      source: "Сайт",
    },
    {
      id: 2,
      name: "Михаил Сидоров",
      phone: "+7 (999) 765-43-21",
      email: "mikhail@example.com",
      project: "ЖК Зеленый Квартал",
      apartment: "1-комнатная",
      status: "В работе",
      date: "2024-12-19",
      source: "Реклама",
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b bg-white sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Home className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Недвижимость 4.0</span>
            </Link>

            <nav className="hidden md:flex items-center space-x-8">
              <Link href="/dashboard" className="text-blue-600 font-medium">
                Панель управления
              </Link>
              <Link href="/catalog" className="text-gray-700 hover:text-blue-600 font-medium">
                Каталог
              </Link>
              <Link href="#" className="text-gray-700 hover:text-blue-600 font-medium">
                Аналитика
              </Link>
            </nav>

            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="icon">
                <Bell className="w-5 h-5" />
              </Button>
              <Avatar>
                <AvatarImage src="/placeholder.svg?height=32&width=32" />
                <AvatarFallback>АП</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Role Selector */}
        <div className="mb-8">
          <div className="flex items-center space-x-4">
            <h1 className="text-3xl font-bold text-gray-900">Панель управления</h1>
            <Select value={userRole} onValueChange={setUserRole}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="developer">Застройщик</SelectItem>
                <SelectItem value="buyer">Покупатель</SelectItem>
                <SelectItem value="admin">Администратор</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats[userRole as keyof typeof stats].map((stat, index) => (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">{stat.label}</CardTitle>
                <stat.icon className="w-5 h-5 text-gray-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-green-600 mt-1">{stat.change} за месяц</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList>
            <TabsTrigger value="overview">Обзор</TabsTrigger>
            {userRole === "developer" && (
              <>
                <TabsTrigger value="projects">Проекты</TabsTrigger>
                <TabsTrigger value="leads">Заявки</TabsTrigger>
                <TabsTrigger value="analytics">Аналитика</TabsTrigger>
              </>
            )}
            {userRole === "buyer" && (
              <>
                <TabsTrigger value="favorites">Избранное</TabsTrigger>
                <TabsTrigger value="applications">Мои заявки</TabsTrigger>
                <TabsTrigger value="recommendations">Рекомендации</TabsTrigger>
              </>
            )}
            {userRole === "admin" && (
              <>
                <TabsTrigger value="developers">Застройщики</TabsTrigger>
                <TabsTrigger value="moderation">Модерация</TabsTrigger>
                <TabsTrigger value="reports">Отчеты</TabsTrigger>
              </>
            )}
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {userRole === "developer" && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Последние заявки</CardTitle>
                    <CardDescription>Новые обращения от покупателей</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {leads.slice(0, 3).map((lead) => (
                        <div key={lead.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div>
                            <p className="font-medium">{lead.name}</p>
                            <p className="text-sm text-gray-600">{lead.project}</p>
                          </div>
                          <Badge variant={lead.status === "Новая" ? "default" : "secondary"}>{lead.status}</Badge>
                        </div>
                      ))}
                    </div>
                    <Button variant="outline" className="w-full mt-4 bg-transparent">
                      Все заявки
                    </Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Продажи по проектам</CardTitle>
                    <CardDescription>Статистика продаж за текущий месяц</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {projects.map((project) => (
                        <div key={project.id} className="space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="font-medium">{project.name}</span>
                            <span className="text-sm text-gray-600">
                              {project.sold}/{project.total}
                            </span>
                          </div>
                          <Progress value={(project.sold / project.total) * 100} className="h-2" />
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {userRole === "buyer" && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Рекомендации для вас</CardTitle>
                    <CardDescription>Подобранные ИИ варианты</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="p-4 border rounded-lg">
                        <h3 className="font-medium">ЖК Солнечный Берег</h3>
                        <p className="text-sm text-gray-600">Краснодар • от 4.8М ₽</p>
                        <p className="text-xs text-green-600 mt-1">Совпадение: 95%</p>
                      </div>
                      <div className="p-4 border rounded-lg">
                        <h3 className="font-medium">ЖК Зеленый Квартал</h3>
                        <p className="text-sm text-gray-600">СПб • от 6.2М ₽</p>
                        <p className="text-xs text-green-600 mt-1">Совпадение: 87%</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Активные заявки</CardTitle>
                    <CardDescription>Ваши обращения к застройщикам</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">ЖК Северная Звезда</p>
                          <p className="text-sm text-gray-600">2-комнатная</p>
                        </div>
                        <Badge>Ответ получен</Badge>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">ЖК Премиум Резиденс</p>
                          <p className="text-sm text-gray-600">3-комнатная</p>
                        </div>
                        <Badge variant="secondary">Ожидание</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {userRole === "admin" && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Новые застройщики</CardTitle>
                    <CardDescription>Ожидают модерации</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-blue-600">8</div>
                    <Button variant="outline" className="w-full mt-4 bg-transparent">
                      Перейти к модерации
                    </Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Жалобы</CardTitle>
                    <CardDescription>Требуют рассмотрения</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-red-600">3</div>
                    <Button variant="outline" className="w-full mt-4 bg-transparent">
                      Рассмотреть
                    </Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Системные уведомления</CardTitle>
                    <CardDescription>Важные события</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-orange-600">12</div>
                    <Button variant="outline" className="w-full mt-4 bg-transparent">
                      Просмотреть
                    </Button>
                  </CardContent>
                </Card>
              </div>
            )}
          </TabsContent>

          {userRole === "developer" && (
            <>
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
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle>Список проектов</CardTitle>
                        <CardDescription>Управление вашими жилыми комплексами</CardDescription>
                      </div>
                      <div className="flex space-x-2">
                        <Input placeholder="Поиск..." className="w-64" />
                        <Button variant="outline" size="icon">
                          <Filter className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
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
                        {projects.map((project) => (
                          <TableRow key={project.id}>
                            <TableCell className="font-medium">{project.name}</TableCell>
                            <TableCell>{project.location}</TableCell>
                            <TableCell>
                              <Badge variant={project.status === "Активный" ? "default" : "secondary"}>
                                {project.status}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              {project.sold}/{project.total}
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
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle>Все заявки</CardTitle>
                        <CardDescription>Обращения от потенциальных покупателей</CardDescription>
                      </div>
                      <div className="flex space-x-2">
                        <Select>
                          <SelectTrigger className="w-40">
                            <SelectValue placeholder="Статус" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="all">Все</SelectItem>
                            <SelectItem value="new">Новые</SelectItem>
                            <SelectItem value="in-progress">В работе</SelectItem>
                            <SelectItem value="closed">Закрытые</SelectItem>
                          </SelectContent>
                        </Select>
                        <Input placeholder="Поиск по имени..." className="w-64" />
                      </div>
                    </div>
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
                        {leads.map((lead) => (
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
            </>
          )}
        </Tabs>
      </div>
    </div>
  )
}
