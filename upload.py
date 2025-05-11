import boto3
import json

# Replace with your actual bucket name
BUCKET_NAME = "awscloudhacks20254778a1e2a74d463fac056f01856fbce11cf-dev"

def save_transcript_to_file(transcript_data, filename="transcript.json"):
    with open(filename, "w") as f:
        json.dump(transcript_data, f, indent=2)
    print(f"✅ Transcripts saved to {filename}")
    return filename

def upload_to_s3(file_path, bucket, key=None):
    s3 = boto3.client("s3")
    key = key or file_path
    s3.upload_file(file_path, bucket, key)
    print(f"✅ Uploaded {file_path} → s3://{bucket}/{key}")

if __name__ == "__main__":
    # Example: your transcript dict
    transcript = {
        "speaker1": ["Hello", "How are you?"],
        "speaker2": ["I’m good, thanks!"]
    }

    # 1) Save locally
    local_file = save_transcript_to_file(transcript)

    # 2) Upload to S3
    upload_to_s3(local_file, BUCKET_NAME)
