# Description: Utility functions for the project
import os
import json
import openai
import math
from time import time, sleep
from uuid import uuid4
from transformers import GPT2Tokenizer

openai.api_key = os.environ['OPENAI_API_KEY']

# alias of open_file
def open_file(filename):
    return read_file(filename)

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            return infile.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as infile:
            contents = infile.read()
            return contents.encode('ascii', 'ignore').decode('utf-8')

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def format_counter(c, w=4):
    return f"{c:0{w}d}"

def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

def flatten_convo(conversation):
    convo = ''
    for i in conversation:
        convo += '%s: %s\n' % (i['role'].upper(), i['content'])
    return convo.strip()


# Allows for a prompt to be split into a system and a prompt, if the system exists
def parse_prompt(prompt):
    # Encode the prompt as ASCII
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()

    # Split the prompt into lines
    if prompt.strip().startswith("SYSTEM:"):

        full_document = prompt.replace("SYSTEM:", "").lstrip()
        paragraphs = full_document.split('\n\n')

        system = paragraphs.pop(0)
        prompt = '\n\n'.join(paragraphs)

        return {'full_document': full_document, 'system': system, 'prompt': prompt}
    else:
        # If the first line does not start with "SYSTEM:", return full document, '', full document
        full_document = prompt.strip()
        return {'full_document': full_document, 'system': '', 'prompt': full_document}

#
def gpt3x_completion(prompt, model='gpt-3.5-turbo', temp=0.4, top_p=1.0, tokens=0, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
  gpt4_completion(prompt, model='gpt-3.5-turbo', temp=temp, top_p=top_p, tokens=tokens, freq_pen=freq_pen, pres_pen=pres_pen, stop=stop)

def gpt4_completion(prompt, model='gpt-4', temp=0.4, top_p=1.0, tokens=0, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):

    messages = []
    prompt_parts = parse_prompt(prompt)

    if (prompt_parts['system'] != ''):
            # We have a system param in the endpoint, so we can use it
            messages.append({'role': 'system', 'content': prompt_parts['system']})

    messages.append({'role': 'user', 'content': prompt_parts['prompt']})

    return chatgpt_completion(messages, model=model, temp=temp, top_p=top_p, tokens=tokens, freq_pen=freq_pen, pres_pen=pres_pen, stop=stop)


# def chatgpt_completion(messages, model="gpt-3.5-turbo"):
#     response = openai.ChatCompletion.create(model=model, messages=messages)
#     text = response['choices'][0]['message']['content']
#     filename = 'chat_%s_muse.txt' % time()
#     if not os.path.exists('chat_logs'):
#         os.makedirs('chat_logs')
#     save_file('chat_logs/%s' % filename, text)
#     return text


# model='gpt-4'
def chatgpt_completion(messages, model='gpt-3.5-turbo', temp=0.4, top_p=1.0, tokens=0, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0

    model_max_tokens = 4000
    if (model == 'gpt-4'):
        model_max_tokens = 8000

    flat_conversation = flatten_convo(messages)

    if (tokens == 0):
      tokens = model_max_tokens - estimate_tokens(flat_conversation)

    if (tokens < 100):
       return "Chat-GPT error: %s" % "Not enough tokens to generate a response (internal error)"


    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['message']['content'].strip()
            #text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()

            # Check if the subdirectory exists
            if not os.path.exists('logs_chat'):
                # If the subdirectory doesn't exist, create it
                os.mkdir('logs_chat')

            save_file('logs_chat/%s' % filename, flat_conversation + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "Chat-GPT error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def gpt3_completion(prompt, engine='text-davinci-003', temp=0.4, top_p=1.0, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0

    prompt_parts = parse_prompt(prompt)

    # We don't have a system param in the endpoint, so we can just use the full document
    prompt = prompt_parts['full_document']

    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            #text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()

            # Check if the subdirectory exists
            if not os.path.exists('gpt3_logs'):
                # If the subdirectory doesn't exist, create it
                os.mkdir('gpt3_logs')

            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

# See: https://medium.com/@nils_reimers/openai-gpt-3-text-embeddings-really-a-new-state-of-the-art-in-dense-text-embeddings-6571fe3ec9d9
# for alternative embedding methods
def gpt3_embedding(content, engine='text-embedding-ada-002'):
    content = content.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Embedding.create(input=content,engine=engine)
    vector = response['data'][0]['embedding']  # this is a normal list
    return vector

def create_prompt(string, data):
    if string.endswith('.txt'):
        return create_prompt_from_file(string, data)
    else:
        return create_prompt_from_string(string, data)

def create_prompt_from_file(template_file, data):
    template_path1 = os.path.join(os.path.dirname(__file__), 'templates/')
    template_path2 = os.path.join(os.path.dirname(__file__), '../templates/')

    if (not template_file.endswith('.txt')):
         template_file += '.txt'

    if os.path.exists(template_path1 + template_file):
        template_string = read_file(template_path1 + template_file)
    elif os.path.exists(template_path2 + template_file):
        template_string = read_file(template_path2 + template_file)
    else:
        return ''

    return create_prompt_from_string(template_string, data)

def create_prompt_from_string(template_string, data):
    data['uuid'] = str(uuid4())
    for key, value in data.items():
        template_string = template_string.replace("<<" + key.upper() + ">>", str(value))
    return template_string

def estimate_tokens(text):
    words = text.split()
    num_words = len(words)
    num_tokens = math.ceil(1.25 * num_words)
    return num_tokens

def estimate_tokens_real(text):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokens = tokenizer.encode(text)
    return len(tokens)
