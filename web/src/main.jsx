import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

const API_BASE = "http://localhost:8030";

function App() {
  const [file, setFile] = useState(null);
  const [img, setImg] = useState("");
  const [error, setError] = useState("");
  const [preset, setPreset] = useState("generic");
  const [customBoxes, setCustomBoxes] = useState("[[50,50,300,120]]");
  const [auditId, setAuditId] = useState("");
  const [presets, setPresets] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/redact/presets`)
      .then((response) => response.json())
      .then((payload) => {
        setPresets(payload.items);
      })
      .catch(() => {
        setPresets([{ name: "generic", boxes: [] }]);
      });
  }, []);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setImg("");
    setAuditId("");

    if (!file) {
      setError("Choose an image first.");
      return;
    }

    const form = new FormData();
    form.append("file", file);
    form.append("preset", preset);

    if (customBoxes.trim()) {
      form.append("boxes", customBoxes);
    }

    try {
      const response = await fetch(`${API_BASE}/api/redact/image`, {
        method: "POST",
        body: form
      });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      const data = await response.json();
      setAuditId(data.audit_id);
      setImg(`data:image/png;base64,${data.image_base64_png}`);
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <main style={{ maxWidth: 860, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Secure File Redaction Service</h1>
      <form onSubmit={submit}>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <select value={preset} onChange={(e) => setPreset(e.target.value)} style={{ marginLeft: 8 }}>
          {presets.map((item) => (
            <option key={item.name} value={item.name}>
              {item.name}
            </option>
          ))}
        </select>
        <button type="submit" style={{ marginLeft: 8 }}>Redact</button>

        <div style={{ marginTop: 10 }}>
          <label>
            Custom Boxes JSON
            <input
              style={{ marginLeft: 8, width: 420 }}
              value={customBoxes}
              onChange={(e) => setCustomBoxes(e.target.value)}
              placeholder="[[x1,y1,x2,y2], ...]"
            />
          </label>
        </div>
      </form>

      {auditId ? <p>Audit ID: {auditId}</p> : null}
      {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
      {img ? <img src={img} alt="Redacted output" style={{ marginTop: 16, maxWidth: "100%" }} /> : null}
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
