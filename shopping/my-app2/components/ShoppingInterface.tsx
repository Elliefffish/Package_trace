'use client'

import { useState } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { placeOrder } from '../app/actions'


const api_url = process.env.NEXT_PUBLIC_IMAGE_API_URL;

type Good = {
  good_id: number
  name: string
  price: number
  img: string
  description: string
}

export function ShoppingInterface({ goods }: { goods: Good[]}) {
  const [orderedPackageId, setOrderedPackageId] = useState<string | null>(null)
  const router = useRouter()

  const handleOrder = async (GoodId: number) => {
    const packageId = await placeOrder(GoodId)
    setOrderedPackageId(packageId)

/*    const response = await fetch('/api/order',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ goodId, store: selectedStore }),
      })

      if (response.ok) {
        router.push('/orders')
      } else {
        alert('Failed to place order')
      }*/
  }

  const handleTracePackage = () => {
    if (orderedPackageId) {
      router.push(`/packages?id=${orderedPackageId}`)
    }
  }


  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {goods.map((good) => (
        <div key={good.good_id} className="border p-4 rounded-lg">
          <Image src={`${api_url}/image?img=${good.img}`} alt={good.name} width={203} height={200} className="mb-2" />
          {/*
          <Image src={`http://localhost:3001/image?img=${good.img.split('/').pop()}`} alt={good.name} width={203} height={200} className="mb-2" />
          */}
          <h2 className="text-lg font-semibold">{good.name}</h2>
          <p className="mb-2">${good.price.toFixed(2)}</p>
          <p className="mb-2">{good.description}</p>
          <Button onClick={() => handleOrder(good.id)}>Order Now</Button>
        </div>
      ))}
      {orderedPackageId && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Order Placed!</strong>
          <div><span className="block sm:inline"> Your package ID is: {orderedPackageId}</span></div>
          <Button className="mt-2" onClick={handleTracePackage}>Trace Package</Button>
        </div>
      )}
    </div>
  )
}


