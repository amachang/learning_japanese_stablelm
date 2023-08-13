# 作業ログ

- github repo 作った
- what i know メモを作った
- 念の為確認したが ChatGPT は Stable Diffusion も StableLM もない時代の知識らしい
- 各種必要な環境を調べる
  - StableLM Instruct の方の Huggingface のページでも読む
- 軽くサンプルコードや requirements をみて、派生的な知識を得る
- huggingface のファイル群をざっと見る
- 最終的には GKE で使うときだけ Web UI を立ち上げるみたいにしたいけど、一旦普通の Compute Engine インスタンスを立てる
  - どのくらいだろとりあえず T4 / n1-highmem-8 / Ubuntu 22.04 / 100 GB / スポットくらいな感じで。こういうとき Ubuntu じゃないほうが良いんだろうか
    - 0.36 USD/hour
      - 消し忘れたら月 30000 円くらい飛ぶ感じで
    - 慣れてるって理由だけで Ubuntu だけど。どのディストリビューションに何が入ってるか全く知らない
  - スポットだから別のゾーンじゃないと借りられないかなとかも検討してたけど、すんなり instance allocation された
- Compute Engine のセットアップスクリプトは[scripts/setup\_instance.sh](scripts/setup_instance.sh)にまとめていく

