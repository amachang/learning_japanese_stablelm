import readline
import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM
from pathlib import Path
import time
import jinja2
import re
from stderr import sys

def main():
    tokenizer = LlamaTokenizer.from_pretrained("novelai/nerdstash-tokenizer-v1", additional_special_tokens=["▁▁"])

    ai_name = "AI子"
    ai_intro_phrases = [
        "名前はAI子。人口的に作られた知性の塊。",
        "職業はスーパーAI、なんでも質問に答えちゃう。",
        "人に優しく丁寧に接することがAIが市民権を得るために必要だと思うの。",
    ]

    user_name = "天野"
    user_intro_phrases = [
        "名前は天野です。",
        "趣味はプログラミングです。",
        "AIと楽しく話せる時代が来るのかな？そうしたら孤独は消滅する？そんなことを考えてます。",
    ]

    history = [
    ]

    model = AutoModelForCausalLM.from_pretrained(
        "stabilityai/japanese-stablelm-base-alpha-7b",
        trust_remote_code=True,
        variant="fp16",
    )
    model.half()
    model.eval()
    assert torch.cuda.is_available()
    model = model.to("cuda")

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("prompt_template"),
        autoescape=False,
    )
    template_env.filters["escape_name"] = escape_name
    template_env.filters["escape_phrase"] = escape_phrase

    max_new_tokens = 100

    while True:
        start_time = time.time()

        user_phrase = input("あなた：").strip();
        history.append((user_name, user_phrase))

        input_ids = make_prompt(template_env, history, {
            "ai": {
                "name": ai_name,
                "intro_phrases": ai_intro_phrases,
            },
            "user": {
                "name": user_name,
                "intra_phrases": user_intro_phrases,
            },
        }, 2048 - max_new_tokens - 1)

        new_phrase = None;
        while True:
            tokens = model.generate(
                input_ids.to(device=model.device),
                max_new_tokens=max_new_tokens,
                temperature=1,
                top_p=0.95,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                bos_token_id=tokenizer.bos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

            new_tokens = get_new_tokens(input_ids[0], tokens[0])
            if new_tokens is None:
                continue

            new_phrase = tokenizer.decode(new_tokens, skip_special_tokens=True)
            new_phrase = parse_new_phrase(new_phrase)
            if new_phrase is None:
                continue

            break

        history.append((ai_name, new_phrase))
        print(f"{ai_name}: {new_phrase}")

@jinja2.pass_eval_context
def escape_name(eval_ctx, value):
    return re.sub(r'[：:]', '', value)

@jinja2.pass_eval_context
def escape_phrase(eval_ctx, value):
    value = re.sub(r'「', '『', value)
    return re.sub(r'」', '』', value)

def make_prompt(template_env, history, personas, max_token_len):
    hostory_entry_count = bisect_search(0, len(history) + 1, lambda n: get_prompt_token_len(template_env, history, personas, n) < max_token_len)
    target_history = history[-history_entry_count:]
    return render(template_env, target_history, personas)

def bisect_search(start, end, fn):
    if end <= start + 1:
        return start
    middle = (start + end) // 2
    if fn(middle):
        return bisect_search(middle, end, fn)
    else:
        return bisect_search(start, middle, fn)

def get_prompt_token_len(template_env, history, personas, history_entry_count):
    target_history = history[-history_entry_count:]
    prompt = render(template_env, target_history, personas)
    input_ids = tokenizer.encode(
        prompt,
        add_special_tokens=False,
        return_tensors="pt"
    )
    return input_ids.shape[1]

def render(template_env, history, personas):
    template = template_env.get_template("001.j2");
    return template.render(history=history, personas=personas)

def get_new_tokens(input_tokens, output_tokens):
    input_len = len(input_tokens)
    output_len = len(output_tokens)

    if output_len < input_len:
        print("Short output", stderr)
        return None

    for i in range(input_len):
        if input_tokens[i] != output_tokens[i]:
            print("Unmatched leading inputs", stderr)
            return None

    return output_tokens[input_len:]

def parse_new_phrase(phrase):
    matches = re.search(r'(.*?)」', phrase)
    if matches is None:
        print("No closing かぎ括弧", stderr)
        return None

    phrase = matches.group(1)

    delimiters = {
        "'": "'",
        '"': '"',
        "(": ")",
        "{": "}",
        "[": "]",
        "❲": "❳",
        "⟮": "⟯",
        "（": "）",
        "｛": "｝",
        "【": "】",
        "〔": "〕",
        "‘": "’",
        "“": "”",
        "『": "』",
        "〘": "〙",
        "⦅": "⦆",
        "⟬": "⟭",
        "〖": "〗",
        "｢": "｣",
        "「": "」",
        "［": "］",
        "〚": "〛",
        "⟦": "⟧",
    }

    closing_delimiters = delimiters.values()

    stack = []
    for c in phrase:
        if delimiters.has(c):
            stack.append(delimiters[c])
        elif stack[-1] == c:
            stack = stack[:-1]
        elif c in closing_delimiters:
            print(f"Unmatched delimiter: {c}", file=stderr)
            return None

    return phrase



if __name__ == "__main__":
    main()


