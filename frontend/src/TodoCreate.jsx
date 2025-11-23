import { useState } from "react";
import { api } from "./api";

export default function TodoCreate({ onCreated }) {
    const [title, setTitle] = useState("");

    async function create() {
        await api("/api/todos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title })
        });
        setTitle("");
        onCreated();
    }

    return (
        <div>
            <input value={title} onChange={e => setTitle(e.target.value)} placeholder="タイトル" />
            <button onClick={create}>追加</button>
        </div>
    );
}


//TodoCreate.jsx