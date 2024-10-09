import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
  Routes,
  Navigate
} from "react-router-dom";


import Menu from './components/Menu.jsx'
import Layout from './components/admin/Layout.jsx'
import Dashboard from './components/admin/Dashboard.jsx'
import MenuManager from './components/admin/MenuManager.jsx';
import Orderlist from './components/admin/Orderlist.jsx';
import Cart from './components/Cart.jsx';
 
 
 



const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Menu />} />
      <Route path="/cart" element={<Cart />} />
      
      <Route path="admin" element={<Layout />}>
        <Route index element={<Navigate to="dashboard" />} /> {/* Redirect to dashboard */}
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="menu" element={<MenuManager />} />
        <Route path="orders" element={<Orderlist />} />       
      </Route>
      
    </Route>
  )
);


function App() {
  return (
 
    <>
      <RouterProvider router={router} />

    </>
  );
}

export default App;