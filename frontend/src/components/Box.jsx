import React from "react"

export default function Box({ children, definition }) {
  return (
    <div className="box-component">
      <div className="title">
        <b>{definition}</b> demo
      </div>
      <div className="body">{children}</div>
    </div>
  )
}
