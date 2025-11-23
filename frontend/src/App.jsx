import { useState } from "react";
import Login from "./Login";
import TodoList from "./TodoList";

export default function App() {
    const [loggedIn, setLoggedIn] = useState(false);

    return (
        <div style={{ padding: "20px" }}>
            {loggedIn ? (
                <TodoList logout={() => setLoggedIn(false)} />
            ) : (
                <Login onLogin={() => setLoggedIn(true)} />
            )}
        </div>
    );
}


//App.jsx