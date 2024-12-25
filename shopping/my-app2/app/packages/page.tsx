import { SearchForm } from './components/SearchForm'
import { PackageInfo } from './components/PackageInfo'

export default function PackageTracking({
  searchParams
}: {
  searchParams: { id?: string }
}) {
  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Package Tracker</h1>
        <SearchForm initialId={searchParams.id} />
        <PackageInfo searchParams={searchParams} />
      </div>
    </div>
  )
}


