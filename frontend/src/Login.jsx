import { useState } from "react";
import { setTokens } from "./api";

export default function Login({ onLogin }) {
    const [u, setU] = useState("");
    const [p, setP] = useState("");
    const [error, setError] = useState("");

    async function login() {
        const res = await fetch("/api/auth/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: u, password: p })
        });
        if (!res.ok) return setError("ログイン失敗");
        const data = await res.json();
        setTokens(data.access, data.refresh);
        onLogin();
    }

    return (
        <div>
            <h2>ログイン</h2>
            <input placeholder="username" value={u} onChange={(e) => setU(e.target.value)} />
            <input placeholder="password" type="password" value={p} onChange={(e) => setP(e.target.value)} />
            <button onClick={login}>ログイン</button>
            {error && <p>{error}</p>}
        </div>
    );
}


//Login.jsx