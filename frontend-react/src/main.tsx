import React from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./ui/App";
import Success from "./ui/Success";

// keep this import only if you actually have it
// otherwise remove it to avoid a runtime error
// import "./styles.css";

const rootEl = document.getElementById("root");
if (!rootEl) throw new Error("Root element #root not found in index.html");

createRoot(rootEl).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/success" element={<Success />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
