import subprocess
import argparse
import os
import sys

def run_script(script_path, args_list):
    command = [sys.executable, script_path] + args_list
    print("Running command:", " ".join(command))
    subprocess.run(command, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Resume and Cover Letter together")
    parser.add_argument("--resume", required=True, help="Path to resume text file (parsed)")
    parser.add_argument("--job", required=True, help="Path to job description text file")
    parser.add_argument("--github", help="GitHub link (optional)")
    parser.add_argument("--resume_output", default="generated_resume.txt", help="Path to save generated resume")
    parser.add_argument("--coverletter_output", default="cover_letter.txt", help="Path to save generated cover letter")

    args = parser.parse_args()


    # Step 0: Parse PDF to resume_data.txt if needed
    if not os.path.exists(args.resume):
        print("🔍 Parsing PDF resume...")
        doc_parser_args = [
            "--pdf", args.pdf,
            "--out", args.resume
        ]
        run_script("backend/doc_parser.py", doc_parser_args)
        print(f"📝 Parsed resume data saved to {args.resume}")
    else:
        print("✅ Parsed resume data already exists, skipping PDF parsing.")


    # Step 1: Generate Resume
    print("🚀 Generating Tailored Resume...")
    resume_args = [
        "--resume_txt", args.resume,
        "--jd_txt", args.job,
        "--output_txt", args.resume_output
    ]
    if args.github:
        resume_args += ["--profile_link", args.github]

    run_script("backend/generate_resume.py", resume_args)

    # Step 2: Generate Cover Letter
    print("\n📄 Generating Cover Letter...")
    cover_args = [
        "--resume", args.resume,
        "--job", args.job,
        "--output", args.coverletter_output
    ]
    if args.github:
        cover_args += ["--github", args.github]

    run_script("backend/generate_cover_letter.py", cover_args)

    print("\n✅ All Done! Resume and Cover Letter generated successfully.")
