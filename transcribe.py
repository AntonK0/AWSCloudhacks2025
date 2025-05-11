import asyncio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
import pyaudio
import boto3
import os
import json
import time
import requests

# Initialize AWS clients
s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')

def transcribe_audio_file(s3_bucket, s3_key):
    """
    Transcribe an audio file from S3 using Amazon Transcribe
    """
    try:
        # Start transcription job
        job_name = f"transcription-{os.path.basename(s3_key)}"
        
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{s3_bucket}/{s3_key}'},
            MediaFormat='webm',
            LanguageCode='en-US'
        )
        
        # Wait for transcription to complete
        while True:
            status = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            time.sleep(5)
        
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            # Get the transcript
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcript_response = requests.get(transcript_uri)
            transcript_data = transcript_response.json()
            
            # Extract the transcript text
            transcript_text = transcript_data['results']['transcripts'][0]['transcript']
            
            # Delete the transcription job
            transcribe_client.delete_transcription_job(
                TranscriptionJobName=job_name
            )
            
            return transcript_text
        else:
            raise Exception(f"Transcription failed: {status['TranscriptionJob']['FailureReason']}")
            
    except Exception as e:
        print(f"Error in transcription: {str(e)}")
        return None
# ===================== Event Handler =====================
class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        for result in transcript_event.transcript.results:
            # Only print final results, skip partials for clarity
            if not result.is_partial:
                for alt in result.alternatives:
                    print(alt.transcript)

# ================ Real-Time Audio Capture =================
async def write_microphone(stream):
    RATE = 16000             # sample rate expected by Transcribe
    CHUNK = 1024             # how many frames per buffer
    FORMAT = pyaudio.paInt16 # 16-bit signed int PCM
    CHANNELS = 1             # mono audio

    pa = pyaudio.PyAudio()
    mic = pa.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)

    try:
        while True:
            data = mic.read(CHUNK, exception_on_overflow=False)
            await stream.input_stream.send_audio_event(audio_chunk=data)
    except asyncio.CancelledError:
        # If the gather() is cancelled, end the stream
        pass
    finally:
        await stream.input_stream.end_stream()
        mic.stop_stream()
        mic.close()
        pa.terminate()

# ======================== Main ============================
async def main():
    client = TranscribeStreamingClient(region="us-west-2")

    # Start the bidirectional transcription stream
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )

    handler = MyEventHandler(stream.output_stream)

    # Run mic capture and event handling side by side
    await asyncio.gather(
        write_microphone(stream),
        handler.handle_events()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTranscription stopped.")

