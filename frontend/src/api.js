const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

async function request(path, opts = {}){
  const url = `${API_BASE}${path}`
  const fetchOpts = Object.assign({
    headers: { 'Accept': 'application/json' },
    credentials: 'include'
  }, opts)

  if (fetchOpts.body && !(fetchOpts.body instanceof FormData)){
    fetchOpts.headers['Content-Type'] = 'application/json'
    fetchOpts.body = JSON.stringify(fetchOpts.body)
  }

  const res = await fetch(url, fetchOpts)
  const contentType = res.headers.get('content-type') || ''
  const data = contentType.includes('application/json') ? await res.json() : null
  if (!res.ok) throw { status: res.status, data }
  return data
}

export async function getMedicines(query = ''){
  const q = query ? `?q=${encodeURIComponent(query)}` : ''
  return request(`/medicines/${q}`)
}

export async function getMedicineBySlug(slug){
  return request(`/medicines/${slug}/`)
}

export async function getCategories(){
  return request('/categories/')
}

export async function getCart(){
  return request('/cart/')
}

export async function addToCart(medicine_id){
  return request('/cart/add/', { method: 'POST', body: { medicine_id } })
}

export async function updateCartItem(item_id, quantity){
  return request('/cart/update/', { method: 'POST', body: { item_id, quantity } })
}

export async function removeCartItem(item_id){
  return request('/cart/remove/', { method: 'POST', body: { item_id } })
}

export async function checkout(formData){
  // formData is a FormData instance
  return request('/checkout/', { method: 'POST', body: formData })
}
