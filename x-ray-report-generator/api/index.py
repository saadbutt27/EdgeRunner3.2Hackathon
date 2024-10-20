from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from .utils import *

# Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.post("/api/py/image")
async def process_image(request: Request):
    data = await request.json()
    image_data = data.get('image')
    patient_name = data.get('patient_name')
    patient_dob = data.get('patient_dob')

    if image_data and patient_name and patient_dob:
        # Create input message for the LLaMA model
        input_message = create_message(image_data, patient_name, patient_dob)
        
        # Get the response from the LLaMA model
        response_content = lama_model(input_message)
        # print(f"Model Response: {response_text}")

        # Generate the PDF
        pdf_buffer = generate_pdf(response_content)
        
        # Return the PDF as a downloadable file
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf", 
            headers={"Content-Disposition": "attachment; filename=report.pdf"}
        )
    else:
        return {"error": "No image data received"}