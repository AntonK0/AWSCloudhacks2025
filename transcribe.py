import asyncio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
import pyaudio

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
