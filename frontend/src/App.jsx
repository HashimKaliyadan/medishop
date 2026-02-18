import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import AllMedicines from './pages/AllMedicines'
import MedicineDetail from './pages/MedicineDetail'
import Cart from './pages/Cart'
import Checkout from './pages/Checkout'

export default function App(){
  return (
    <BrowserRouter>
      <header style={{padding: '1rem', borderBottom: '1px solid #eee'}}>
        <nav style={{display:'flex', gap:12}}>
          <Link to="/">Home</Link>
          <Link to="/medicines">Medicines</Link>
          <Link to="/cart">Cart</Link>
        </nav>
      </header>
      <main style={{padding: '1rem'}}>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/medicines" element={<AllMedicines/>} />
          <Route path="/medicines/:slug" element={<MedicineDetail/>} />
          <Route path="/cart" element={<Cart/>} />
          <Route path="/checkout" element={<Checkout/>} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
