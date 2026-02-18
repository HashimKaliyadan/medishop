import React, {useEffect, useState} from 'react'
import { getCart, updateCartItem, removeCartItem } from '../api'

export default function Cart(){
  const [cart, setCart] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const load = ()=>{
    setLoading(true)
    getCart().then(d=>{ setCart(d); setLoading(false) }).catch(e=>{ setError(e); setLoading(false) })
  }

  useEffect(()=>{ load() },[])

  if (loading) return <div>Loading cart...</div>
  if (error) return <div>Unable to load cart (are you logged in?).</div>
  if (!cart) return <div>No cart</div>

  return (
    <div>
      <h2>Your Cart</h2>
      <ul>
        {cart.items.map(item=> (
          <li key={item.id}>
            {item.medicine.name} — {item.quantity} — {item.line_total}
            <div>
              <button onClick={async ()=>{ await updateCartItem(item.id, item.quantity+1); load() }}>+1</button>
              <button onClick={async ()=>{ await updateCartItem(item.id, item.quantity-1); load() }}>-1</button>
              <button onClick={async ()=>{ await removeCartItem(item.id); load() }}>Remove</button>
            </div>
          </li>
        ))}
      </ul>
      <p>Total: {cart.total}</p>
    </div>
  )
}
