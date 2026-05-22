const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export function authHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}
