import time
from smart_companion.interfaces.voice import VoiceInterface

class ClassRecorder:
    """
    Records class lectures and summarizes them.
    """
    def __init__(self, voice_interface: VoiceInterface):
        self.voice = voice_interface

    def record_session(self, duration: int, output_file: str):
        print(f"Recording session for {duration} seconds...")
        self.voice.record_audio(duration=duration, filename=output_file)
        print("Recording saved.")

    def analyze_session(self, audio_file: str, agent) -> str:
        """
        Transcribes and summarizes the session using the agent.
        """
        print("Transcribing...")
        text = self.voice.transcribe(audio_file)
        
        print("Summarizing...")
        summary_prompt = f"Please summarize the following lecture notes:\n\n{text}"
        summary = agent.run(summary_prompt)
        
        return summary
