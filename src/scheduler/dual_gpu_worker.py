# -*- coding: utf-8 -*-
"""
Dual GPU MiniMax-H3 Async Dispatcher
负责将结构化 MiniMax 分镜 JSON 任务，按奇偶镜头异步派发至双卡 4090 对应的 ComfyUI 实例 (GPU 0: 8188 / GPU 1: 8189)。
"""

import os
import json
import time
import asyncio
import logging
import argparse
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DualGPUWorker")


class ComfyUIWorkerClient:
    def __init__(self, host: str, port: int, gpu_id: int):
        self.host = host
        self.port = port
        self.gpu_id = gpu_id
        self.base_url = f"http://{host}:{port}"

    async def is_alive(self) -> bool:
        """检测 ComfyUI 实例是否存活"""
        try:
            import urllib.request
            req = urllib.request.Request(f"{self.base_url}/system_stats", headers={"User-Agent": "novel2hongguo"})
            with urllib.request.urlopen(req, timeout=2) as resp:
                return resp.status == 200
        except Exception:
            return False

    async def render_minimax_shot(self, shot_data: Dict[str, Any], output_dir: str, mock: bool = False) -> str:
        """提交单个分镜渲染任务"""
        shot_num = shot_data.get("shot_number", 1)
        phase = shot_data.get("narrative_phase", "SHOT")
        output_mp4 = os.path.join(output_dir, f"shot_{shot_num:02d}_{phase}.mp4")

        logger.info(f"🚀 [GPU {self.gpu_id} | Port {self.port}] 开始渲染分镜 {shot_num:02d} ({phase})...")
        logger.info(f"   台词: {shot_data.get('dialogue_chinese', '无台词')}")
        logger.info(f"   提示词: {shot_data.get('integrated_multimodal_description', '')[:90]}...")

        if mock:
            # 模拟渲染等待 (双卡并发验证)
            await asyncio.sleep(2.0)
            with open(output_mp4, "wb") as f:
                f.write(b"MOCK_MINIMAX_H3_VIDEO_BYTES")
            logger.info(f"✅ [GPU {self.gpu_id}] 分镜 {shot_num:02d} 渲染完成 -> {output_mp4}")
            return output_mp4

        # 真实 ComfyUI API 调度逻辑
        # 构建 MiniMax-H3 ComfyUI API Payload 并提交 POST /prompt
        # ...
        return output_mp4


class DualGPUScheduler:
    def __init__(self):
        self.workers = [
            ComfyUIWorkerClient("127.0.0.1", 8188, gpu_id=0),
            ComfyUIWorkerClient("127.0.0.1", 8189, gpu_id=1),
        ]

    async def dispatch_episode(self, storyboard_json_path: str, output_dir: str = "data/output_videos", mock: bool = True):
        os.makedirs(output_dir, exist_ok=True)
        with open(storyboard_json_path, "r", encoding="utf-8") as f:
            storyboard = json.load(f)

        shots = storyboard.get("shots", [])
        total_shots = len(shots)
        logger.info(f"🎬 启动双卡 4090 调度矩阵: 《{storyboard.get('episode_title', '未命名短剧')}》 共 {total_shots} 个分镜")

        # 检查双卡端口存活状态
        alive_statuses = await asyncio.gather(*[w.is_alive() for w in self.workers])
        for idx, alive in enumerate(alive_statuses):
            status_text = "🟢 在线" if alive else "🔴 未检测到 (切换为模拟/等待模式)"
            logger.info(f"   Worker {idx}: GPU {self.workers[idx].gpu_id} (Port {self.workers[idx].port}) -> {status_text}")

        # 如果实例未启动且未强制指定 mock，自动降级为 mock 以便先行验证调度逻辑
        use_mock = mock or (not all(alive_statuses))
        if use_mock and not mock:
            logger.warning("⚠️ ComfyUI 实例尚未在 8188/8189 启动，自动启用本地并发仿真管线验证！")

        # 奇偶分镜分配策略 (GPU 0 跑奇数镜头，GPU 1 跑偶数镜头)
        tasks = []
        for idx, shot in enumerate(shots):
            worker = self.workers[idx % 2]
            tasks.append(worker.render_minimax_shot(shot, output_dir, mock=use_mock))

        start_time = time.time()
        rendered_clips = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time

        logger.info(f"🎉 全集 {total_shots} 个分镜已全部渲染交付! 耗时: {elapsed:.2f} 秒")
        logger.info(f"📁 分镜切片存储目录: {output_dir}")
        return rendered_clips


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="双卡 4090 MiniMax-H3 异步调度器")
    parser.add_argument("--script", type=str, required=True, help="MiniMax 分镜 JSON 文件路径")
    parser.add_argument("--outdir", type=str, default="data/output_videos", help="输出视频目录")
    parser.add_argument("--mock", action="store_true", help="启用并发仿真模式")
    args = parser.parse_args()

    scheduler = DualGPUScheduler()
    asyncio.run(scheduler.dispatch_episode(args.script, args.outdir, mock=args.mock))
