import React, { useEffect, useState } from "react"
import CurrentWeather from "./CurrentWeather"
import PersonDetails from "./PersonDetails"
import BeneficialOwners from "./BeneficialOwners"
import { getDataspaceConfiguration } from "../utils.js"
import DataspaceConfigurationContext from "../context/dataspaceConfigurationContext"

function App() {
  const [dataspaceConfiguration, setDataspaceConfiguration] = useState({
    dataspaceBaseDomain: "sandbox.ioxio-dataspace.com",
  })

  useEffect(() => {
    async function fetchData() {
      const data = await getDataspaceConfiguration()
      setDataspaceConfiguration(data)
    }
    fetchData()
  }, [])

  return (
    <DataspaceConfigurationContext.Provider value={dataspaceConfiguration}>
      <div className="app">
        <CurrentWeather />
        <PersonDetails />
        <BeneficialOwners />
      </div>
    </DataspaceConfigurationContext.Provider>
  )
}

export default App
