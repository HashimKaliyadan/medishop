import React, {useState} from 'react'
import { checkout, getCart } from '../api'
import { useNavigate } from 'react-router-dom'

export default function Checkout(){
  const [form, setForm] = useState({ line1:'', line2:'', city:'', pincode:'', phone:'' })
  const [prescription, setPrescription] = useState(null)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    const fd = new FormData()
    fd.append('line1', form.line1)
    fd.append('line2', form.line2)
    fd.append('city', form.city)
    fd.append('pincode', form.pincode)
    fd.append('phone', form.phone)
    if (prescription) fd.append('prescription', prescription)

    try{
      const res = await checkout(fd)
      alert('Order placed')
      navigate('/')
    }catch(e){
      setError(e.data?.error || 'Checkout failed')
    }
  }

  return (
    <div>
      <h2>Checkout</h2>
      {error && <div style={{color:'red'}}>{error}</div>}
      <form onSubmit={submit}>
        <div>
          <label>Line1</label>
          <input value={form.line1} onChange={e=>setForm({...form, line1:e.target.value})} />
        </div>
        <div>
          <label>Line2</label>
          <input value={form.line2} onChange={e=>setForm({...form, line2:e.target.value})} />
        </div>
        <div>
          <label>City</label>
          <input value={form.city} onChange={e=>setForm({...form, city:e.target.value})} />
        </div>
        <div>
          <label>Pincode</label>
          <input value={form.pincode} onChange={e=>setForm({...form, pincode:e.target.value})} />
        </div>
        <div>
          <label>Phone</label>
          <input value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} />
        </div>
        <div>
          <label>Prescription (file)</label>
          <input type="file" onChange={e=>setPrescription(e.target.files[0])} />
        </div>
        <button type="submit">Place order</button>
      </form>
    </div>
  )
}
