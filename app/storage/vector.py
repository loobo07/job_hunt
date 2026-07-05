import re


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9+#.]+", text.lower()))


class DeterministicVectorStore:
    def similarity(self, query: str, document: str) -> float:
        query_tokens = _tokens(query)
        document_tokens = _tokens(document)
        if not query_tokens or not document_tokens:
            return 0.0
        return len(query_tokens & document_tokens) / len(query_tokens | document_tokens)
