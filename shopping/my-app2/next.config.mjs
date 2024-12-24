/** @type {import('next').NextConfig} */
const nextConfig = {

images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost', // 圖片主機
        port: '3001',         
        pathname: '/image',    
      },
    ],
  },};

export default nextConfig;
