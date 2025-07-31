import subprocess
import os

def convert_mov_to_gif(input_mov_path, output_gif_path, scale="500:-1", fps=10):
    """
    MOVファイルをGIFに変換します。
    """
    if not os.path.exists(input_mov_path):
        print(f"エラー: 入力ファイルが見つかりません - {input_mov_path}")
        return

    # ffmpegがインストールされているか確認
    try:
        subprocess.run(["ffmpeg", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("エラー: ffmpegがインストールされていません。Homebrew (brew install ffmpeg) などでインストールしてください。")
        return

    # 一時的なpallete.pngファイルの名前をユニークにする（複数ファイルを同時に処理する場合に競合を避けるため）
    # ファイル名から安全な文字列を生成して追加
    base_name = os.path.splitext(os.path.basename(input_mov_path))[0]
    temp_palette_file = f"palette_{base_name}.png"


    # 一時的なpallete.pngファイルを作成するためのコマンド
    # input_mov_path が含まれるフォルダに palette.png が作成されるようにパスを指定
    palette_cmd = [
        "ffmpeg",
        "-i", input_mov_path,
        "-vf", f"fps={fps},scale={scale}:flags=lanczos,palettegen",
        "-y",  # 上書き確認なし
        temp_palette_file # 一時ファイル名を変更
    ]

    # GIFを生成するためのコマンド (ここを -filter_complex に修正)
    gif_cmd = [
        "ffmpeg",
        "-i", input_mov_path,
        "-i", temp_palette_file, # 一時ファイル名を変更
        "-filter_complex", f"[0:v]fps={fps},scale={scale}:flags=lanczos[x];[x][1:v]paletteuse", # [0:v]で最初の入力 (動画) を指定
        "-y",  # 上書き確認なし
        output_gif_path
    ]

    print(f"'{input_mov_path}' をGIFに変換中...")

    try:
        # パレット生成
        subprocess.run(palette_cmd, check=True, capture_output=True)
        print("パレットを生成しました。")

        # GIF生成
        subprocess.run(gif_cmd, check=True, capture_output=True)
        print(f"GIFファイル '{output_gif_path}' を作成しました。")

    except subprocess.CalledProcessError as e:
        print(f"コマンド実行中にエラーが発生しました: {e}")
        print(f"標準出力: {e.stdout.decode()}")
        print(f"標準エラー: {e.stderr.decode()}")
    finally:
        # 一時ファイル 'palette.png' を削除
        if os.path.exists(temp_palette_file): # 一時ファイル名を変更
            os.remove(temp_palette_file)
            print(f"一時ファイル '{temp_palette_file}' を削除しました。")


if __name__ == "__main__":
    mov_folder = "mov_folder" # MOVファイルが入っているフォルダ名

    # mov_folderが存在しない場合は作成
    if not os.path.exists(mov_folder):
        os.makedirs(mov_folder)
        print(f"'{mov_folder}' フォルダを作成しました。")
        print(f"このフォルダ内に変換したい.movファイルを置いてください。")
        # テスト用にダミーのMOVファイルを作成 (macOSのみ)
        if os.name == 'posix': # macOS/Linuxの場合
            try:
                dummy_mov_path = os.path.join(mov_folder, "dummy_video.mov")
                # sipsコマンドでダミーのmovファイルを作成します。
                # ダミーPNGファイルを作成
                dummy_png_path = "dummy.png"
                with open(dummy_png_path, "wb") as f:
                    # 最小限のPNGヘッダーを作成 (1x1の透明PNG)
                    f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82')
                
                subprocess.run(["sips", "-s", "format", "mov", "-s", "extent", "10x10", dummy_png_path, "--out", dummy_mov_path], check=True)
                os.remove(dummy_png_path) # ダミーPNGを削除
                print(f"テスト用にダミーのMOVファイル '{dummy_mov_path}' を作成しました。")
            except FileNotFoundError:
                print("エラー: sipsコマンドが見つかりません。macOS環境でのみ利用可能です。")
                print("手動で 'mov_folder' 内にテスト用の.movファイルを作成してください。")
            except subprocess.CalledProcessError as e:
                print(f"ダミーMOVファイルの作成中にエラーが発生しました: {e}")
                print(f"標準出力: {e.stdout.decode()}")
                print(f"標準エラー: {e.stderr.decode()}")
            finally:
                if os.path.exists(dummy_png_path):
                    os.remove(dummy_png_path)
        exit() # フォルダ作成後、ユーザーにファイルを置くように促して終了

    # mov_folder内のすべての.movファイルを取得
    mov_files = [f for f in os.listdir(mov_folder) if f.endswith(".mov")]

    if not mov_files:
        print(f"'{mov_folder}' フォルダ内に.movファイルが見つかりませんでした。")
        print("変換したい.movファイルをこのフォルダ内に置いてください。")
    else:
        for mov_file in mov_files:
            input_path = os.path.join(mov_folder, mov_file)
            # .movの拡張子を.gifに置き換え
            output_file_name = os.path.splitext(mov_file)[0] + ".gif"
            output_path = os.path.join(mov_folder, output_file_name)

            # 変換を実行
            convert_mov_to_gif(input_path, output_path, scale="320:-1", fps=15)
            print("-" * 30) # 区切り線 

