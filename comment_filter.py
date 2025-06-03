def is_spam(comment):
    bad_keywords = ["subscribe", "click here", "free", "check this", "http", "www"]
    return any(word in comment.lower() for word in bad_keywords)

def has_link(comment):
    return "http" in comment or "www." in comment

def is_useful(comment):
    return len(comment.split()) > 5 and not is_spam(comment)