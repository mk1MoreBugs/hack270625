export default function Loading() {
  return (
    <div className="flex min-h-[40vh] items-center justify-center">
      {/* Простой индикатор загрузки */}
      <span
        aria-label="Загрузка…"
        className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-muted-foreground border-t-transparent"
      />
    </div>
  )
}
