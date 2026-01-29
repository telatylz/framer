/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['dakiktabela.com.tr'],
  },
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
    ]
  },
}

module.exports = nextConfig
