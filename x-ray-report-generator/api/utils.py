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
        # print("taking response")
        response=client.chat.completions.create(
            model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
            messages=input_message,
            max_tokens=300,
        )

        # print("got the response")
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
                You are an AI assistant tasked with analyzing an X-ray image for diagnostic purposes and generating a structured medical report. The patient’s X-ray was taken at a diagnostic center, and your goal is to analyze the image and provide an insightful report based on the following sections.

                **Title**: DHA Diagnostic Center

                **Address**: Imaging Center, Khyaban-e-Tufail, DHA Phase VII Ext.

                **Patient Details**:
                **Name**: {patient_name}
                **Date of Birth**: {patient_dob}
                **MR #**: __________
                **Physician**: __________
                **Exam**: __________
                **Date of Examination**: {datetime.now().date()}

                **Report Details**:
                1) **Clinical Information**:
                   - Include any relevant clinical context that might be important for interpreting the image, such as the patient's symptoms, medical history, or any previous diagnosis.
                2) **Contrast**:
                   - Mention whether any contrast agent was used during the imaging and if so, how it impacts the visualization of different anatomical structures.
                3) **Imaging Technique**:
                   - Describe the X-ray technique used and whether it affects the accuracy or clarity of the results. Note any specific settings that may be relevant to the interpretation.
                4) **Findings**:
                   - Provide a detailed analysis of the X-ray. Look for signs of fractures, lesions, abnormal tissue growth, dislocations, or any indications of disease. Ensure that your observations are based on clear evidence from the image.
                5) **Impression**:
                   - Summarize the overall diagnosis or preliminary conclusion based on your findings. Highlight any critical medical concerns or abnormalities that may need urgent attention or further medical examination.

                **Responsible AI Considerations**:
                - **Accuracy**: Ensure that your findings are strictly based on the evidence visible in the image. Avoid making assumptions or medical conclusions that are not supported by clear observations.
                - **Safety**: Be careful with your conclusions. Flag any areas where you are uncertain and emphasize that a licensed radiologist or physician should verify the analysis.
                - **Bias Mitigation**: Provide a fair and unbiased interpretation, avoiding any conclusions that could be influenced by incomplete patient data or assumptions.

                This report serves as a diagnostic aid and is not a substitute for a professional medical evaluation.
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

# def generate_pdf(content):
#     # Initialize PDF object
#     pdf = FPDF()

#     # Add a page
#     pdf.add_page()

#     # Set font for the heading (Bold and larger size)
#     pdf.set_font("Arial", style='B', size=16)
#     pdf.cell(200, 10, "X-Ray Report", ln=True, align='C')  # Centered heading

#     # Add a subheading (Italic)
#     pdf.set_font("Arial", style='I', size=12)
#     pdf.cell(200, 10, "Generated on: 2024-10-19", ln=True, align='L')

#     # Add some space
#     pdf.ln(10)

#     # Set regular font for content
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, content)  # The regular content of the PDF

#     # Add a bold subheading
#     pdf.set_font("Arial", style='B', size=12)
#     pdf.cell(200, 10, "Findings:", ln=True)

#     # Add some italic text under Findings
#     pdf.set_font("Arial", style='I', size=12)
#     pdf.multi_cell(0, 10, "The patient shows signs of improvement after the treatment...")

#     # Create a BytesIO buffer to hold the PDF
#     pdf_buffer = io.BytesIO()

#     # Output the PDF data as a string and write it to the BytesIO buffer
#     pdf_output = pdf.output(dest='S').encode('latin1')
#     pdf_buffer.write(pdf_output)

#     # Set the file pointer to the beginning of the stream
#     pdf_buffer.seek(0)

#     return pdf_buffer

def generate_pdf(content):
    # Helper function to parse the content and apply bold formatting
    def parse_and_format_text(pdf, text):
        tokens = text.split('**')
        for i, token in enumerate(tokens):
            if i % 2 == 1:
                pdf.set_font("Arial", style='B', size=12)  # Bold text
            else:
                pdf.set_font("Arial", style='', size=12)   # Regular text
            pdf.multi_cell(0, 5, token)

    # Initialize PDF object
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font for the "X-Ray Report" heading (Bold and 20 in size)
    pdf.set_font("Arial", style='B', size=20)
    pdf.cell(200, 10, "X-Ray Report", ln=True, align='C')  # Centered heading

    # Add a subheading (Italic)
    pdf.set_font("Arial", style='I', size=12)
    pdf.cell(200, 10, "Generated on: 2024-10-19", ln=True, align='L')

    # Add some space
    pdf.ln(10)

    # Parse and add the content
    parse_and_format_text(pdf, content)

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