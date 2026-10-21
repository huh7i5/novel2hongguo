# -*- coding: utf-8 -*-
"""
MiniMax-H3 Streamlined Video Stitcher
负责将双卡 4090 渲染生成的自带音画的分镜 MP4 切片，通过 FFmpeg 流式无损拼接为 60 秒完整短剧。
"""

import os
import glob
import subprocess
import argparse


def stitch_episode_clips(input_dir: str = "data/output_videos", output_path: str = "data/output_videos/final_episode_01.mp4") -> str:
    """使用 FFmpeg concat 协议一键拼接所有分镜切片"""
    clips = sorted(glob.glob(os.path.join(input_dir, "shot_*.mp4")))
    if not clips:
        raise FileNotFoundError(f"目录 {input_dir} 下未找到任何 shot_*.mp4 分镜视频！")

    print(f"[*] 发现 {len(clips)} 个分镜切片，准备拼接...")

    # 生成 FFmpeg concat 列表清单
    list_file = os.path.join(input_dir, "concat_manifest.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for clip in clips:
            # 路径规范化 (绝对路径，反斜杠替换为正斜杠)
            abs_path = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")

    # 执行 FFmpeg 无损流式拼接
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[Success] 完整短剧成片已合成导出: {output_path}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"[Note] 本地若未安装系统级 ffmpeg，可安装或通过系统包管理器调用: {e}")
        # 输出清单文件以备手动或外部调用
        print(f"[Info] 拼接清单已生成于: {list_file}")

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MiniMax-H3 短剧快速流式拼接器")
    parser.add_argument("--indir", type=str, default="data/output_videos", help="分镜切片目录")
    parser.add_argument("--output", type=str, default="data/output_videos/final_episode_01.mp4", help="合成成片输出路径")
    args = parser.parse_args()

    stitch_episode_clips(args.indir, args.output)
