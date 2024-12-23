import { NextResponse } from 'next/server'
import { createpackage } from '@/lib/api'

export async function POST(request: Request) {
  const { good_id, place } = await request.json()
  const order = await createpackage(good_id, place)
  return NextResponse.json(order)
}

