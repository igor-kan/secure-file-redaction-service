import React, { useState } from "react";
import { createRoot } from "react-dom/client";

function App() {
  const [file, setFile] = useState(null);
  const [img, setImg] = useState("");
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    setImg("");

    if (!file) {
      setError("Choose an image first.");
      return;
    }

    const form = new FormData();
    form.append("file", file);

    try {
      const response = await fetch("http://localhost:8030/api/redact/image", {
        method: "POST",
        body: form
      });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      const data = await response.json();
      setImg(`data:image/png;base64,${data.image_base64_png}`);
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <main style={{ maxWidth: 760, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Secure File Redaction Service</h1>
      <form onSubmit={submit}>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <button type="submit" style={{ marginLeft: 8 }}>Redact</button>
      </form>
      {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
      {img ? <img src={img} alt="Redacted output" style={{ marginTop: 16, maxWidth: "100%" }} /> : null}
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
