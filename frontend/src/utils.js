export async function fetchDataProduct(definition, params) {
  // In this application we use data products that are published under
  //  "ioxio" source only
  const resp = await fetch(`/api/data-product/${definition}?source=ioxio`, {
    method: "POST",
    body: JSON.stringify(params),
  })
  if (!resp.ok) {
    throw new Error("Failed to fetch a data product")
  }
  return await resp.json()
}

export async function getUser() {
  const resp = await fetch(`/api/me`, {
    method: "GET",
  })
  if (!resp.ok) {
    throw new Error("Failed to fetch the current user")
  }
  return await resp.json()
}
