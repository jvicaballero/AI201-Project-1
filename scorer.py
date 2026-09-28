def judge(question: str, expects, answer: str, results) -> bool:
    """Pass if the answer contains `expects` — or, if `expects` is a list of
    alternative phrasings, if it contains any one of them. The generation
    model doesn't always phrase the same fact the same way ("10%" vs
    "ten percent"), so some expects values list the phrasings we've actually
    seen instead of a single exact string.
    """
    if not expects:
        return False

    alternatives = expects if isinstance(expects, (list, tuple)) else [expects]
    answer_lower = (answer or "").lower()
    return any(alt.strip().lower() in answer_lower for alt in alternatives)