import React from "react"
import settings from "../settings"

export default function DataProductLink({ definition }) {
  const link = `${settings.DATA_DEFINITION_VIEWER_URL}/definitions/${definition}`
  return (
    <span>
      <a href={link}>{definition}</a> data product published under{" "}
      <strong>ioxio</strong> source on{" "}
      <a href={settings.IOXIO_SANDBOX_DATASPACE_URL}>IOXIO Sandbox</a> dataspace.
    </span>
  )
}
