from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_presets() -> None:
    response = client.get("/api/redact/presets")
    assert response.status_code == 200
    assert any(item["name"] == "passport" for item in response.json()["items"])


def test_redact_image_returns_audit_id() -> None:
    image = Image.new("RGB", (640, 480), color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    payload = buffer.getvalue()

    response = client.post(
        "/api/redact/image",
        files={"file": ("sample.png", payload, "image/png")},
        data={"preset": "invoice"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["audit_id"]
    assert body["preset"] == "invoice"
    assert len(body["redaction_boxes"]) >= 1
