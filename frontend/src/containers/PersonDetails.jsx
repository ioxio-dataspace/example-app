import React, { useEffect, useState } from "react"
import Box from "../components/Box"
import LoginForm from "../components/LoginForm"
import { fetchDataProduct, getUser } from "../utils"
import DataProductLink from "../components/DataProductLink"

const DEFINITION = "Person/Details_v1.0"

export default function PersonDetails() {
  const [user, setUser] = useState({ loggedIn: false })
  const [personDetails, setPersonDetails] = useState({})
  const [isPersonFetching, setIsPersonFetching] = useState(false)
  const [isUserLoading, setIsUserLoading] = useState(false)

  // fetch user on page load
  useEffect(() => {
    setIsUserLoading(true)
    getUser().then((data) => {
      setUser(data)
      setIsUserLoading(false)
    })
    return () => {}
  }, [])

  // once we ensure user is logged in, fetch data product automatically
  useEffect(() => {
    if (!user.loggedIn) {
      return
    }
    setIsPersonFetching(true)
    fetchDataProduct(DEFINITION, {}).then((resp) => {
      if (resp.ok) {
        setPersonDetails(resp.data)
      } else {
        throw new Error("Failed to fetch person details")
      }
      setIsPersonFetching(false)
    })
    return () => {}
  }, [user])

  if (isUserLoading) {
    return (
      <Box title={"Authentication"}>
        <i>Loading...</i>
      </Box>
    )
  } else if (!user.loggedIn) {
    return (
      <Box title={"Authentication"}>
        <LoginForm />
      </Box>
    )
  }

  return (
    <Box title={"Authentication"}>
      <div className="user-navbar">
        <div>Logged in as {user.email}</div>
        <a href="/api/logout">Logout</a>
      </div>
      {isPersonFetching && <i>Fetching user information...</i>}
      {!isPersonFetching && (
        <div>
          <div>
            <b>Name:</b> {personDetails.name}
          </div>
          <div>
            <b>Address:</b> {personDetails.address}
          </div>
        </div>
      )}
      <div>
        <p>User profile data is available only for authenticated users</p>
        <p>
          Profile data is fake data generated uniquely for the given email address. It's
          fetched automatically from <DataProductLink definition={DEFINITION} />
        </p>
      </div>
    </Box>
  )
}
