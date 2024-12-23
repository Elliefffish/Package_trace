'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

type Order = {
  id: number
  productName: string
  orderTime: string
  status: 'processing' | 'shipping' | 'delivered'
  statusUpdateTime: string
  store: string
}

export default function OrderList({ initialOrders }: { initialOrders: Order[] }) {
  const [orders, setOrders] = useState(initialOrders)

  useEffect(() => {
    const intervalId = setInterval(async () => {
      const response = await fetch('/api/orders')
      const updatedOrders = await response.json()
      setOrders(updatedOrders)
    }, 5 * 60 * 1000) // Update every 5 minutes

    return () => clearInterval(intervalId)
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {orders.map((order) => (
        <Card key={order.id}>
          <CardHeader>
            <CardTitle>{order.productName}</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Order Time: {new Date(order.orderTime).toLocaleString()}</p>
            <p>Status: {order.status}</p>
            <p>Last Updated: {new Date(order.statusUpdateTime).toLocaleString()}</p>
            <p>Store: {order.store}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

