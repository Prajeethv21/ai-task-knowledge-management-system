const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    let message = response.statusText || "Request failed";
    const text = await response.text();
    if (text) {
      try {
        const data = JSON.parse(text);
        message = data?.detail || text;
      } catch {
        message = text;
      }
    }
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}
