from utils import * 

# xray_iamge 
#  
image_path = "images/xray2.jpeg"
base64_image = encode_image(image_path)

# patient_detail

p_name = "Rehan"
p_dob = "02-11-2001"


print(base64_image)

# creating prompt for model
input_mesage = create_message(base64_image,p_dob ,p_name)

# getting model response 
response = lama_model(input_mesage)
print(response)



# converting output into pdf

pdf = PDF()
pdf.add_page()
pdf.chapter_body(response)
pdf.output("report.pdf")












# class PDF(FPDF):
#     def header(self):
#         # Set font for header
#         self.set_font("Arial", "B", 12)

#     def chapter_title(self, title):
#         # Set font for chapter title
#         self.set_font("Arial", "B", 12)
#         self.cell(0, 10, title, 0, 1, 'L')
#         self.ln(5)

#     def chapter_body(self, body):
#         # Set font for body
#         self.set_font("Arial", "", 12)
#         # Split the text into lines and handle bold formatting
#         for line in body.split('\n'):
#             if line.startswith("**") and line.endswith("**"):
#                 # Strip the asterisks and set to bold
#                 self.set_font("Arial", "B", 12)
#                 line = line[2:-2].strip()
#             else:
#                 self.set_font("Arial", "", 12)
#             self.multi_cell(0, 10, line)
#         self.ln()