from collections import defaultdict

MAX_HISTORY = 20


class ConversationStore:
    def __init__(self):
        self._store: dict[str, list[dict]] = defaultdict(list)

    def get(self, phone: str) -> list[dict]:
        return self._store[phone]

    def append(self, phone: str, role: str, content: str) -> None:
        self._store[phone].append({"role": role, "content": content})
        # Keep only the last MAX_HISTORY messages to stay within Claude's context
        if len(self._store[phone]) > MAX_HISTORY:
            self._store[phone] = self._store[phone][-MAX_HISTORY:]

    def clear(self, phone: str) -> None:
        self._store[phone] = []


store = ConversationStore()
