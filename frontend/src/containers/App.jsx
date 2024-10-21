import React, { useEffect, useState } from "react"
import Navbar from "../components/Navbar"
import CurrentWeather from "./CurrentWeather"
import PersonDetails from "./PersonDetails"
import BeneficialOwners from "./BeneficialOwners"
import BatteryHealth from "./BatteryHealth"
import { getDataspaceConfiguration } from "../utils.js"
import DataspaceConfigurationContext from "../context/dataspaceConfigurationContext"

function App() {
  const [dataspaceConfiguration, setDataspaceConfiguration] = useState({
    dataspaceBaseUrl: "https://sandbox.ioxio-dataspace.com",
    consentPortalUrl: "https://consent.sandbox.ioxio-dataspace.com",
    definitionViewerUrl: "https://definitions.sandbox.ioxio-dataspace.com",
    dataspaceName: "IOXIO Sandbox Dataspace",
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
        <Navbar />
        <CurrentWeather />
        <PersonDetails />
        <BeneficialOwners />
        <BatteryHealth />
      </div>
    </DataspaceConfigurationContext.Provider>
  )
}

export default App
