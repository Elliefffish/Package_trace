import { getOrders } from '@/lib/api'
import OrderList from '@/components/OrderList'

export default async function OrdersPage() {
  const orders = await getOrders()

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Order Status</h1>
      <OrderList initialOrders={orders} />
    </div>
  )
}

