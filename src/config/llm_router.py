import os
from dotenv import load_dotenv
from lightrag.llm.openai import openai_complete_if_cache
from src.config.reranker import MAX_INPUT_TOKENS, MAX_OUTPUT_TOKENS

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
VISION_MODEL = os.getenv("VISION_MODEL")

def truncate_to_token_limit(text, max_tokens=MAX_INPUT_TOKENS):
    tokens = text.split()
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        return " ".join(tokens) + "..."
    return text

def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
    prompt = truncate_to_token_limit(prompt)
    history = history_messages[-5:] if history_messages else []
    return openai_complete_if_cache(
        LLM_MODEL,
        prompt,
        system_prompt=system_prompt,
        history_messages=history,
        api_key=API_KEY,
        base_url=BASE_URL,
        max_tokens=MAX_OUTPUT_TOKENS,
        temperature=0.3,
        **kwargs,
    )

def vision_model_func(prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs):
    prompt = truncate_to_token_limit(prompt)
    try:
        if messages:
            return openai_complete_if_cache(
                VISION_MODEL, "", system_prompt=None, history_messages=[],
                messages=messages, api_key=API_KEY, base_url=BASE_URL,
                max_tokens=MAX_OUTPUT_TOKENS, **kwargs
            )
        elif image_data:
            return openai_complete_if_cache(
                VISION_MODEL, "", system_prompt=None, history_messages=[],
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]
                }],
                api_key=API_KEY, base_url=BASE_URL,
                max_tokens=MAX_OUTPUT_TOKENS, **kwargs
            )
        else:
            return llm_model_func(prompt, system_prompt, history_messages, **kwargs)
    except Exception as e:
        print(f"[Vision fallback] {e}")
        return llm_model_func(prompt, system_prompt, history_messages, **kwargs)
