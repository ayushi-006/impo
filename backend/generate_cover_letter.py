# generate_cover_letter.py

from langchain.llms import Ollama  # or OpenAI, if using it
from langchain.prompts import PromptTemplate
import argparse

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_cover_letter(resume_text, job_description, github_link=" "):
    llm = Ollama(model="llama3")  # or any model you're using

    prompt_template = PromptTemplate(
        input_variables=["resume", "job", "github"],
        template="""
        Write a personalized, concise, and enthusiastic cover letter based on the resume and job description below.
        If a GitHub link is provided, mention relevant projects.
         Its purpose is to:

        Introduce yourself and explain why you’re writing.
        Highlight key qualifications and experiences that match the job posting.
        Demonstrate fit and enthusiasm for the role and the company’s mission.
        Showcase your personality and communication skills in a way a résumé alone cannot.
        Keep it concise: One page,  short paragraphs, and make it consise with the resume and job description.

        Typical Structure
        header:
        Greeting
        opening paragraph: Introduce yourself and explain why you’re writing.
        body paragraph(s): Highlight key qualifications and experiences that match the job posting.
        closing paragraph: Demonstrate fit and enthusiasm for the role and the company’s mission.
        sign-off/regards

        Resume:
        {resume}

        Job Description:
        {job}

        GitHub Link (if any):
        {github}

        The tone should be professional and goal-oriented.
        Output just the final letter content.
        """
    )

    prompt = prompt_template.format(resume=resume_text, job=job_description, github=github_link or "Not provided")
    return llm.invoke(prompt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Cover Letter using LLM")
    parser.add_argument("--resume", required=True, help="Path to parsed resume text file")
    parser.add_argument("--job", required=True, help="Path to job description text file")
    parser.add_argument("--github", required=False, help="GitHub link (optional)")
    parser.add_argument("--output", default="cover_letter.txt", help="Output file path")
    # parser.add_argument("--github_link", required=False, default="", help="Github link for the candidate")

    args = parser.parse_args()

    resume_text = load_file(args.resume)
    job_description = load_file(args.job)

    cover_letter = generate_cover_letter(resume_text, job_description, args.github)

    print("\n===== Cover Letter (Markdown) =====\n")


    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(cover_letter)

    print(f"✅ Cover letter saved to: {args.output}")
