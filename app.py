from flask import Flask, render_template, request, jsonify # Added request, jsonify
import os
import boto3 # Added boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError # For S3 error handling
from werkzeug.utils import secure_filename # For securing filenames

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

# --- AWS S3 Configuration ---
# IMPORTANT: Replace with your actual S3 bucket name and region
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'awscloudhacks20254778a1e2a74d463fac056f01856fbce11cf-dev')
S3_BUCKET_REGION = os.environ.get('S3_BUCKET_REGION', 'us-west-2') # e.g., 'us-west-2'
S3_RESUMES_PREFIX = 'resumes/'
S3_JD_PREFIX = 'job_descriptions/'


# Initialize S3 client
# Boto3 will automatically look for credentials in environment variables,
# shared credential file (~/.aws/credentials), or IAM roles.
# Ensure your environment is configured with AWS credentials and region.
try:
    s3_client = boto3.client('s3', region_name=S3_BUCKET_REGION)
except Exception as e:
    s3_client = None # Handle cases where boto3 might not initialize
    print(f"Error initializing S3 client: {e}")
# --- End AWS S3 Configuration ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/resume-upload')
def resume_upload_page(): # Renamed to avoid conflict with the API endpoint logic if it were merged
    return render_template('resume_upload.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/api/upload-file', methods=['POST'])
def upload_file_to_s3():
    """
    Handles file uploads (resume or job description) and stores them in S3.
    Expects 'file' and 'fileType' ('resume' or 'jd') in the form data.
    """
    if s3_client is None:
        return jsonify({'error': 'S3 client not initialized. Check server logs.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    file_type = request.form.get('fileType') # 'resume' or 'jd'

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file_type not in ['resume', 'jd']:
        return jsonify({'error': 'Invalid fileType specified. Must be "resume" or "jd".'}), 400

    if file:
        filename = secure_filename(file.filename)
        s3_prefix = S3_RESUMES_PREFIX if file_type == 'resume' else S3_JD_PREFIX
        s3_object_name = os.path.join(s3_prefix, filename) # Store in a folder based on type

        try:
            # Upload the file to S3
            s3_client.upload_fileobj(
                file,
                S3_BUCKET_NAME,
                s3_object_name
                # You can add ExtraArgs for things like ContentType if needed
                # ExtraArgs={'ContentType': file.content_type}
            )
            # In a real app, you might store the s3_object_name or a URL in a database
            return jsonify({
                'message': f"File '{filename}' uploaded successfully as {file_type} to S3.",
                'filename': filename,
                's3_key': s3_object_name
            }), 200

        except NoCredentialsError:
            print("AWS credentials not found.")
            return jsonify({'error': 'AWS credentials not found. Configure your environment.'}), 500
        except PartialCredentialsError:
            print("Incomplete AWS credentials.")
            return jsonify({'error': 'Incomplete AWS credentials. Configure your environment.'}), 500
        except ClientError as e:
            print(f"S3 Client Error: {e.response['Error']['Message']}")
            return jsonify({'error': f"S3 Client Error: {e.response['Error']['Message']}"}), 500
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500
    
    return jsonify({'error': 'File upload failed for an unknown reason.'}), 500


if __name__ == '__main__':
    # For local development, ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    # and AWS_DEFAULT_REGION (or S3_BUCKET_REGION) are set in your environment,
    # or you have a configured AWS credentials file (~/.aws/credentials).
    # Example (do not hardcode credentials in production):
    # os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_KEY'
    # os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET'
    # os.environ['S3_BUCKET_NAME'] = 'your-actual-bucket-name'
    # os.environ['S3_BUCKET_REGION'] = 'your-actual-region'
    
    # Check if bucket name and region are set (especially if not using environment variables directly above)
    if S3_BUCKET_NAME == 'your-s3-bucket-name-here' or S3_BUCKET_REGION == 'your-s3-region-here':
        print("WARNING: S3_BUCKET_NAME or S3_BUCKET_REGION are not configured. Please set them.")
        print("You can set them as environment variables or directly in the script (for testing only).")

    app.run(debug=True)
