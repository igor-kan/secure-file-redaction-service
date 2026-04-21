import base64
import json
from io import BytesIO
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from PIL import Image, ImageDraw

app = FastAPI(title="Secure File Redaction Service")

PRESETS = {
    "passport": [[60, 80, 420, 150], [60, 220, 300, 270]],
    "invoice": [[80, 90, 420, 130], [80, 200, 350, 260]],
    "generic": [],
}


def normalize_boxes(boxes: list[list[int]], width: int, height: int) -> list[list[int]]:
    normalized = []
    for box in boxes:
        if len(box) != 4:
            raise HTTPException(status_code=400, detail="invalid_redaction_box")
        x1, y1, x2, y2 = [int(value) for value in box]
        x1 = max(0, min(x1, width - 1))
        y1 = max(0, min(y1, height - 1))
        x2 = max(0, min(x2, width))
        y2 = max(0, min(y2, height))
        if x2 <= x1 or y2 <= y1:
            raise HTTPException(status_code=400, detail="invalid_redaction_box")
        normalized.append([x1, y1, x2, y2])
    return normalized


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": "0.2.0"}


@app.get("/api/redact/presets")
def presets() -> dict:
    return {"items": [{"name": key, "boxes": value} for key, value in PRESETS.items()]}


@app.post("/api/redact/image")
async def redact_image(
    file: UploadFile = File(...),
    boxes: str | None = Form(default=None),
    preset: str = Form(default="generic"),
) -> dict:
    audit_id = str(uuid4())
    payload = await file.read()
    image = Image.open(BytesIO(payload)).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    if boxes:
        parsed = json.loads(boxes)
    else:
        parsed = PRESETS.get(preset, PRESETS["generic"])
        if not parsed:
            parsed = [[width // 5, height // 3, width * 4 // 5, height // 2]]

    parsed = normalize_boxes(parsed, width, height)

    for box in parsed:
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], fill="black")

    output = BytesIO()
    image.save(output, format="PNG")
    encoded = base64.b64encode(output.getvalue()).decode("utf-8")

    return {
        "audit_id": audit_id,
        "filename": file.filename,
        "preset": preset,
        "redaction_boxes": parsed,
        "image_base64_png": encoded,
    }
