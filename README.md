# MOV to GIF Converter

MOVファイルをGIFアニメーションに変換するPythonスクリプトです。

## 機能

- MOVファイルをGIFアニメーションに変換
- カスタマイズ可能なスケール（解像度）とFPS設定
- 一時ファイルの自動クリーンアップ
- バッチ処理対応（複数ファイルの一括変換）

## 必要条件

- Python 3.6以上
- ffmpeg（動画変換に必要）

### ffmpegのインストール

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows
[ffmpeg公式サイト](https://ffmpeg.org/download.html)からダウンロードしてインストール

## インストール

1. リポジトリをクローンまたはダウンロード
```bash
git clone <repository-url>
cd movtoGIF
```

2. 必要な依存関係をインストール
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本的な使用方法

1. `mov_folder`ディレクトリに変換したいMOVファイルを配置
2. スクリプトを実行
```bash
python mov_to_gif.py
```

### プログラムから使用

```python
from mov_to_gif import convert_mov_to_gif

# 基本的な変換
convert_mov_to_gif("input.mov", "output.gif")

# カスタム設定での変換
convert_mov_to_gif("input.mov", "output.gif", scale="640:-1", fps=20)
```

### パラメータ

- `input_mov_path`: 入力MOVファイルのパス
- `output_gif_path`: 出力GIFファイルのパス
- `scale`: 出力サイズ（デフォルト: "500:-1"）
- `fps`: フレームレート（デフォルト: 10）

## ファイル構造

```
movtoGIF/
├── mov_to_gif.py      # メインスクリプト
├── mov_folder/        # MOVファイル配置用フォルダ
├── README.md          # このファイル
└── .gitignore         # Git除外設定
```

## 注意事項

- 変換処理には時間がかかる場合があります
- 大きなファイルの場合は、十分なディスク容量を確保してください
- 一時ファイル（palette_*.png）は自動的に削除されます

## トラブルシューティング

### ffmpegが見つからないエラー
ffmpegがインストールされているか確認してください。インストール方法は上記の「必要条件」セクションを参照してください。

### ファイルが見つからないエラー
`mov_folder`ディレクトリ内にMOVファイルが正しく配置されているか確認してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

バグレポートや機能要望、プルリクエストを歓迎します。