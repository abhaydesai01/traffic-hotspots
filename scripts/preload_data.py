import subprocess

BUCKET_NAME = 'traffic-hubspot'
FILE_KEY = 'collisions.csv'
LOCAL_FILE = 'collisions.csv'

def download_with_cli():
    print(f"📦 Downloading {FILE_KEY} using AWS CLI...")
    cmd = [
        "aws", "s3", "cp",
        f"s3://{BUCKET_NAME}/{FILE_KEY}",
        LOCAL_FILE
    ]
    try:
        subprocess.run(cmd, check=True)
        print("✅ File downloaded successfully via AWS CLI")
    except subprocess.CalledProcessError as e:
        print("❌ Download failed:", e)

if __name__ == "__main__":
    download_with_cli()
