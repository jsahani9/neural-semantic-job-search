"""
Bedrock client for Llama 3.3 70B text generation
"""
import os
import json
import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID")


def generate(prompt: str) -> str:
    if not MODEL_ID:
        raise RuntimeError("BEDROCK_MODEL_ID is missing")

    client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

    body = {
        "prompt": prompt,
        "max_gen_len": 600,
        "temperature": 0.2,
        "top_p": 0.9,
    }

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )

    data = json.loads(response["body"].read())

    if "generation" in data:
        return data["generation"].strip()
    if "generations" in data and data["generations"]:
        return str(data["generations"][0].get("text", "")).strip()

    raise RuntimeError(f"Unexpected Bedrock response format: {data}")
