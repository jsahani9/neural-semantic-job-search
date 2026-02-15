from src.services.adzuna_client import search_jobs

def main():
    print("=== Canada SWE ===")
    canada_swe = search_jobs("software engineer", "Canada", 20)
    print(len(canada_swe))

    print("=== Ontario AI/ML (60 days recommended) ===")
    ontario_aiml = search_jobs("machine learning ai engineer data scientist", "Ontario", 20)
    print(len(ontario_aiml))

    print("=== Ontario Junior AI/ML ===")
    ontario_junior = search_jobs("machine learning ai junior entry new grad intern", "Ontario", 20)
    print(len(ontario_junior))

    print("\nShowing Ontario Junior AI/ML results:\n")
    for i, job in enumerate(ontario_junior, 1):
        print(f"{i}. {job.get('title','')}")
        print(f"   Company: {job.get('company','')}")
        print(f"   Location: {job.get('location','')}")
        print(f"   URL: {job.get('url','')}\n")

if __name__ == "__main__":
    main()
