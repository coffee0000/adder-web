import React, { useEffect } from "react";
import ReactDOM from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom";
import { initializeIcons } from "@fluentui/react";

import "./index.css";

import Plus from "./pages/plus/Plus";
import NoPage from "./pages/NoPage";

initializeIcons();

export default function App() {
    useEffect(() => {
        document.title = "calculate";
    }, []);

    return (
        <HashRouter>
            <Routes>
                <Route path="/" element={<Plus />} />
            </Routes>
        </HashRouter>
    );
}

const rootElement = document.getElementById("root");
if (rootElement) {
    ReactDOM.createRoot(rootElement).render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    );
} else {
    console.error("Root element not found!");
}