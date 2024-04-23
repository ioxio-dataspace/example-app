import React, { useContext } from "react"
import DataspaceConfigurationContext from "../context/dataspaceConfigurationContext"

export default function DataProductLink({ definition }) {
  const dataspaceConfiguration = useContext(DataspaceConfigurationContext)

  return (
    <span>
      <a href={dataspaceConfiguration.definitionViewerUrl} target="_blank">
        {definition}
      </a>{" "}
      data product published under <strong>ioxio</strong> source on{" "}
      <a href={dataspaceConfiguration.dataspaceBaseUrl} target="_blank">
        {dataspaceConfiguration.dataspaceName}
      </a>
      .
    </span>
  )
}
