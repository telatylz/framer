import './globals.css'

export const metadata = {
  title: 'DAKiTAI Panel',
  description: 'Profesyonel İşletme Yönetim Sistemi',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  )
}
