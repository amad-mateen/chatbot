import os
import re
from typing import List, Tuple

class SimpleRetriever:
    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.qa_pairs = self._load_kb()

    def _load_kb(self) -> List[Tuple[str, str]]:
        qa_pairs = []
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Split by double newlines, then by first line/question
        blocks = re.split(r'\n\n+', content)
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                question = lines[0].strip()
                answer = ' '.join(lines[1:]).strip()
                qa_pairs.append((question, answer))
        return qa_pairs

    def retrieve(self, query: str, top_k: int = 1) -> List[Tuple[str, str]]:
        # Simple keyword overlap scoring
        query_words = set(re.findall(r'\w+', query.lower()))
        scored = []
        for q, a in self.qa_pairs:
            kb_words = set(re.findall(r'\w+', q.lower()))
            score = len(query_words & kb_words)
            scored.append((score, q, a))
        scored.sort(reverse=True)
        return [(q, a) for score, q, a in scored[:top_k] if score > 0]
