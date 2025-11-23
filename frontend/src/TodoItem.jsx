import { api } from "./api";

export default function TodoItem({ item, onChanged }) {
    async function toggle() {
        await api(`/api/todos/${item.id}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ...item,
                completed: !item.completed
            })
        });
        onChanged();
    }

    async function remove() {
        await api(`/api/todos/${item.id}/`, { method: "DELETE" });
        onChanged();
    }

    return (
        <div>
            <input type="checkbox" checked={item.completed} onChange={toggle} />
            {item.title}
            <button onClick={remove}>削除</button>
        </div>
    );
}


//TodoItem.jsx