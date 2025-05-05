import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.chat_models  import  ChatOpenAI
from langchain_openai import ChatOpenAI

from PyPDF2 import PdfReader
import pandas as pd
from doc_parser import extract_text_from_pdf

load_dotenv() # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY") # Get OpenAI API key from .env file

#LANGCHAIN
# from langchain.chat_models  import  ChatOpenAI


# once we get the real text we need to structure it in a way that we can use it to generate the resume according to the JD, this is where AI and langchain comes in

#Generate structured output using langchain _OpenAI ✨

def generate_structured_output(resume_text):
    template = PromptTemplate(
        input_variables=["resume_text"],
        template="""
        You are a resume parser. Your task is to extract the following information from the resume text provided.
        The output should be in JSON format. The keys should be the following:
        - name
        - email
        - phone
        - skills
        - experience
        - education
        - projects
        - languages
        - certifications
        - references
        - summary
    
        Resume text: {resume_text}
        """
)

    llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0, max_tokens=2000)
    chain = LLMChain(llm = llm ,  prompt=template)     
    structured_response = chain.invoke({"resume_text":resume_text})                                                       
    return structured_response.replace("```", "").replace("json", "")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "resume.pdf")
    resume_text = extract_text_from_pdf(pdf_path)

    structured_response = generate_structured_output(resume_text)


print(structured_response)

