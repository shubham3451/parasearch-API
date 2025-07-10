def tokenize_paragraphs(text):
    """
    Split the input text into paragraphs using two newlines,
    and yield each paragraph with its list of normalized words.
    """
    paragraphs = [p.strip() for p in text.strip().split('\n\n') if p.strip()]
    for para in paragraphs:
        words = [word.lower() for word in para.split()]
        yield para, words




