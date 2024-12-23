import ProductList from '@/components/ProductList'
import { getGoods } from '@/lib/api'

export default async function Home() {
  const goods = await getGoods()

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Order Website</h1>
      <ProductList goods={goods} />
    </main>
  )
}

