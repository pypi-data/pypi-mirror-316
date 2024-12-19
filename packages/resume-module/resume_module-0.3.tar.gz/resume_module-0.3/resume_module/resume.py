import openai
from dotenv import load_dotenv
import os
from fpdf import FPDF

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def input_fields():
    fields = [
        'Name', 'Contactnumber', 'Youraddress', 'professionalsummary',
        'Github', 'Linkedin', 'Facebook', 'Workexperience',
        'EducationQualification', 'Interests', 'Languages'
    ]

    print("Enter your details to generate a professional resume:")
    inputs = [input(f"{field}: ") for field in fields]

    return dict(zip(fields, inputs))


def generate_resume(data, model_name="gpt-3.5-turbo", custom_prompt=None):

    # Prepare the prompt
    from openai import OpenAI
    client = OpenAI()
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = f"Give me a professional looking resume based on this given data: {data}"

    # Make the OpenAI API call for generating the resume
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the resume content
    content = completion.choices[0].message.content
    return content


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", size=12)
        self.cell(0, 10, "Professional Resume", align="C", ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def save_to_pdf(content, filename):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)


def generate_and_save_resume(model_name="gpt-3.5-turbo", custom_prompt=None):
    # Step 1: Get user input
    user_data = input_fields()

    # Step 2: Generate resume content
    print("\nGenerating your resume...")
    resume_content = generate_resume(user_data, model_name)

    # Step 3: Save to PDF
    output_file = f"{user_data['Name']}.pdf"
    save_to_pdf(resume_content, output_file)
    print(f"\nYour resume has been saved as '{output_file}'.")
