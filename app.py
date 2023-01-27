import os
from slack_bolt import App

import degreer

# ボットトークンと署名シークレットでアプリを初期化
app = App(
    token='xoxb-4658828931218-4658721256579-g7JxcYfcQG2BDYe0rCN6kMdX',
    signing_secret='ea138abb01c0b890196f978fe0d5b72f'
)


@app.message(degreer.keyRegex)
def convert_chord(message, say):
    # テキストを取得
    msg : str = message['text']

    if degreer.isInvalid(msg):
        say('形式が違う、見直してくれ')
        return

    # 送信
    say(degreer.convert2Degree(msg))


# 起動
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))