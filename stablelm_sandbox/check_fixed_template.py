import readline
import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM
from pathlib import Path
import time

def main():
    tokenizer = LlamaTokenizer.from_pretrained("novelai/nerdstash-tokenizer-v1", additional_special_tokens=['▁▁'])

    prompt = Path('prompt_template').joinpath('000.j2').read_text();
    input_ids = tokenizer.encode(
        prompt,
        add_special_tokens=False,
        return_tensors="pt"
    )

    input_token_length = input_ids.shape[1];
    print(f"Template Tokens: {input_token_length}");

    model = AutoModelForCausalLM.from_pretrained(
        "stabilityai/japanese-stablelm-base-alpha-7b",
        trust_remote_code=True,
    )
    model.half()
    model.eval()
    assert torch.cuda.is_available()
    model = model.to("cuda")

    while True:
        start_time = time.time()

        tokens = model.generate(
            input_ids.to(device=model.device),
            max_new_tokens=2048 - 1 - input_token_length,
            temperature=1,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

        out = tokenizer.decode(tokens[0], skip_special_tokens=True)
        print(f"------------------------------")
        print(f"{out}")
        print(f"------------------------------")
        print(f"Output Tokens: {len(tokens[0])}");
        print(f"Time: {time.time() - start_time} sec");

if __name__ == "__main__":
    main()

