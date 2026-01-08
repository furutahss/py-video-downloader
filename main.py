import sys
import argparse
import yt_dlp
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# 動画保存先のディレクトリ
SAVE_PATH = Path.home() / "Downloads" / "MyDownloadedVideos"

# 動画ダウンロード
# @param  url: ダウンロードする動画のURL
# @returns  ダウンロード結果のメッセージ
def download_video(url):
    if not SAVE_PATH.exists():
        SAVE_PATH.mkdir(parents=True)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(SAVE_PATH / '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': True,
    }

    print(f"🚀 開始: {url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"✅ 成功: {url}"
    except Exception as e:
        return f"❌ 失敗: {url} (理由: {e})"

# メイン処理
# @returns  None
def main():
    parser = argparse.ArgumentParser(description="複数のURLから動画を一括ダウンロードします。")
    parser.add_argument("urls", nargs="+", help="ダウンロードしたい動画のURL（スペース区切りで複数指定可能）")
    parser.add_argument("-p", "--parallel", type=int, default=3, help="同時ダウンロード数 (デフォルト: 3)")
    
    args = parser.parse_args()

    print(f"📂 保存先: {SAVE_PATH}")
    print(f"🔄 同時実行数: {args.parallel}")
    print("-" * 40)

    # ThreadPoolExecutorによる並列実行
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        # urlsリストをmapに渡し、結果を取得
        results = list(executor.map(download_video, args.urls))

    print("-" * 40)
    print("📊 実行結果サマリー:")
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
