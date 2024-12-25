import { getPackageInfo } from '@/app/actions'
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
          <span>Package {packageInfo.package_id}</span>
          <span>{packageInfo.status}</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-500">Time: {packageInfo.status_time.split('T')[0]}</p>
        <p className="text-sm text-gray-500 mt-2">Current Location: {packageInfo.place}</p>
      </CardContent>
    </Card>
  )
}


