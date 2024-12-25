export interface StatusUpdate {
  status: string
  timestamp: string
  location: string
}

export interface Package {
  id: string
  status: string
  estimatedArrival: string
  currentLocation: string
  statusHistory: StatusUpdate[]
}


