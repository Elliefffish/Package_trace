'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { addPackage } from '../actions'

export function AddPackageForm() {
  const [packageId, setPackageId] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (packageId) {
      await addPackage(packageId)
      setPackageId('')
      router.refresh()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <Input
        type="text"
        value={packageId}
        onChange={(e) => setPackageId(e.target.value)}
        placeholder="Enter package ID"
        className="flex-grow"
      />
      <Button type="submit">Add Package</Button>
    </form>
  )
}


