import React, {useEffect, useState} from 'react'
import { useParams, Link } from 'react-router-dom'
import { getMedicineBySlug, addToCart } from '../api'

export default function MedicineDetail(){
  const { slug } = useParams()
  const [medicine, setMedicine] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(()=>{
    getMedicineBySlug(slug).then(d=>{ setMedicine(d); setLoading(false) }).catch(e=>{ setError(e); setLoading(false) })
  },[slug])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error loading medicine.</div>
  if (!medicine) return <div>Not found</div>

  return (
    <div>
      <h2>{medicine.name}</h2>
      {medicine.image && <img src={medicine.image} alt={medicine.name} style={{maxWidth:300}} />}
      <p>{medicine.description}</p>
      <p>Price: {medicine.price}</p>
      <p>In stock: {medicine.in_stock ? 'Yes' : 'No'}</p>
      <button onClick={async ()=>{ try{ await addToCart(medicine.id); alert('Added to cart'); }catch(e){ alert('Add to cart failed: '+(e.data?.error||e.status)) } }}>Add to cart</button>
      <p><Link to="/medicines">Back</Link></p>
    </div>
  )
}
