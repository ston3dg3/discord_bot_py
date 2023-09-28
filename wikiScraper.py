import wikipedia

def wikiSearches(query):
    try:
        results = wikipedia.search(query)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return e.options

def wikiSummary(page_title):
    try:
        summary = wikipedia.summary(page_title)
        return summary
    except wikipedia.exceptions.DisambiguationError:
        return "You are as vague as a chameleon trying to hide in a room full of rainbows!"