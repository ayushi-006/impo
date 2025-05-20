import argparse
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from langchain_core.runnables import chain
from extract_github import fetch_github_info, github_username


# github_username = resume_data.get("github_username", "") or args.profile_link.split("/")[-1]

# github_summary = fetch_github_info(github_username)

def load_github_summary(filepath="github_summary.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No GitHub summary available."
    
github_summary = load_github_summary()

def load_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def generate_tailored_resume(resume_data, job_description, profile_link=" "):
    prompt = PromptTemplate(
        input_variables=[
            "job_description", "full_name", "summary_or_objective", "skills", "experience",
            "projects", "education", "certifications", "awards_and_achievements","CGPA",
            "languages", "interests", "references, github_summary"
        ],
         template="""
                You are a professional resume optimizer. Your task is to tailor the resume to the job description below based on the provided resume data and and GitHub contributions.
                
                
                GitHub Contributions:
                {github_summary}
                Job Description:
                {job_description}
                
                Candidate Details:
                Full Name: {full_name}
                Summary/Objective: {summary_or_objective}
                Skills: {skills}
                Experience: {experience}
                Projects: {projects}
                Education: {education}
                CGPA: {cgpa}
                Certifications: {certifications}
                Awards & Achievements: {awards_and_achievements}
                Languages: {languages}
                Interests: {interests}
                References: {references}
                
                Please generate a professional resume in **Markdown** format. Return a professional, ATS-friendly resume focusing on alignment between the user's skills and the job description.it should emphasizes the most relevant skills and experience, and is concise, structured, and impactful.
                 """
    )

    llm = Ollama(model="llama3", temperature=0)
    # chain = LLMChain(llm=llm, prompt=prompt)
    runnable = prompt | llm

    return runnable.invoke({
        "job_description": job_description,
        "github_summary": github_summary,
        "full_name": resume_data.get("full_name", ""),
        "summary_or_objective": resume_data.get("summary_or_objective", ""),
        "skills": resume_data.get("skills", ""),
        "experience": resume_data.get("work_experience", ""),
        "projects": resume_data.get("projects", ""),
        "education": resume_data.get("education", ""),
        "cgpa": resume_data.get("CGPA", ""),
        "certifications": resume_data.get("certifications", ""),
        "awards_and_achievements": resume_data.get("awards_and_achievements", "position_of responsibility"),
        "languages": resume_data.get("languages", ""),
        "interests": resume_data.get("interests", ""),
        "references": resume_data.get("references", "")
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume_txt", required=True, help="impo\resume_data.txt")
    parser.add_argument("--jd_txt", required=True, help="impo\backend\jd.txt")
    parser.add_argument("--output_txt", required=False, default="tailored_resume.txt", help="Path to output tailored resume .txt file")
    parser.add_argument("--profile_link", required=False, default="", help="Profile link for the candidate")
    args = parser.parse_args()

    # Load inputs
    resume_json = load_txt_file(args.resume_txt)
    resume_data = json.loads(resume_json)
    job_description = load_txt_file(args.jd_txt)

    # Generate tailored resume
    tailored_resume = generate_tailored_resume(resume_data, job_description, args.profile_link)

    print("\n===== Tailored Resume (Markdown) =====\n")
    # print(tailored_resume)

    output_file = args.output_txt
    with open(output_file, "w", encoding="utf=8") as f:
        f.write(tailored_resume)

    print(f"\nTailored resume saved to {output_file}\n")
