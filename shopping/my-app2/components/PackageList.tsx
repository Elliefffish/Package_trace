'use client'

import { useState } from 'react'
import { Package } from '../types'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

export function PackageList({ initialPackages }: { initialPackages: Package[] }) {
  const [packages, setPackages] = useState(initialPackages)

  return (
    <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {packages.map((pkg) => (
        <Card key={pkg.id}>
          <CardHeader>
            <CardTitle className="flex justify-between items-center">
              <span>Package {pkg.id}</span>
              <Badge variant={pkg.statusHistory[0].status === 'Delivered' ? 'success' : 'default'}>
                {pkg.statusHistory[0].status}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-500 mb-2">Estimated Arrival: {pkg.estimatedArrival}</p>
            <Accordion type="single" collapsible className="w-full">
              <AccordionItem value="status-history">
                <AccordionTrigger>View Status History</AccordionTrigger>
                <AccordionContent>
                  <ul className="space-y-2">
                    {pkg.statusHistory.map((update, index) => (
                      <li key={index} className="text-sm">
                        <p className="font-semibold">{update.status}</p>
                        <p className="text-gray-500">{update.timestamp}</p>
                        <p className="text-gray-500">{update.location}</p>
                      </li>
                    ))}
                  </ul>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}


