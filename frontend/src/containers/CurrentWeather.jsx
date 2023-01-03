import React, { useState } from "react"
import Box from "../components/Box"
import { fetchDataProduct } from "../utils"
import WeatherData from "../components/WeatherData"
import DataProductLink from "../components/DataProductLink"

const DEFINITION = "draft/Weather/Current/Metric"
const LOCATIONS = {
  Helsinki: [60.1699, 24.9384],
  Tokyo: [35.6762, 139.6503],
  Lisbon: [38.7223, 9.1393],
  "New York": [40.7128, 74.006],
}
const DEFAULT_CITY = "Helsinki"

export default function CurrentWeather() {
  const [location, setLocation] = useState(LOCATIONS[DEFAULT_CITY])
  const [lat, setLat] = useState(LOCATIONS[DEFAULT_CITY][0])
  const [lon, setLon] = useState(LOCATIONS[DEFAULT_CITY][1])

  const [isFetching, setIsFetching] = useState(false)
  const [weather, setWeather] = useState({})

  function updateCoords(event) {
    const city = event.target.value
    setLocation(city)
    setLat(LOCATIONS[city][0])
    setLon(LOCATIONS[city][1])
  }

  async function fetchWeather(event) {
    event.preventDefault()
    setIsFetching(true)
    const resp = await fetchDataProduct(DEFINITION, {
      lat: lat,
      lon: lon,
    })
    setWeather(resp)
    setIsFetching(false)
  }

  return (
    <Box definition={DEFINITION}>
      <div className="current-weather">
        <div className="main-box">
          <form onSubmit={fetchWeather}>
            <select onChange={updateCoords} value={location}>
              {Object.keys(LOCATIONS).map((city) => (
                <option key={city}>{city}</option>
              ))}
            </select>
            <div>
              <div>Latitude</div>
              <input value={lat} onChange={(e) => setLat(e.target.value)} />
            </div>
            <div>
              <div>Longitude</div>
              <input value={lon} onChange={(e) => setLon(e.target.value)} />
            </div>
            <button type="submit">Fetch</button>
          </form>
          <div>
            {isFetching && <i>Loading...</i>}
            {!isFetching && weather.temp !== undefined && (
              <WeatherData weather={weather} />
            )}
          </div>
        </div>
        <p>
          Weather Data Product uses public information and it doesn't require any
          authentication to fetch it.
        </p>
        <p>
          By clicking "Fetch", you will request data from{" "}
          <DataProductLink definition={DEFINITION} />
        </p>
      </div>
    </Box>
  )
}
