export async function fetchDataProduct(definition, params) {
  // In this application we use data products that are published under
  //  "ioxio" source only
  try {
    const resp = await fetch(`/api/data-product/${definition}?source=ioxio`, {
      method: "POST",
      body: JSON.stringify(params),
    })
    return await resp.json()
  } catch (err) {
    throw new Error("Failed to fetch a data product")
  }
}

export async function getUser() {
  try {
    const resp = await fetch(`/api/me`, {
      method: "GET",
    })
    return await resp.json()
  } catch (err) {
    throw new Error("Failed to fetch a user")
  }
}
