import asyncio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
import pyaudio

# import your save/upload helpers
from upload import save_transcript_to_file, upload_to_s3, BUCKET_NAME

# ===================== Event Handler =====================
class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream, transcript_accumulator):
        super().__init__(transcript_result_stream)
        self.acc = transcript_accumulator

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        for result in transcript_event.transcript.results:
            # Only handle final results
            if not result.is_partial:
                for alt in result.alternatives:
                    line = alt.transcript
                    print(line)
                    self.acc.append(line)

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

    # Accumulate every final line here
    all_lines = []
    handler = MyEventHandler(stream.output_stream, all_lines)

    # Run mic capture and event handling side by side
    tasks = [
        asyncio.create_task(write_microphone(stream)),
        asyncio.create_task(handler.handle_events())
    ]

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        # Stop on Ctrl-C
        for t in tasks:
            t.cancel()
        print("\n🛑 KeyboardInterrupt caught, wrapping up…")
    finally:
        # 1) Save locally
        fname = save_transcript_to_file(all_lines)
        # 2) Upload to S3
        upload_to_s3(fname, BUCKET_NAME)

if __name__ == "__main__":
    asyncio.run(main())
