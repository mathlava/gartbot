# がーとぼっと
がーと([Twitter](https://twitter.com/kinder_Gart_en)) が作り始めた，主に数学を愛する会([Twitter](https://twitter.com/mathlava?s=20))の Discord サーバーで動かしている Discord の Bot です．
現在は他のサーバーへの招待リンクは発行していません．

## 公式 Discord サーバー
https://discord.gg/7gypE3Q

## 必要要件
- Linux or macOS
- Python3
- TeXLive
- Poppler (pdftoppm)
- ImageMagick (convert)

## テスト方法
`.env` を作り
```
DISCORD_TOKEN="Your_Discord_Bot_Token"
```
とする．

`config.json` を作り
```json
{
    "prefix": "!"
}
```
とする．

シェルで
```
pip install -r requirements.txt
```
を実行する．

`gartbot.py` を Python3 で実行する．
