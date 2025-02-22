import os
import json
import shutil
import subprocess
from PIL import Image
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def set_metadata(image_path, metadata_path):
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    # ファイルの拡張子を取得
    _, ext = os.path.splitext(image_path)

    # 実際のファイル形式を確認
    try:
        with Image.open(image_path) as img:
            actual_ext = '.' + ('jpeg' if img.format.lower() == 'jpg' else img.format.lower())
    except IOError:
        actual_ext = None

    if actual_ext and ext.lower() != actual_ext.lower():
        new_image_path = image_path.rsplit('.', 1)[0] + actual_ext
        os.rename(image_path, new_image_path)
        image_path = new_image_path

    # 撮影日時のフォーマット統一
    try:
        photo_taken_time_dt = datetime.strptime(metadata["photoTakenTime"]["formatted"], '%Y/%m/%d %H:%M:%S %Z')
        photo_taken_time_str = photo_taken_time_dt.strftime('%Y:%m:%d %H:%S:%M')
    except ValueError:
        print(f"Error parsing date: {metadata['photoTakenTime']['formatted']}")
        return

    exiftool_cmd = [
        'exiftool',
        f'-Title={metadata.get("title", "")}',
        f'-Description={metadata.get("description", "")}',
        f'-ImageDescription={metadata.get("description", "")}',
        f'-CreateDate={photo_taken_time_str}',
        f'-DateTimeOriginal={photo_taken_time_str}',
        '-overwrite_original',
        image_path
    ]

    if ext.lower() in ['.jpg', '.jpeg']:
        exiftool_cmd.extend([
            f'-GPSLatitude={metadata["geoData"]["latitude"]}',
            f'-GPSLongitude={metadata["geoData"]["longitude"]}',
            f'-GPSAltitude={metadata["geoData"]["altitude"]}'
        ])

    try:
        # ExifToolコマンドを実行
        subprocess.run(exiftool_cmd, check=True, stderr=subprocess.PIPE, text=True)
        print(f"Metadata set for {image_path}")
        # ファイルの作成日時と最終更新日時を更新
        timestamp = photo_taken_time_dt.timestamp()
        os.utime(image_path, (timestamp, timestamp))
        print(f"Timestamps updated for {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error setting metadata for {image_path}: {e.stderr}")
        with open('data/out/failed.txt', 'a') as f:
            f.write(f"{image_path}\n")

def process_file(image_path, metadata_path, output_dir):
    dest_path = os.path.join(output_dir, os.path.basename(image_path))

    # 出力先ファイルが既に存在する場合、エラーを発生させる
    if os.path.exists(dest_path):
        raise FileExistsError(f"File already exists: {dest_path}")

    shutil.copy(image_path, dest_path)
    set_metadata(dest_path, metadata_path)

def process_directory(input_dir, output_dir, max_workers=50):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.supplemental-metadata.json'):
                    continue
                image_path = os.path.join(root, file)
                metadata_path = image_path + '.supplemental-metadata.json'
                if os.path.exists(metadata_path):
                    futures.append(executor.submit(process_file, image_path, metadata_path, output_dir))
        
        # 完了するのを待つ
        for future in futures:
            try:
                future.result()  # ここで例外が発生すると処理が中断される
            except FileExistsError as e:
                print(f"Error: {e}")
                return  # 処理を中断

if __name__ == "__main__":
    input_dir = 'data/Takeout/Google フォト'
    output_dir = 'data/out'
    os.makedirs(output_dir, exist_ok=True)
    process_directory(input_dir, output_dir)
