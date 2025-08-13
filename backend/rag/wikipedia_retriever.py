import wikipedia

class WikipediaRetriever:
    def __init__(self):
        pass

    def retrieve(self, query: str, sentences: int = 2) -> str:
        try:
            page = wikipedia.page(query)
            summary = wikipedia.summary(query, sentences=sentences)
            return f"Wikipedia: {summary}"
        except wikipedia.DisambiguationError as e:
            option = e.options[0]
            try:
                summary = wikipedia.summary(option, sentences=sentences)
                return f"Wikipedia (disambiguated): {summary}"
            except Exception:
                return "Wikipedia: No clear summary found."
        except Exception:
            return "Wikipedia: No relevant information found."
