import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from PyPDF2 import PdfReader
import pandas as pd




load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") # Get OpenAI API key from .env file

# function to extract text from PDF file

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text= " "  
    for page in reader.pages:
        text += page.extract_text()
    return text

#saving the extracted text in a text file
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(current_dir, "resume.pdf")
resume_text = extract_text_from_pdf(pdf_path)

print(resume_text[:1000])









