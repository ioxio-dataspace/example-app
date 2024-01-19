import React, { useEffect, useState } from "react"
import Box from "../components/Box"
import LoginForm from "../components/LoginForm"
import { fetchDataProduct, getUser } from "../utils"
import DataProductLink from "../components/DataProductLink"
import conf from "../settings"

const DEFINITION = "Employment/WorkContract_v0.3"
// in this app we will just use the hardcoded data as a parameter
const COMPANY_ID = "5590379409"

export default function BeneficialOwners() {
  const [user, setUser] = useState({ loggedIn: false })
  const [ownersData, setOwnersData] = useState({ shareholders: [] })
  const [isLoading, setIsLoading] = useState(false)
  const [verifyConsentUrl, setVerifyConsentUrl] = useState("")
  // fetch user on page load
  useEffect(() => {
    setIsLoading(true)
    getUser().then((data) => {
      setUser(data)
      setIsLoading(false)
    })
    return () => {}
  }, [])

  // once we ensure user is logged in, fetch data product automatically
  useEffect(() => {
    ;(async () => {
      if (!user.loggedIn) {
        return
      }
      setIsLoading(true)
      const resp = await fetchDataProduct(
        DEFINITION,
        {
          nationalIdentifier: COMPANY_ID,
        },
        true
      ) // consent=true
      if (resp.ok) {
        setOwnersData(resp.data)
      }
      // data product requires a consent
      else if (resp.status === 403) {
        const currentUrl = window.location.href.split("?")[0]
        setVerifyConsentUrl(`${resp.data.verifyUrl}?returnUrl=${currentUrl}`)
      } else {
        throw new Error("Failed to fetch beneficial owners")
      }
      setIsLoading(false)
      return () => {}
    })()
  }, [user])

  function onRequestConsentClick() {
    window.location.href = verifyConsentUrl
  }

  if (isLoading) {
    return (
      <Box title={"Consent"}>
        <i>Loading...</i>
      </Box>
    )
  } else if (!user.loggedIn) {
    return (
      <Box title={"Consent"}>
        <LoginForm />
      </Box>
    )
  } else if (verifyConsentUrl !== "") {
    return (
      <Box title={"Consent"}>
        <div>
          Some data sources can require a consent from a user to return the data.
        </div>
        <div>
          By clicking the button below you will be redirected to Consent Portal for
          approving or denying the consent.
        </div>
        <button onClick={onRequestConsentClick}>Request consent</button>
      </Box>
    )
  }

  return (
    <Box title={"Consent"}>
      <div className="user-navbar">
        <div>Logged in as {user.email}</div>
        <a href="/api/logout">Logout</a>
      </div>
      <div>Beneficial Owners of company {COMPANY_ID}:</div>
      {ownersData.shareholders.map((s) => (
        <ul key={s.name}>
          <li>
            <strong>{s.name}</strong>
          </li>
          <div>Shares: </div>
          {s.shareOwnership.map((shares, i) => (
            <div key={s.name + i}>
              {shares.shareSeriesClass} - {shares.quantity}
            </div>
          ))}
        </ul>
      ))}
      <div>
        <p>
          This data is available only for users who granted this application a consent
          to view this data.
        </p>
        <p>
          You can manage your consents at{" "}
          <a href={conf.CONSENT_PORTAL_URL} target="_blank">
            Consent Portal
          </a>
          . For example, you can revoke it.
        </p>
        <p>
          This is mock data generated for demo purposes only. It's fetched automatically
          from <DataProductLink definition={DEFINITION} />
        </p>
      </div>
    </Box>
  )
}
