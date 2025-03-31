import base64
import io

from PIL import Image
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.post("/process-image")
async def process_image(
        file: UploadFile = File(...),
        value: int = Form(128)
):
    image = Image.open(io.BytesIO(await file.read()))
    image = image.resize((128, 128))
    gray = image.convert("L")

    gray.convert("1", dither=Image.Dither.FLOYDSTEINBERG)

    buffered = io.BytesIO()
    gray.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image": img_base64}
