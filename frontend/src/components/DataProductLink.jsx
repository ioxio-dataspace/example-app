import React, { useContext } from "react"
import DataspaceConfigurationContext from "../context/dataspaceConfigurationContext"

export default function DataProductLink({ definition }) {
  const dataSpaceConfiguration = useContext(DataspaceConfigurationContext)

  return (
    <span>
      <a href={dataSpaceConfiguration.definitionViewerUrl} target="_blank">
        {definition}
      </a>{" "}
      data product published under <strong>ioxio</strong> source on{" "}
      <a href={dataSpaceConfiguration.dataspaceBaseUrl} target="_blank">
        IOXIO Sandbox
      </a>{" "}
      dataspace.
    </span>
  )
}
