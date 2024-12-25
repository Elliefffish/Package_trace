'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
//import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function SearchForm({ initialId = '' }: { initialId?: string }) {
  const [packageId, setPackageId] = useState(initialId)
  const router = useRouter()

  useEffect(() => {
    if (initialId) {
      handleSubmit()
    }
  }, [initialId])

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (packageId) {
      router.push(`/packages?id=${encodeURIComponent(packageId)}`)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <input
          type="text"
          value={packageId}
          onChange={(e) => setPackageId(e.target.value)}
          placeholder="Enter package ID"
          className="w-full"
        />
      </div>
      <Button type="submit" className="w-full">Search</Button>
    </form>
  )
}


