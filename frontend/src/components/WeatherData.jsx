export default function WeatherData({ weather }) {
  function formatTemp(t) {
    const sign = t > 0 ? "+" : ""
    return sign + t.toFixed(1) + " °C"
  }

  function formatWind(ws) {
    return ws.toFixed(1) + " m/s"
  }

  function formatHumidity(h) {
    return Math.round(h) + "%"
  }

  return (
    <div className="data">
      <div>Temp: {formatTemp(weather.temp)}</div>
      <div>{weather.rain ? "Rain" : "No rain"}</div>
      <div>Humidity: {formatHumidity(weather.humidity)}</div>
      <div>Wind: {formatWind(weather.windSpeed)}</div>
    </div>
  )
}
