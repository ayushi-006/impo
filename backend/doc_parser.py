# # import os
# # import json
# # from dotenv import load_dotenv
# # from langchain_openai import ChatOpenAI
# # from langchain.prompts import PromptTemplate
# # from langchain.chains import LLMChain
# # from PyPDF2 import PdfReader
# # import pandas as pd
# # from langchain_community.llms import Ollama
# import fitz  # PyMuPDF
# import argparse
# import re
# import json
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain_community.llms import Ollama

# #extract text from PDF file

# def extract_text_from_pdf(file_path):
#     doc = fitz.open(file_path)
#     text=" "
#     for page in doc:
#         text += page.get_text()
#     return text


# # section extraction using regex
# def extract_section(text, keyword_list):
#     # Create a regex pattern for all keywords
#     header_pattern = '|'.join([re.escape(k) for k in keyword_list])
    
#     # Use lookahead to stop at the next section title (from the keyword list)
#     pattern = rf"(?i)({header_pattern})[\s\S]*?(?=(\n(?:{header_pattern})\b|\Z))"

#     match = re.search(pattern, text, re.IGNORECASE)
#     if match:
#         return match.group(0).strip()
#     return "Not Found"

# # Extracts all important sections (skills, experience, etc.) from the resume

# def parse_resume_sections(text):
#     return {
#     "name": extract_section(text, ["name", "full name", "contact name"]),
#     "email": extract_section(text, ["email", "e-mail", "email address"]),
#     "phone": extract_section(text, ["phone", "mobile", "contact number", "telephone"]),
#     "summary_or_objective": extract_section(text, ["summary", "professional summary",  "objective"]),
#     "work_experience": extract_section(text, ["experience", "work experience", "professional experience", "employment history" ]),
#     "education": extract_section(text, ["education", "academic background", "educational qualifications", "academic qualifications"]),
#     "skills": extract_section(text, ["skills", "technical skills", "key skills", "core competencies", "technologies", "tools"]),
#     "projects": extract_section(text, ["projects", "key projects", "academic projects", "notable projects"]),
#     "certifications": extract_section(text, ["certifications", "licenses", "certified courses"]),
#     "languages": extract_section(text, ["languages", "language proficiency"]),
#     "awards_and_achievements": extract_section(text, ["awards", "achievements", "honors", "recognition"]),
#     "interests": extract_section(text, ["interests", "hobbies", "extracurricular activities"]),
#     "references": extract_section(text, ["references", "referees", "reference information"]),
# }

# #	Parses args (--pdf, --job_title), runs extraction + resume generation, and prints the result

# if __name__ == "__main__":
#     parser  = argparse.ArgumentParser()
#     parser.add_argument("--pdf", required=True, help="impo\data\resume2.pdf")
#     parser.add_argument("--out", required=True, help="impo\resume_data.txt")
#     args = parser.parse_args()

#     raw_text = extract_text_from_pdf(args.pdf)
#     parsed_data = parse_resume_sections(raw_text)

#     with open(args.out,"w") as f:
#         f.write(json.dumps(parsed_data, indent=2))

#     print(f"📝Parsed resume data saved to {args.out}")


import fitz  # PyMuPDF
import argparse
import re
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_section(text, keyword_list):
    header_pattern = '|'.join([re.escape(k) for k in keyword_list])
    
    # Match header and extract until next header OR end of file
    pattern = rf"(?i)({header_pattern})[\s:]*\n?([\s\S]*?)(?=(\n(?:{header_pattern})\b|\Z))"
    
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(2).strip()
    
    return "Not Found"


def extract_inline_field(text, field_type):
    if field_type == "email":
        match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    elif field_type == "phone":
        match = re.search(r"\+?\d[\d\s\-()]{8,}\d", text)
    elif field_type == "name":
        # Assume name is at the top (first line)
        lines = text.strip().split('\n')
        if lines:
            return lines[0].strip()
        else:
            return "Not Found"
    else:
        match = None

    return match.group(0).strip() if match else "Not Found"


def parse_resume_sections(text):
    return {
        "name": extract_inline_field(text, "name"),
        "email": extract_inline_field(text, "email"),
        "phone": extract_inline_field(text, "phone"),
        "summary_or_objective": extract_section(text, ["summary", "professional summary", "objective"]),
        "work_experience": extract_section(text, ["experience", "work experience", "professional experience", "employment history"]),
        "education": extract_section(text, ["education", "academic background", "educational qualifications", "academic qualifications"]),
        "skills": extract_section(text, ["skills", "technical skills", "key skills", "core competencies", "technologies", "tools"]),
        "projects": extract_section(text, ["projects", "key projects", "academic projects", "notable projects"]),
        "certifications": extract_section(text, ["certifications", "licenses", "certified courses"]),
        "languages": extract_section(text, ["languages", "language proficiency"]),
        "awards_and_achievements": extract_section(text, ["awards", "achievements", "honors", "recognition"]),
        "interests": extract_section(text, ["interests", "hobbies", "extracurricular activities"]),
        "references": extract_section(text, ["references", "referees", "reference information"]),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, help="Path to PDF file")
    parser.add_argument("--out", required=True, help="Path to output file")
    args = parser.parse_args()

    raw_text = extract_text_from_pdf(args.pdf)
    parsed_data = parse_resume_sections(raw_text)

    with open(args.out, "w") as f:
        f.write(json.dumps(parsed_data, indent=2))

    print(f"📝 Parsed resume data saved to {args.out}")












































