import readline
import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM

def main():
    tokenizer = LlamaTokenizer.from_pretrained("novelai/nerdstash-tokenizer-v1", additional_special_tokens=['▁▁'])
    model = AutoModelForCausalLM.from_pretrained(
        "stabilityai/japanese-stablelm-base-alpha-7b",
        trust_remote_code=True,
    )
    model.half()
    model.eval()
    assert torch.cuda.is_available()
    model = model.to("cuda")

    while True:
        prompt = input("(q: quit)> ").strip()

        if prompt == "":
            continue

        if prompt == "q":
            print("終了します。")
            break

        input_ids = tokenizer.encode(
            prompt,
            add_special_tokens=False,
            return_tensors="pt"
        )

        tokens = model.generate(
            input_ids.to(device=model.device),
            max_new_tokens=128,
            temperature=1,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

        out = tokenizer.decode(tokens[0], skip_special_tokens=True)
        print(f"{out}")

if __name__ == "__main__":
    main()

