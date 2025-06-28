import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import Link from "next/link"

export default function LoginPage() {
  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-400px)] bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold">Вход в аккаунт</CardTitle>
          <CardDescription>Введите данные для входа или выберите роль</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="example@mail.com" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Пароль</Label>
              <Input id="password" type="password" required />
            </div>
            <div className="flex flex-col space-y-2 pt-2">
              <Link href="/dashboard" passHref>
                <Button className="w-full">Войти</Button>
              </Link>
              <Button variant="secondary" className="w-full">
                Зарегистрироваться
              </Button>
            </div>
          </form>
          <div className="mt-6 flex flex-col items-center space-y-2">
            <Link href="/dashboard-developer" passHref>
              <Button variant="link">Войти как застройщик</Button>
            </Link>
            <Link href="/dashboard-admin" passHref>
              <Button variant="link">Войти как админ</Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
