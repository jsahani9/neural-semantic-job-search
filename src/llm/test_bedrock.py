import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

def main():
    if not MODEL_ID:
        raise RuntimeError("BEDROCK_MODEL_ID is missing in .env")

    client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

    prompt = "Write one short line explaining semantic search in simple words."

    body = {
        "prompt": prompt,
        "max_gen_len": 120,
        "temperature": 0.2,
        "top_p": 0.9,
    }

    resp = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )

    data = json.loads(resp["body"].read())
    print("RAW RESPONSE:", data)

    if "generation" in data:
        print("\nMODEL OUTPUT:\n", data["generation"])
    elif "generations" in data and data["generations"]:
        print("\nMODEL OUTPUT:\n", data["generations"][0].get("text"))
    else:
        print("\nCould not find text field, inspect RAW RESPONSE above.")

if __name__ == "__main__":
    main()
