'use client'

import { useState } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

{/*image api : http://localhost:3001 write in ".env.local" in root dir */}
const api_url = process.env.NEXT_PUBLIC_IMAGE_API_URL;

type Good = {
  good_id: number
  name: string
  price: number
  img: string
  description: string
}

export default function GoodList({ goods }: { goods: Good[] }) {
  const [selectedStore, setSelectedStore] = useState<string>('')
  const router = useRouter()

  const handleOrder = async (goodId: number) => {
    if (!selectedStore) {
      alert('Please select a store')
      return
    }

    const response = await fetch('/api/order', {
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
          {/*
          <Select onValueChange={setSelectedStore}>
            <SelectTrigger className="w-full mb-2">
              <SelectValue placeholder="Select store" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="familymart">FamilyMart</SelectItem>
              <SelectItem value="7-11">7-11</SelectItem>
              <SelectItem value="ok-mart">OK-Mart</SelectItem>
              <SelectItem value="shopee">Shopee</SelectItem>
            </SelectContent>
          </Select>
          */}
          <Button onClick={() => handleOrder(good.good_id)} className="w-full">
            Order
          </Button>
        </div>
      ))}
    </div>
  )
}

