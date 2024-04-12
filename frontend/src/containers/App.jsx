import React from "react"
import Navbar from "../components/Navbar"
import CurrentWeather from "./CurrentWeather"
import PersonDetails from "./PersonDetails"
import BeneficialOwners from "./BeneficialOwners"

function App() {
  return (
    <div className="app">
      <Navbar />
      <CurrentWeather />
      <PersonDetails />
      <BeneficialOwners />
    </div>
  )
}

export default App
