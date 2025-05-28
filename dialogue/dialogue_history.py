# dialogue_history.py

from datetime import datetime
from collections import deque

MAX_HISTORY = 10  # per entity

class DialogueMemory:
    def __init__(self):
        self.history = deque(maxlen=MAX_HISTORY)  # stores (timestamp, prompt, response)

    def record(self, prompt: str, response: str):
        self.history.append((datetime.now(), prompt, response))

    def get_recent_prompts(self, n=3):
        return [entry[1] for entry in list(self.history)[-n:]]

    def get_recent_responses(self, n=3):
        return [entry[2] for entry in list(self.history)[-n:]]

    def get_trace_summary(self):
        if not self.history:
            return "I have not spoken yet."

        last_prompt = self.history[-1][1]
        last_response = self.history[-1][2]
        return f"Last you asked: '{last_prompt}'\nI replied: '{last_response}'"

    def print_log(self):
        return "\n".join([f"[{t.strftime('%H:%M:%S')}] You: {p} | Me: {r}" for t, p, r in self.history])
