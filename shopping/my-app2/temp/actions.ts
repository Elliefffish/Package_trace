'use server'

import { Package, StatusUpdate } from './types'

const packagesDatabase: Package[] = [
  {
    id: 'PKG001',
    status: 'In Transit',
    estimatedArrival: '2023-05-16',
    currentLocation: 'Distribution Center, New York',
    statusHistory: [
      { status: 'In Transit', timestamp: '2023-05-15 14:30', location: 'Distribution Center, New York' },
      { status: 'Processing', timestamp: '2023-05-14 09:00', location: 'Sorting Facility, New Jersey' },
    ],
  },
  {
    id: 'PKG002',
    status: 'Delivered',
    estimatedArrival: '2023-05-14',
    currentLocation: 'Customer Address, Los Angeles',
    statusHistory: [
      { status: 'Delivered', timestamp: '2023-05-14 10:15', location: 'Customer Address, Los Angeles' },
      { status: 'Out for Delivery', timestamp: '2023-05-14 08:30', location: 'Local Courier, Los Angeles' },
      { status: 'In Transit', timestamp: '2023-05-13 20:00', location: 'Distribution Center, San Francisco' },
    ],
  },
]

export async function getPackageInfo(id: string): Promise<Package | null> {
  // In a real application, you would fetch this data from an API or database
  const packageInfo = packagesDatabase.find(pkg => pkg.id === id)
  return packageInfo || null
}


