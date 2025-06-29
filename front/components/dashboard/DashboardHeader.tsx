import { Home, Bell } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import Link from "next/link"

type DashboardHeaderProps = {
  links: { href: string; label: string; active?: boolean }[]
  userName?: string
  isLogoLink?: boolean
}

export function DashboardHeader({ links, userName = "АП", isLogoLink = true }: DashboardHeaderProps) {
  return (
    <header className="border-b bg-white sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {isLogoLink ? (
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Home className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Недвижимость 5.0</span>
            </Link>
          ) : (
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Home className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Недвижимость 5.0</span>
            </div>
          )}

          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon">
              <Bell className="w-5 h-5" />
            </Button>
            <Avatar>
              <AvatarImage src={`https://i.pravatar.cc/32?u=${userName}`} />
              <AvatarFallback>{userName}</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>
    </header>
  )
}
