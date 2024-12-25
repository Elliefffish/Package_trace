import { getPackageInfo } from '../../actions'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
//import { Badge } from "@/components/ui/badge"

export async function PackageInfo({ searchParams }: { searchParams: { id?: string } }) {
  const packageId = searchParams?.id

  if (!packageId) {
    return null
  }

  const packageInfo = await getPackageInfo(packageId)

  if (!packageInfo) {
    return (
      <Card className="mt-8">
        <CardContent className="pt-6">
          <p className="text-center text-red-500">Package not found</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle className="flex justify-between items-center">
          <span>Package {packageInfo.id}</span>
          <span variant={packageInfo.status === 'Delivered' ? 'success' : 'default'}>{packageInfo.status}</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-500">Estimated Arrival: {packageInfo.estimatedArrival}</p>
        <p className="text-sm text-gray-500 mt-2">Current Location: {packageInfo.currentLocation}</p>
        <div className="mt-4">
          <h3 className="text-sm font-medium text-gray-900">Status History</h3>
          <ul className="mt-2 space-y-2">
            {packageInfo.statusHistory.map((update, index) => (
              <li key={index} className="text-sm">
                <p className="font-semibold">{update.status}</p>
                <p className="text-gray-500">{update.timestamp}</p>
                <p className="text-gray-500">{update.location}</p>
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}


