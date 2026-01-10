import os
import re
import random
import difflib
import time
import sys


class ChatBot:
    def __init__(self, kb_path=None):
        self.name = "highxbot"
        if kb_path is None:
            kb_path = os.path.join(os.path.dirname(__file__), "knowledge.txt")
        self.kb = self.load_knowledge(kb_path)
        self.fallbacks = [
            "Sorry, I don't know that. Can you rephrase?",
            "I'm not sure — try asking in a different way.",
            "I don't have an answer for that right now."
        ]
        self.greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]

    def typing_effect(self, text, delay=0.03):
        """Print text with typing effect (character by character)."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()  # newline after typing

    def load_knowledge(self, path):
        kb = {}
        if not os.path.exists(path):
            return kb
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # split at first '|'
                if '|' in line:
                    q, a = line.split('|', 1)
                    # normalize stored questions to match preprocessing
                    q = re.sub(r"[^a-z0-9\s]", "", q.strip().lower())
                    a = a.strip()
                    if q:
                        kb[q] = a
        return kb

    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text.strip()

    def best_kb_match(self, text):
        # Exact match first
        if text in self.kb:
            return self.kb[text]

        words = set(text.split())
        best = None
        best_score = 0
        for q, a in self.kb.items():
            q_words = set(q.split())
            score = len(words & q_words)
            if score > best_score:
                best_score = score
                best = a
        if best_score > 0:
            return best

        # Fallback: fuzzy match against stored questions
        try:
            keys = list(self.kb.keys())
            close = difflib.get_close_matches(text, keys, n=1, cutoff=0.72)
            if close:
                return self.kb[close[0]]
        except Exception:
            pass

        return None

    def respond(self, user_input):
        if not user_input or not user_input.strip():
            return "Please say something."

        t = self.preprocess(user_input)
        if any(g in t for g in self.greetings):
            return random.choice(["Hello!", "Hi there!", "Hey — how can I help?"])

        if t in ("exit", "quit", "bye", "goodbye"):
            return "Bye!"

        # Try knowledge base
        kb_answer = self.best_kb_match(t)
        if kb_answer:
            return kb_answer

        # Small heuristics
        if t.isdigit():
            return "You entered a number: %s" % t

        return random.choice(self.fallbacks)

    def chat_loop(self):
        print(f"{self.name} — type 'exit' or 'quit' to stop")
        while True:
            try:
                user = input("You: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            
            # Add delay before responding (like ChatGPT thinking)
            time.sleep(0.5)
            
            resp = self.respond(user)
            print(f"{self.name}: ", end="", flush=True)
            self.typing_effect(resp, delay=0.03)
            
            if user.strip().lower() in ("exit", "quit", "bye", "goodbye"):
                break


if __name__ == "__main__":
    bot = ChatBot()
    bot.chat_loop()
