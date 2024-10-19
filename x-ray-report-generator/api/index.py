from fastapi import FastAPI, Request, Response
import base64
from io import BytesIO
from PIL import Image
from fastapi.responses import StreamingResponse
from .utils import *
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
    patient_name = data.get('patient_name')
    patient_dob = data.get('patient_dob')

    # print(image_data, patient_name, patient_dob)

    if image_data and patient_name and patient_dob:
        # Create input message for the LLaMA model
        input_message = create_message(image_data, patient_name, patient_dob)
        
        # Get the response from the LLaMA model
        response_content = lama_model(input_message)
        # print(f"Model Response: {response_text}")

        # Generate the PDF
        # content = "Sample text for the PDF"  # Replace with your actual content
        pdf_buffer = generate_pdf(response_content)
        
        # Return the PDF as a downloadable file
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf", 
            headers={"Content-Disposition": "attachment; filename=report.pdf"}
        )
    else:
        return {"error": "No image data received"}