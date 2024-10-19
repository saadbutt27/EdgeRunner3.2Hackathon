from fastapi import FastAPI, Request
import base64
from io import BytesIO
from PIL import Image
# from fastapi.middleware.cors import CORSMiddleware

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# origins = [
#     "http://localhost:3000",  # Example frontend URL
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.post("/api/py/image")
async def process_image(request: Request):
    data = await request.json()
    image_data = data.get('image')
    print(image_data)

    if image_data:
        # Strip the "data:image/png;base64," prefix from the data URL
        base64_image = image_data.split(",")[1]

        # Decode the base64 image
        image_bytes = base64.b64decode(base64_image)

        # Convert to an image using PIL (Python Imaging Library)
        image = Image.open(BytesIO(image_bytes))

        # You can now display the image or save it
        image.show()  # This will display the image
        return {"message": "Image processed successfully"}
    else:
        return {"error": "No image data received"}