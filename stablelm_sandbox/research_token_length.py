import readline
import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM

def main():
    tokenizer = LlamaTokenizer.from_pretrained("novelai/nerdstash-tokenizer-v1", additional_special_tokens=['▁▁'])
    while True:
        prompt = input("> ").strip()

        if prompt == "":
            continue

        if prompt in { "exit", "quit", "q" }:
            print("終了します。")
            break

        input_ids = tokenizer.encode(
            prompt,
            add_special_tokens=False,
            return_tensors="pt"
        )

        tokens = input_ids[0];
        print({
            "length": len(tokens),
            "tokens": tokens,
            "rebuild_prompt": tokenizer.decode(tokens)
        });

if __name__ == "__main__":
    main()

