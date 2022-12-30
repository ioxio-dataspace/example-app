export async function fetchDataProduct(definition, source, params) {
  const resp = await fetch(`/api/data-product/${definition}?source=${source}`, {
    method: "POST",
    body: JSON.stringify(params),
  })
  return await resp.json()
}

export async function getUser() {
  const resp = await fetch(`/api/me`, {
    method: "GET",
  })
  return await resp.json()
}
