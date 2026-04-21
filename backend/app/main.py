import base64
import json
from io import BytesIO

from fastapi import FastAPI, File, Form, UploadFile
from PIL import Image, ImageDraw

app = FastAPI(title="Secure File Redaction Service")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/redact/image")
async def redact_image(
    file: UploadFile = File(...),
    boxes: str | None = Form(default=None),
) -> dict:
    payload = await file.read()
    image = Image.open(BytesIO(payload)).convert("RGB")
    draw = ImageDraw.Draw(image)

    if boxes:
        parsed = json.loads(boxes)
    else:
        width, height = image.size
        parsed = [[width // 5, height // 3, width * 4 // 5, height // 2]]

    for box in parsed:
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], fill="black")

    output = BytesIO()
    image.save(output, format="PNG")
    encoded = base64.b64encode(output.getvalue()).decode("utf-8")

    return {
        "filename": file.filename,
        "redaction_boxes": parsed,
        "image_base64_png": encoded,
    }
