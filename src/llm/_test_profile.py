from src.llm.profile_analyzer import analyze_profile

FAKE_RESUME = """
Computer Science student with experience in Python and machine learning.
Built projects using pandas, numpy, scikit-learn, FastAPI, and Docker.
Worked on a GenAI project using AWS Bedrock and LangChain.
Looking for junior AI or backend roles.
"""

def main():
    result = analyze_profile(FAKE_RESUME)
    print("\n===== PROFILE ANALYSIS =====\n")
    print(result)

if __name__ == "__main__":
    main()
