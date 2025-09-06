const API_BASE_URL = import.meta.env.VITE_API_URL

const defaultOptions: RequestInit = {
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  credentials: 'include',
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, {
      ...defaultOptions,
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`)
    }

    return (await response.json()) as T
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}

export default request
