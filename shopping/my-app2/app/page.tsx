//import ProductList from '@/components/ProductList'
import { ShoppingInterface } from '@/components/ShoppingInterface'
import { getGoods } from '@/lib/api'

export default async function Home() {
  const goods = await getGoods()

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Welcome to Our Shop</h1>
        <ShoppingInterface goods={goods} />
      </div>
    </div>
  )
}



