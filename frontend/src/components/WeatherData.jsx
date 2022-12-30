export default function WeatherData({ weather }) {
  function formatTemp(t) {
    const sign = t > 0 ? "+" : ""
    return sign + Math.round(t * 10) / 10 + " °C"
  }

  function formatWind(ws) {
    return Math.round(ws * 10) / 10 + " m/s"
  }

  return (
    <div className="data">
      <div>Temp: {formatTemp(weather.temp)}</div>
      <div>{weather.rain ? "Rain" : "No rain"}</div>
      <div>Humidity: {Math.floor(weather.humidity)} %</div>
      <div>Wind: {formatWind(weather.windSpeed)}</div>
    </div>
  )
}
