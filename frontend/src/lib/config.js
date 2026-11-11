/**
 * Resolves the Django REST backend base URL cleanly across local development
 * and production cloud hosting (Vercel + Render / Railway).
 */
export function getBackendUrl() {
  const raw =
    process.env.NEXT_PUBLIC_BACKEND_URL ||
    process.env.BACKEND_URL ||
    "http://127.0.0.1:8000";
  return raw.replace(/\/+$/, "");
}

export function backendApi(path) {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return `${getBackendUrl()}${normalized}`;
}
