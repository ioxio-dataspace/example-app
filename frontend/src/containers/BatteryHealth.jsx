import React, { useEffect, useState } from "react"
import Box from "../components/Box"
import { fetchDataProduct } from "../utils"
import DataProductLink from "../components/DataProductLink"

// Data definition and source to use in this example
const DEFINITION = "DigitalProductPassport/Battery/HealthData_v0.2"
const SOURCE = "dpp_demo:access_control_demo"

// in this app we will just use the hardcoded data as parameters
const PRODUCT = "lithium-ion"
const ID = "660e8400-e29b"

export default function BatteryHealth() {
  const [batteryHealthData, setBatteryHealthData] = useState({
    status: "",
    manufacturingDate: "",
  })
  const [isLoading, setIsLoading] = useState(false)

  // once we ensure user is logged in, fetch data product automatically
  useEffect(() => {
    ;(async () => {
      try {
        setIsLoading(true)
        const resp = await fetchDataProduct(
          DEFINITION,
          {
            product: PRODUCT,
            id: ID,
          },
          false,
          SOURCE
        )
        if (resp.ok) {
          setBatteryHealthData(resp.data)
        } else {
          throw new Error("Failed to fetch battery health data")
        }
      } finally {
        setIsLoading(false)
      }
      return () => {}
    })()
  }, [])

  if (isLoading) {
    return (
      <Box title={"Access control keys"}>
        <i>Loading...</i>
      </Box>
    )
  }

  return (
    <Box title={"Access control keys"}>
      <div>
        Battery health data for battery {PRODUCT} / {ID}:
      </div>
      <ul>
        <li>
          <b>Status:</b> {batteryHealthData.status}
        </li>
        <li>
          <b>Manufacturing date:</b> {batteryHealthData.manufacturingDate}
        </li>
      </ul>
      <div>
        <p>
          This data is available only with an application's private access control key,
          and an API token fetched with it.
        </p>
        <p>
          This is mock data generated for demo purposes only. It's fetched automatically
          from <DataProductLink definition={DEFINITION} />
        </p>
      </div>
    </Box>
  )
}
