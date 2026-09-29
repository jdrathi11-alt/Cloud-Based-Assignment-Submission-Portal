const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function getErrorMessage(detail) {
  if (typeof detail === 'string') {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map(item => {
        if (typeof item === 'string') return item;
        return item?.msg || JSON.stringify(item);
      })
      .join(', ');
  }

  if (detail && typeof detail === 'object') {
    if (detail.msg) {
      return detail.msg;
    }

    if (detail.message) {
      return detail.message;
    }

    return JSON.stringify(detail);
  }

  return 'Request failed';
}

export async function api(
  path,
  { method = 'GET', body, token, form = false } = {}
) {
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  if (body && !form) {
    headers['Content-Type'] = 'application/json';
  }

  const r = await fetch(`${API}${path}`, {
    method,
    headers,
    body: form
      ? body
      : body
        ? JSON.stringify(body)
        : undefined,
  });

  const data = await r.json().catch(() => ({
    detail: r.statusText,
  }));

  if (!r.ok) {
    throw new Error(getErrorMessage(data.detail));
  }

  return data;
}

export async function downloadFile(id, token, name) {
  const r = await fetch(`${API}/api/submissions/${id}/download`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!r.ok) {
    throw new Error('Download failed');
  }

  const blob = await r.blob();
  const a = document.createElement('a');

  a.href = URL.createObjectURL(blob);
  a.download = name || 'submission';
  a.click();

  URL.revokeObjectURL(a.href);
}

export { API };