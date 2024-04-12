import github from "../assets/github.svg"

export default function Navbar() {
  return (
    <div className="nav">
      <a
        className="nav-link"
        href="https://github.com/ioxio-dataspace/example-app"
        rel="noreferrer"
        target="_blank"
      >
        <img className="nav-logo" src={github} alt="View source in GitHub" />
      </a>
    </div>
  )
}
