# -*- coding: utf-8 -*-
"""
Hugging Face 开源小说语料流式下载器
从 wdndev/webnovel-chinese 数据集高速拉取指定数量的完本网络小说并存入 data/raw_novels/
"""

import os
import json
import argparse
import requests
from collections import defaultdict


def download_sample_novels(count: int = 5, output_dir: str = "data/raw_novels", mirror_url: str = "https://hf-mirror.com"):
    os.makedirs(output_dir, exist_ok=True)
    target_url = f"{mirror_url}/datasets/wdndev/webnovel-chinese/resolve/main/data/webnovel_0.jsonl"
    
    print(f"[*] 正在从开源镜像流式拉取网络小说数据: {target_url}")
    print(f"[*] 目标下载小说本数: {count}")
    
    novels_dict = defaultdict(list)
    completed_novels = set()
    current_title = None

    headers = {"User-Agent": "novel2hongguo-downloader/1.0"}
    with requests.get(target_url, stream=True, headers=headers, timeout=20) as resp:
        resp.raise_for_status()
        
        for line in resp.iter_lines():
            if not line:
                continue
                
            try:
                record = json.loads(line.decode("utf-8"))
            except Exception:
                continue
                
            title = record.get("title", "").strip()
            chapter = record.get("chapter", "").strip()
            text = record.get("text", "").strip()
            
            if not title or not text:
                continue

            # 检测到换书且已有书收集完毕
            if current_title and title != current_title:
                completed_novels.add(current_title)
                print(f"  [+] 成功抓取全本: 《{current_title}》 (共 {len(novels_dict[current_title])} 章)")
                
                # 保存为 TXT 文件
                safe_title = "".join(c for c in current_title if c.isalnum() or c in ("_", "-", " ")).strip()
                if not safe_title:
                    safe_title = f"novel_{len(completed_novels)}"
                txt_path = os.path.join(output_dir, f"{safe_title}.txt")
                
                with open(txt_path, "w", encoding="utf-8") as f:
                    for ch_name, ch_text in novels_dict[current_title]:
                        f.write(f"\n\n{ch_name}\n\n")
                        f.write(ch_text)
                print(f"      -> 已保存至: {txt_path}")

                if len(completed_novels) >= count:
                    break

            current_title = title
            novels_dict[title].append((chapter, text))

    print(f"[Done] 批量下载完成，共计获取 {len(completed_novels)} 本完整小说，存入 {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hugging Face 中文网络小说批量下载器")
    parser.add_argument("--count", type=int, default=3, help="需要下载的小说本数")
    parser.add_argument("--outdir", type=str, default="data/raw_novels", help="保存目录")
    args = parser.parse_args()

    download_sample_novels(count=args.count, output_dir=args.outdir)
