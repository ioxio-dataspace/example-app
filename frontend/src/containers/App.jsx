import React from "react"
import CurrentWeather from "./CurrentWeather"
import PersonDetails from "./PersonDetails"
import BeneficialOwners from "./BeneficialOwners"

function App() {
  return (
    <div className="app">
      <CurrentWeather />
      <PersonDetails />
      <BeneficialOwners />
    </div>
  )
}

export default App
