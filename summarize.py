from .utils import estimate_tokens, gpt3_completion, read_file

def summarize_text(text, target_tokens, count=3, engine='text-curie-001', tokens=2048):

    tokens = estimate_tokens(text)

    if tokens <= target_tokens:
        return text, tokens

    if count <= 0:
         return text, tokens

    # Give us some room to work with
    summary_size = "detailed"

    # If this is our last try, then go to extremes to get the target number of tokens
    if count == 1:
        summary_size = "concise"
        tokens = target_tokens
        engine='text-davinci-003'

    summary_size = "concise" if count <= 1 else "detailed"
    prompt = "Create a %s summary of the following text in approximately %s words. Ensure all major entities are represented in the summary.\n\nTEXT: %s\n\nSUMMARY:" % (summary_size, int(0.75*target_tokens), text)

    summary_text = gpt3_completion(prompt, engine=engine, tokens=tokens)
    print ("%s GPT3 returned %d (%s) tokens" % (count, estimate_tokens(summary_text), estimate_tokens(text)))

    return summarize_text(summary_text, target_tokens, count-1, engine=engine, tokens=tokens)

