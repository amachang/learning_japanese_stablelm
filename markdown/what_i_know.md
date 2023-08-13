# わかったこと

- 基本
  - [このモデルを使う](https://huggingface.co/stabilityai/japanese-stablelm-instruct-alpha-7b)
- とりあえず分かる範囲で必要なライブラリとか
  - torch
  - transformers
  - einops
  - sentencepiece
  - cuda
- 新しいものなので ChatGPT はこの作業の役には立たない
- ML の基礎知識的なこと
  - AutoModelForCausalLM ってどんなモデル
    - 文章の続きを書いたり、会話に回答したりする出力ヘッドを持つモデル。 CLM とか略すらしい
  - NIDIA/Megatron-LM という transformer ベースのモデルの学習を大規模高速化するための手法を使っている。 GPT-NeoX というのがその環境とかツールキットの名前
    - StableLM はそれで学習され huggingface 用に変換されて公開されている

# わかってないこと

- 関連ライブラリの version とかはどんな感じ？
- GCP でどのくらいのインスタンスが必要？
  - 使うのに正味どのくらいのお金かかる？
- いい感じの Web UI とかある？
- 架空や実在の人物の mimic と会話することってできるんですか？
  - 故人とか
  - 歴史上の人物とか
  - アイドルとか
  - 小説の中の人物とか
- いい感じの Web UI とかってすでに開発されてる？最悪 X 経由でアクセス可能な GUI でも良い。
- ネット小説とか学習させたら、その中のキャラになってくれるの？
- 追加学習の手法は？
  - few shot, one shot は?
  - dream booth 的な手法はどう？
  - every dream 的な手法はどう？
  - lora は？
- モデルシェアサイトはすでにある？
- chichipui 的な小説サイトは可能性あるの？人格を公開して遊ぶ感じ？ディストピア？
- decoder-only model って何？
  - encoder は他のモデルの使ってますってことですかね
- [requirements.txt](https://huggingface.co/stabilityai/japanese-stablelm-instruct-alpha-7b/blob/main/requirements.txt) には `sentencepiece` `einops` しか書いてないけど、 transformers とかはいらないのか？
  - 自分は huggingface リポジトリのことわかってないかもしれない

