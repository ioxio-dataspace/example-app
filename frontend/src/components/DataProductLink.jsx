import React, { useContext } from "react"
import DataspaceConfigurationContext from "../context/dataspaceConfigurationContext"

export default function DataProductLink({ definition }) {
  const dataSpaceConfiguration = useContext(DataspaceConfigurationContext)
  const linkToDefinition = `https://definitions.${dataSpaceConfiguration.dataspaceBaseDomain}/definitions/${definition}`
  const linkToDataspace = `https://${dataSpaceConfiguration.dataspaceBaseDomain}`

  return (
    <span>
      <a href={linkToDefinition} target="_blank">
        {definition}
      </a>{" "}
      data product published under <strong>ioxio</strong> source on{" "}
      <a href={linkToDataspace} target="_blank">
        IOXIO Sandbox
      </a>{" "}
      dataspace.
    </span>
  )
}
