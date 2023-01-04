import React from "react"

export default function Box({ children, title }) {
  return (
    <div className="box-component">
      <div className="title">{title} demo</div>
      <div className="body">{children}</div>
    </div>
  )
}
