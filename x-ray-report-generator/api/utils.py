import io
import os
from together import Together
from fpdf import FPDF
import base64
from datetime import datetime
from dotenv import load_dotenv

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

load_dotenv()
secret = os.getenv("LAMA_API_KEY")

def lama_model(input_message):
    client = Together(
        base_url="https://api.aimlapi.com/v1", 
        api_key=secret
    )
    # print(input_message)
    try:
        print("taking response")
        response=client.chat.completions.create(
            model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
            messages=input_message,
            max_tokens=300,
        )

        print("got the response")
        result=response.choices[0].message.content 
        print("Response received from Together API:", response)
        return result
    except Exception as e:
        print("Error during API request:", e)
        raise
        
current_date = datetime.now().date()

def create_message(image, patient_name, patient_dob):
    input_mesage=[{
        "role": "user",
        "content": [{
            "type": "text",
            "text": f''' 
                Generate an X-Ray/MRI report for the attached image. The report should have the following format:

                    1) Title: DHA Diagnostic Center (with big font size)
                    2) Heading: Imaging Center\n Khyaban-e-Tufail, DHA Phase VII Ext.
                    3) Patient Details: 
                        Name: {patient_name}
                        Date of Birth: {patient_dob}
                        MR #: ________
                        Physician: __________
                        Exam: Extract X-Ray/MRI information as per the X-Ray image
                        Dated: {current_date}

                    4) Clinical Information:
                    5) Contrast:
                    6) Technique:
                    7) Findings:
                    8) Impression:
                ''',
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"{image}",
                },
            },],
        },
    ]

    return input_mesage

def generate_pdf(content):
    # Initialize PDF object
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font for the heading (Bold and larger size)
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "X-Ray Report", ln=True, align='C')  # Centered heading

    # Add a subheading (Italic)
    pdf.set_font("Arial", style='I', size=12)
    pdf.cell(200, 10, "Generated on: 2024-10-19", ln=True, align='L')

    # Add some space
    pdf.ln(10)

    # Set regular font for content
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)  # The regular content of the PDF

    # Add a bold subheading
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Findings:", ln=True)

    # Add some italic text under Findings
    pdf.set_font("Arial", style='I', size=12)
    pdf.multi_cell(0, 10, "The patient shows signs of improvement after the treatment...")

    # Create a BytesIO buffer to hold the PDF
    pdf_buffer = io.BytesIO()

    # Output the PDF data as a string and write it to the BytesIO buffer
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_buffer.write(pdf_output)

    # Set the file pointer to the beginning of the stream
    pdf_buffer.seek(0)

    return pdf_buffer

class PDF(FPDF):
    def header(self):
        # Set font for header
        self.set_font("Arial", "B", 12)

    def chapter_title(self, title):
        # Set font for chapter title
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        # Set font for body
        self.set_font("Arial", "", 12)
        # Split the text into lines and handle bold formatting
        for line in body.split('\n'):
            if line.startswith("**") and line.endswith("**"):
                # Strip the asterisks and set to bold
                self.set_font("Arial", "B", 12)
                line = line[2:-2].strip()
            else:
                self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, line)
        self.ln()