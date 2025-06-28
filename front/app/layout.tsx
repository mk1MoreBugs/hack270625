import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { cn } from "@/lib/utils"
import { AppProvider } from "@/contexts/AppContext"
import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export const metadata: Metadata = {
  title: "Недвижимость 4.0",
  description: "Платформа прямых продаж квартир от застройщиков",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body className={cn("min-h-screen bg-background font-sans antialiased", inter.variable)}>
        <AppProvider>
          <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
            <Header />
            <main>{children}</main>
            <Footer />
          </div>
        </AppProvider>
      </body>
    </html>
  )
}
