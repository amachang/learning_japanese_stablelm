import torch
from transformers import LlamaTokenizer, AutoModelForCausalLM

tokenizer = LlamaTokenizer.from_pretrained("novelai/nerdstash-tokenizer-v1", additional_special_tokens=['▁▁'])

model = AutoModelForCausalLM.from_pretrained(
    "stabilityai/japanese-stablelm-base-alpha-7b",
    trust_remote_code=True,
)
model.half()
model.eval()

if torch.cuda.is_available():
    model = model.to("cuda")

prompt = """
AI で科学研究を加速するには、
""".strip()

input_ids = tokenizer.encode(
    prompt,
    add_special_tokens=False,
    return_tensors="pt"
)

# this is for reproducibility.
# feel free to change to get different result
seed = 23  
torch.manual_seed(seed)

tokens = model.generate(
    input_ids.to(device=model.device),
    max_new_tokens=128,
    temperature=1,
    top_p=0.95,
    do_sample=True,
)

out = tokenizer.decode(tokens[0], skip_special_tokens=True)
print(out)
"""
AI で科学研究を加速するには、データ駆動型文化が必要であることも明らかになってきています。研究のあらゆる側面で、データがより重要になっているのです。
20 世紀の科学は、研究者が直接研究を行うことで、研究データを活用してきました。その後、多くの科学分野ではデータは手動で分析されるようになったものの、これらの方法には多大なコストと労力がかかることが分かりました。 そこで、多くの研究者や研究者グループは、より効率的な手法を開発し、研究の規模を拡大してきました。21 世紀になると、研究者が手動で実施する必要のある研究は、その大部分を研究者が自動化できるようになりました。
"""

