# AI Interview Preparation Platform

An AI-powered interview preparation tool that helps users practice for job interviews by simulating realistic interview scenarios, providing real-time feedback on their responses, body language, and communication skills.

## Features

- **Resume & Job Description Analysis**: Upload your resume and job description to get personalized interview questions
- **Real-time AI Interviewer**: Practice with an AI interviewer that asks relevant questions based on the job requirements
- **Speech Recognition & Synthesis**: Natural conversation with voice input and output
- **Video Analysis**: Get feedback on eye contact, body language, and facial expressions
- **Comprehensive Feedback**: Detailed performance analysis and improvement suggestions
- **Progress Tracking**: Monitor your improvement over time

## Technology Stack

### Frontend
- HTML, CSS, JavaScript
- Bootstrap 5
- Chart.js (for visualization)

### Backend
- Python with Flask
- AWS Services:
  - Amazon S3 (document storage)
  - Amazon Textract (document analysis)
  - Amazon Transcribe (speech-to-text)
  - Amazon Polly (text-to-speech)
  - Amazon Rekognition (video analysis)
  - Amazon Comprehend (NLP)
  - Amazon Bedrock (LLM for answer evaluation)
  - Amazon API Gateway
  - AWS Lambda
  - Amazon DynamoDB
  - Amazon Cognito (authentication)
  - AWS Amplify (hosting)

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- AWS Account with appropriate permissions

### Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/ai-interview-prep.git
cd ai-interview-prep
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
ai-interview-prep/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Images and icons
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   ├── resume_upload.html  # Resume/JD upload page
│   ├── interview.html      # Interview simulation page
│   └── feedback.html       # Feedback and analysis page
└── cv.py                   # Computer vision module for pose detection
```

## Architecture

This application follows a serverless architecture using AWS services:
1. Frontend hosted on AWS Amplify
2. API Gateway for handling HTTP requests and WebSocket connections
3. Lambda functions for backend processing
4. S3 for document storage
5. AI/ML services for analysis (Textract, Transcribe, Polly, Rekognition, Comprehend, Bedrock)
6. DynamoDB for storing user data, interview results, and feedback

## Usage

1. **Upload Documents**: Start by uploading your resume and the job description
2. **Prepare for Interview**: The system will analyze your resume and the job description to create personalized interview questions
3. **Practice Interview**: Engage in a realistic interview with the AI interviewer
4. **Receive Feedback**: Get comprehensive feedback on your performance, including technical content, communication skills, and body language
5. **Track Progress**: Monitor your improvement over time and focus on areas that need enhancement

## Development Roadmap

- [x] Basic UI implementation
- [x] Resume and job description upload
- [x] Simple interview simulation
- [x] Basic feedback UI
- [ ] AWS integration
- [ ] Serverless backend implementation
- [ ] Advanced AI/ML integration
- [ ] User authentication
- [ ] Progress tracking
- [ ] Mobile responsiveness enhancements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AWS Cloud services documentation
- MediaPipe for pose detection
- Bootstrap for UI components 