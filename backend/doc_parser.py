# import os
# import json
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from PyPDF2 import PdfReader
# import pandas as pd
# from langchain_community.llms import Ollama
import fitz  # PyMuPDF
import argparse
import re
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

#extract text from PDF file

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text=" "
    for page in doc:
        text += page.get_text()
    return text


# section extraction using regex
def extract_section(text, keyword_list):
    for keyword in keyword_list:
        pattern = rf"{keyword}[\s\S]*?(?=\n[A-Z][^\n]{2,}|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return "Not Found"
    
# Extracts all important sections (skills, experience, etc.) from the resume

def parse_resume_sections(text):
    return {
    "full_name": extract_section(text, ["name", "full name", "contact name"]),
    "email": extract_section(text, ["email", "e-mail", "email address"]),
    "phone": extract_section(text, ["phone", "mobile", "contact number", "telephone"]),
    "summary_or_objective": extract_section(text, ["summary", "professional summary", "career objective", "objective"]),
    "work_experience": extract_section(text, ["experience", "work experience", "professional experience", "employment history", "career history" ]),
    "education": extract_section(text, ["education", "academic background", "educational qualifications", "academic qualifications"]),
    "skills": extract_section(text, ["skills", "technical skills", "key skills", "core competencies", "technologies", "tools"]),
    "projects": extract_section(text, ["projects", "key projects", "academic projects", "notable projects"]),
    "certifications": extract_section(text, ["certifications", "licenses", "certified courses"]),
    "languages": extract_section(text, ["languages", "language proficiency"]),
    "awards_and_achievements": extract_section(text, ["awards", "achievements", "honors", "recognition"]),
    "interests": extract_section(text, ["interests", "hobbies", "extracurricular activities"]),
    "references": extract_section(text, ["references", "referees", "reference information"]),
}

# #generate resume using langchain+ollama ✨ by sending the extracted information to the LLM

# def generate_resume(job_title ,full_name, skills, experience, education, projects, certifications, languages, awards_and_achievements, interests, references, summary_or_objective):
#     prompt = PromptTemplate(
#         input_variables=["job_title", "skills", "experience", "education", "projects", "certifications", "languages", "awards_and_achievements", "interests", "references", "summary_or_objective"],
#         template="""
#         You are a resume generator. Your task is to create a strong, tailored resume based on the information provided.
        
#         Job Title: {job_title}
#         Full Name: {full_name}
#         Summary/Objective:{summary_or_objective}
#         Skills:{skills}
#         Experience:{experience}
#         Projects:{projects}
#         Education:{education}
#         Certifications:{certifications}
#         Awards & Achievements:{awards}
#         Languages:{languages}
#         Interests:{interests}
        
#         The resume should be well-formatted in **Markdown**, have clear **section headers**, and sound professional and concise.
#         """  
#     )
#     llm = Ollama(model="mistral", temperature=0)
#     chain = LLMChain(llm=llm, prompt=prompt)
#     return chain.run({
#         "job_title": job_title,
#         "full_name": full_name,
#         "summary_or_objective": summary_or_objective,
#         "skills": skills,
#         "experience": experience,
#         "projects": projects,
#         "education": education,
#         "certifications": certifications,
#         "awards_and_achievements": awards_and_achievements,
#         "languages": languages,
#         "interests": interests,
#         "references": references,
#     })

#	Parses args (--pdf, --job_title), runs extraction + resume generation, and prints the result

if __name__ == "__main__":
    parser  = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, help="Path to the resume PDF file")
    parser.add_argument("--out", required=True, help="Path to save parsed resume data as .txt")
    args = parser.parse_args()

    raw_text = extract_text_from_pdf(args.pdf)
    parsed_data = parse_resume_sections(raw_text)

    with open(args.out,"w") as f:
        f.write(json.dumps(parsed_data, indent=2))

    print(f"Parsed resume data saved to {args.out}")

    # result = generate_resume(
    #     job_title=args.job_title,
    #     skills=parsed_data["skills"],
    #     experience=parsed_data["experience"],
    #     projects=parsed_data["projects"],
    #     education=parsed_data["education"]
    # )

    # print("\n===== Generated Tailored Resume =====\n")
    # print(result)








































# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY") # Get OpenAI API key from .env file

# # function to extract text from PDF file

# def extract_text_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     text= " "  
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# #saving the extracted text in a text file
# current_dir = os.path.dirname(os.path.abspath(__file__))
# pdf_path = os.path.join(current_dir, "resume.pdf")
# resume_text = extract_text_from_pdf(pdf_path)

# print(resume_text[:1000])









