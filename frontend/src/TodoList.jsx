// frontend/src/TodoList.jsx
import { useEffect, useState } from "react";
import { api } from "./api";
import TodoCreate from "./TodoCreate";
import TodoItem from "./TodoItem";

export default function TodoList({ logout }) {
    const [todos, setTodos] = useState([]);
    const [loading, setLoading] = useState(false);

    async function load() {
        setLoading(true);
        try {
            const res = await api("/api/todos/");
            const data = await res.json();
            setTodos(data);
        } catch (err) {
            console.error("Failed to load todos:", err);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        const loadTodos = async () => await load();
        loadTodos();
    }, []);

    return (
        <div>
            <button onClick={logout}>ログアウト</button>
            <h2>ToDo 一覧</h2>
            <TodoCreate onCreated={load} />
            {loading ? (
                <p>読み込み中...</p>
            ) : (
                todos.map(t => <TodoItem key={t.id} item={t} onChanged={load} />)
            )}
        </div>
    );
}
