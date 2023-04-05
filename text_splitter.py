import re
from .utils import estimate_tokens
import textwrap

def chunk_text(text, token_size=2000, regex_type='sentence'):

    text += '\n'; # Add a newline to the end of the text to ensure the last chunk is included

    # Define regular expressions for splitting text into sentences or paragraphs
    if regex_type == 'sentence':
        regex = r'[^.!?]+[.!?]'
    elif regex_type == 'paragraph': # This is not working
        regex = r'\n{2,}' # r'\n\s*\n'
    else:
        raise ValueError("Invalid regex type: must be 'sentence' or 'paragraph'")

    # Split text into chunks using the specified regular expression
    chunks = re.findall(regex, text)
    # chunks = text.split('\n\n')

    # Initialize an empty list to store the filtered chunks
    filtered_chunks = []

    # Initialize a variable to keep track of the current chunk
    current_chunk = ""
    len_current_chunk = 0

    # Iterate over each chunk
    for chunk in chunks:

        # chunk = textwrap.wrap(chunk, token_size*5, drop_whitespace=False, replace_whitespace=False)

        len_chunk = estimate_tokens(chunk)

        # Check if adding the current chunk to the filtered chunks will make it longer than the specified chunk size
        if len_current_chunk + len_chunk > token_size:

            print (current_chunk, "\n==\n")
            # If so, add the current chunk to the list of filtered chunks and start a new chunk
            filtered_chunks.append(current_chunk)
            current_chunk = ""
            len_current_chunk = 0


        # Add the current chunk to the current filtered chunk
        current_chunk += chunk
        len_current_chunk += len_chunk

    # Add any remaining text as a final filtered chunk
    if current_chunk:
        filtered_chunks.append(current_chunk)

    return filtered_chunks


