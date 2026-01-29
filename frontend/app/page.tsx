export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 flex items-center justify-center">
      <div className="text-center text-white">
        <h1 className="text-6xl font-bold mb-4">DAKiTAI</h1>
        <p className="text-xl mb-8">Profesyonel İşletme Yönetim Sistemi</p>
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-8 max-w-md mx-auto">
          <h2 className="text-2xl font-semibold mb-4">Panel Hazırlanıyor</h2>
          <p className="text-gray-300">Sistem başarıyla çalışıyor!</p>
          <div className="mt-6 space-y-2 text-left">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span>API Servisi</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span>Veritabanı</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span>SSL Sertifikası</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
