export async function getUser() {
  const resp = await fetch(`/api/me`, {
    method: "GET",
  })
  if (!resp.ok) {
    throw new Error("Failed to fetch the current user")
  }
  return await resp.json()
}

export async function fetchDataProduct(
  definition,
  params,
  consent = false,
  source = "ioxio"
) {
  // There is a different API endpoint for data products that require a consent
  const api = consent ? "/api/data-product-consent" : "/api/data-product"
  const resp = await fetch(`${api}/${definition}?source=${source}`, {
    method: "POST",
    body: JSON.stringify(params),
  })
  return {
    ok: resp.ok,
    status: resp.status,
    data: await resp.json(),
  }
}

export async function getDataspaceConfiguration() {
  const resp = await fetch("/api/settings")
  if (!resp.ok) {
    throw new Error("Failed to fetch the dataspace configuration")
  }
  return await resp.json()
}
