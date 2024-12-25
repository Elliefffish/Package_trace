type Goods = {
  good_id: number
  name: string
  price: number
  image: string
  description: string

}
type Package = {
  package_id: number
  place: string
  status: string
  status_time: string
}
type Status = {
    status_id: number
    status:  string
    status_time:  string
    package_id: number
}

// 變數
var api = "http://127.0.0.1:8000/"

export async function getGoods(): Promise<Goods[]> {
  // Replace this with an actual API call to your server
  /*
  return [
    { id: 1, name: 'Goods 1', price: 10.99, image: '/placeholder.svg' },
    { id: 2, name: 'Goods 2', price: 19.99, image: '/placeholder.svg' },
    { id: 3, name: 'Goods 3', price: 5.99, image: '/placeholder.svg' },
  ]
  */
  const response = await fetch( api + 'goods', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch orders: ${response.statusText}`);
  }

  return response.json();
}

export async function createpackage(package_id: number, status_id:number
				   ): Promise<Package> {
  // Replace this with an actual API call to your server
  /*
  const product = await getProducts().then(products => products.find(p => p.id === productId))
  if (!product) throw new Error('Product not found')

  return {
    id: Math.floor(Math.random() * 1000),
    productName: product.name,
    orderTime: new Date().toISOString(),
    status: 'processing',
    statusUpdateTime: new Date().toISOString(),
    store,
  }
  */
  const response = await fetch( api + 'packages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ package_id, status_id }),
  });

   if (!response.ok) {
    //const errorDetails = await response.json();
    //console.error("Error details:", errorDetails);
    throw new Error(`Failed to create order: ${response.statusText}`);
  }

  return response.json();
}

export async function getpackages(id: string): Promise<Package> {
  // Replace this with an actual API call to your server
  /*
  return [
    {
      id: 1,
      goodName: 'Goods 1',
      packageTime: new Date().toISOString(),
      status: 'processing',
      statusUpdateTime: new Date().toISOString(),
      store: 'FamilyMart',
    },
    {
      id: 2,
      goodName: 'Goods 2',
      packageTime: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
      status: 'shipping',
      statusUpdateTime: new Date().toISOString(),
      store: '7-11',
    },
  ]
  */

  const response = await fetch( api + 'packages/'+id , {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch orders: ${response.statusText}`);
  }

  return response.json();

}

export async function getstatus(): Promise<Status[]> {

  const response = await fetch( api + 'packages', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch orders: ${response.statusText}`);
  }

  return response.json();

}

