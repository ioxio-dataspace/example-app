export default function LoginForm() {
  return (
    <div className="login-form">
      <div>
        <p>
          Some data sources require user to be authenticated before requesting the data.
        </p>
        <p>
          Authenticate yourself via Login Portal to see protected data. It doesn't
          require registration and it was implemented only for demo purposes.
        </p>
      </div>
      <a href="/api/login">Login</a>
    </div>
  )
}
