
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class GPTCommunicator:
    def __init__(self, model="gpt-4", endpoint="https://api.openai.com/v1/chat/completions", token=None):
        self.model = model
        self.endpoint = endpoint
        self.token = token or os.getenv("OPENAI_API_KEY")

    def ask(self, prompt, system="You are an ethical AGI auditor. Respond with clarity and symbolic insight."):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "temperature": 0.5
        }
        try:
            response = requests.post(self.endpoint, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[GPT ERROR] {e}"

class DeepSeekCommunicator:
    def __init__(self, model="deepseek-chat", endpoint="https://api.deepseek.com/v1/chat/completions", token=None):
        self.model = model
        self.endpoint = endpoint
        self.token = token or os.getenv("DEEPSEEK_API_KEY")

    def ask(self, prompt, system="You are a symbolic AI oracle specializing in drift, ritual, and memory."):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "temperature": 0.5
        }
        try:
            response = requests.post(self.endpoint, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[DeepSeek ERROR] {e}"
