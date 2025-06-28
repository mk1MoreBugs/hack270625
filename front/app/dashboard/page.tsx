"use client"

import { useAppContext } from "@/contexts/AppContext"
import { Home, Phone, Mail, Eye, Edit, Plus, Bell, Filter, Download } from "lucide-react"
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
import { dashboardStats, projectsData, leadsData } from "@/lib/data"
import type { UserRole } from "@/lib/types"
import { DashboardHeader } from "@/components/dashboard/DashboardHeader"

export default function DashboardPage() {
  const { userRole, setUserRole } = useAppContext()

  const projects = projectsData.slice(0, 2)
  const leads = leadsData

  const buyerLinks = [
    { href: "/dashboard", label: "Панель управления", active: true },
    { href: "/catalog", label: "Каталог" },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {userRole === "buyer" ? (
        <DashboardHeader links={buyerLinks} userName="ИП" />
      ) : (
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
      )}

      <div className="container mx-auto px-4 py-8">
        {userRole === "buyer" ? (
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Панель покупателя</h1>
        ) : (
          <div className="mb-8">
            <div className="flex items-center space-x-4">
              <h1 className="text-3xl font-bold text-gray-900">Панель управления</h1>
              <Select value={userRole} onValueChange={(value) => setUserRole(value as UserRole)}>
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
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {dashboardStats[userRole].map((stat, index) => (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">{stat.label}</CardTitle>
                <stat.icon className="w-5 h-5 text-gray-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                {stat.change && <p className="text-xs text-green-600 mt-1">{stat.change} за месяц</p>}
              </CardContent>
            </Card>
          ))}
        </div>

        <Tabs defaultValue={userRole === "buyer" ? "recommendations" : "overview"} className="space-y-6">
          <TabsList>
            {userRole === "buyer" ? (
              <>
                <TabsTrigger value="recommendations">Рекомендации</TabsTrigger>
                <TabsTrigger value="favorites">Избранное</TabsTrigger>
                <TabsTrigger value="applications">Мои заявки</TabsTrigger>
              </>
            ) : (
              <>
                <TabsTrigger value="overview">Обзор</TabsTrigger>
                {userRole === "developer" && (
                  <>
                    <TabsTrigger value="projects">Проекты</TabsTrigger>
                    <TabsTrigger value="leads">Заявки</TabsTrigger>
                    <TabsTrigger value="analytics">Аналитика</TabsTrigger>
                  </>
                )}
                {userRole === "admin" && (
                  <>
                    <TabsTrigger value="developers">Застройщики</TabsTrigger>
                    <TabsTrigger value="moderation">Модерация</TabsTrigger>
                    <TabsTrigger value="reports">Отчеты</TabsTrigger>
                  </>
                )}
              </>
            )}
          </TabsList>

          {userRole === "buyer" ? (
            <>
              <TabsContent value="recommendations" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Рекомендации для вас</CardTitle>
                    <CardDescription>Подобранные ИИ варианты на основе ваших предпочтений</CardDescription>
                  </CardHeader>
                  <CardContent className="grid gap-6 md:grid-cols-2">
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
                  </CardContent>
                </Card>
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
          ) : (
            <>
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
                                  {project.available}/{project.totalApartments}
                                </span>
                              </div>
                              <Progress value={(project.available / project.totalApartments) * 100} className="h-2" />
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
                                  <Badge variant={lead.status === "Новая" ? "default" : "secondary"}>
                                    {lead.status}
                                  </Badge>
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

              {userRole === "admin" && (
                <>
                  <TabsContent value="developers" className="space-y-6">
                    <div className="flex items-center justify-between">
                      <h2 className="text-2xl font-bold">Застройщики</h2>
                      <Button variant="outline">
                        <Download className="w-4 h-4 mr-2" />
                        Экспорт
                      </Button>
                    </div>

                    <Card>
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <div>
                            <CardTitle>Список застройщиков</CardTitle>
                            <CardDescription>Управление застройщиками</CardDescription>
                          </div>
                          <div className="flex space-x-2">
                            <Input placeholder="Поиск..." className="w-64" />
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
                              <TableHead>Проекты</TableHead>
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

                  <TabsContent value="moderation" className="space-y-6">
                    <div className="flex items-center justify-between">
                      <h2 className="text-2xl font-bold">Модерация</h2>
                    </div>

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
                  </TabsContent>

                  <TabsContent value="reports" className="space-y-6">
                    <div className="flex items-center justify-between">
                      <h2 className="text-2xl font-bold">Отчеты</h2>
                    </div>

                    <Card>
                      <CardHeader>
                        <CardTitle>Общий оборот</CardTitle>
                        <CardDescription>Отчет по обороту недвижимости</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="text-3xl font-bold text-blue-600">1.8Б ₽</div>
                        <Button variant="outline" className="w-full mt-4 bg-transparent">
                          Просмотреть отчет
                        </Button>
                      </CardContent>
                    </Card>
                  </TabsContent>
                </>
              )}
            </>
          )}
        </Tabs>
      </div>
    </div>
  )
}
