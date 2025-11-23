const API_BASE = "http://localhost:8000"; // ← backend コンテナをホスト側からアクセス

let accessToken = null;
let refreshToken = null;

export function setTokens(access, refresh) {
    accessToken = access;
    refreshToken = refresh;
}

async function refreshAccessToken() {
    const res = await fetch(`${API_BASE}/api/auth/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken })
    });
    if (!res.ok) throw new Error("refresh failed");
    const data = await res.json();
    accessToken = data.access;
    return data.access;
}

export async function api(url, options = {}) {
    options.headers = options.headers || {};
    if (accessToken) options.headers["Authorization"] = `Bearer ${accessToken}`;

    let res = await fetch(`${API_BASE}${url}`, options);

    if (res.status === 401 && refreshToken) {
        const newAccess = await refreshAccessToken();
        options.headers["Authorization"] = `Bearer ${newAccess}`;
        res = await fetch(`${API_BASE}${url}`, options);
    }

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`API request failed: ${res.status} ${text}`);
    }

    return res;
}




//api.js