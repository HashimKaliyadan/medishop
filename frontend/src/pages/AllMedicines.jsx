import React, {useEffect, useState} from 'react'
import { Link } from 'react-router-dom'
import { getMedicines } from '../api'

export default function AllMedicines(){
  const [medicines, setMedicines] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    getMedicines().then(data=>{ setMedicines(data); setLoading(false) }).catch(()=>setLoading(false))
  },[])

  if (loading) return <div>Loading...</div>
  return (
    <div>
      <h2>Medicines</h2>
      <ul>
        {medicines.map(m=> (
          <li key={m.id}>
            <Link to={`/medicines/${m.slug}`}>{m.name}</Link> — {m.price}
          </li>
        ))}
      </ul>
    </div>
  )
}
