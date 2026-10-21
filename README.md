# novel2hongguo (小说 to 红果短剧)
> **全自动 AI 商业短剧极简全模态生产管线**  
> *Powered by Gemini 3.8 Flash + MiniMax-H3 (33B Omni-Modal) + Dual RTX 4090 (48GB x 2)*

---

## 🌟 核心理念：全模态端到端（All-in-MiniMax）

在过去，AI 视频短剧通常依赖繁重的 **“6 层拼装管线”**：
> `FLUX 生图 -> 视频模型生静音画面 -> TTS 跑配音 -> ASR 跑时间戳 -> 外部模型做唇形同步 -> FFmpeg 混流音画`

这种架构不仅工程复杂度极高、排队延迟严重，而且角色容易出现“下巴脱臼”、“嘴形对不上”、“打巴掌音效滞后”等严重违和感。

**`novel2hongguo` 采用最新的 MiniMax-H3 全模态（Omni-Modal）端到端架构：**
* **单次前向（One-Pass）全模态生成**：利用 MiniMax-H3 的 `H3-Omni-Transformer` 同时预测视频与音频 Latent；
* **天然唇形对齐（Native Lip-Sync）**：模型在生成说话动作的同时直接合成嘴型与 32kHz 高清立体声音频；
* **物理拟音毫秒级卡点（Synchronized SFX）**：巴掌击打、玻璃碎裂、关门巨响与画面动作在同一时间步原生对齐；
* **双卡 4090 48G 原生常驻**：单卡 48G 显存完美承载 FP8 量化版 MiniMax-H3（约 35GB VRAM），双卡独立并发，实现批量短剧分钟级极速出片。

---

## 🏗️ 极简端到端生产拓扑 (Streamlined Pipeline Topology)

```mermaid
flowchart TD
    subgraph S1["【阶段 1】语料冲突挖掘 (Corpus Engine)"]
        A[数万本小说 TXT 语料库] --> B[CIS 冲突密度流式计算引擎]
        B -->|词频加权 + 对话/标点密度分析| C[黄金冲突段落 JSON 语料]
    end

    subgraph S2["【阶段 2】Gemini 3.8 Flash 剧本与全模态分镜中枢"]
        C --> D[Gemini 3.8 Flash 架构师]
        D -->|去皮肤化 De-skining & 跨题材重组| E[60秒红果短剧剧本 / 黄金3秒钩子 / 结尾断章]
        E -->|生成 MiniMax-H3 专用原生提示词协议| F[MiniMax 分镜表 JSON]
    end

    subgraph S3["【阶段 3】双卡 4090 MiniMax-H3 全模态渲染农场"]
        F --> G[双卡异步调度器 (Least-Loaded)]
        G -->|Port 8188| H1["GPU 0 (48GB): MiniMax-H3 33B (Shot 1, 3, 5...)"]
        G -->|Port 8189| H2["GPU 1 (48GB): MiniMax-H3 33B (Shot 2, 4, 6...)"]
        H1 & H2 -->|直接输出自带唇形、台词、音效与BGM| I[分镜完整 MP4 切片]
    end

    subgraph S4["【阶段 4】极简成片拼接 (Post-Production)"]
        I --> J[FFmpeg 流式 Concat 拼接]
        J --> K[🎬 最终商业短剧成片 MP4 (9:16 竖屏)]
    end
```

---

## 📜 MiniMax-H3 工业级 Prompt 语法协议

MiniMax-H3 支持在提示词中直接嵌入角色对话、情绪、运镜与拟音，由 Gemini 3.8 Flash 自动生成符合规范的结构化提示词：

```text
integrated_multimodal_description: [Shot 1] A dramatic close-up shot of (S1) standing in fury, his eyes burning with cold rage. (S1) slams his fist onto the wooden table with a loud crack, leans forward towards the camera, and says with intense anger, <d>[Chinese] 跪下！把地上的退婚书舔干净！</d>
overall_soundscape: Banquet room tone, heavy fist slamming on wood sound effect, crystal glass vibrating, distant gasps of shocked crowd.
non_diegetic_music: Tense cinematic suspense build-up with subtle sub-bass thud.
```

### 核心语法规则：
1. **说话人标识（Speaker ID）**：每个说话角色分配 `(S1)`, `(S2)` 等固定标识。
2. **台词与唇形对齐（`<d>` 标签）**：格式必须为 `<d>[Chinese] 台词内容</d>`，模型会自动对齐角色的嘴型开合与音色。
3. **动作内拟音（In-shot SFX）**：将击打、碎裂、撞门等动作音效直接写在动作发生的位置。
4. **环境背景音（`overall_soundscape`）**：定义整段视频的房间底噪、天气、脚步等环境音效。
5. **画外配乐（`non_diegetic_music`）**：定义观众听到的背景氛围音乐，若不需要可填 `N/A`。

---

## 🎬 红果/番茄商业爆款短剧叙事公式

本项目严格按照红果/番茄微短剧的算法推荐机制反推剧本：
* **黄金前 3 秒钩子（Hook）**：开局即死局、开局即反转（生死绝境、尊严践踏、战神/神豪马甲掉落、系统倒计时）。
* **60 秒单集时间轴**：
  * `00s - 05s`：黄金钩子（破坏性音效 + 极端面部特写 + 极具羞辱性台词）；
  * `05s - 20s`：矛盾升级（反派极端压迫，观众憋屈感推向峰值）；
  * `20s - 40s`：情绪对抗（主角冷笑反击第一式，火药味拉满）；
  * `40s - 50s`：底牌翻开（神威爆发、顶豪下跪，降维打击反转）；
  * `50s - 60s`：**断章卡点（Cliffhanger）**——巴掌挥到脸前 1mm 处卡死、真相吐露一半，伴随重低音瞬间黑屏，强逼滑入下一集。

---

## 🛠️ 双卡 4090 48G 工作站部署说明

### 1. 显存与运行规格
* **模型大小**：MiniMax-H3（33B 参数）
* **显存占用**：FP8 量化模式下常驻显存约为 **32GB ~ 35GB**。你的单卡 48G 显存富余充足，支持完全零 CPU 交换的满血推理。
* **单镜耗时**：单卡渲染一个 5 秒自带音效的镜头约需 **2.5 ~ 3.5 分钟**。
* **双卡并发吞吐**：双卡异步交替生产，平均 **1.5 分钟产出一个高质量镜头**，一部 15 个镜头的 1 分钟短剧全自动成片仅需约 **20 分钟**。

### 2. 双实例无头启动命令
```bash
# Terminal 1 (GPU 0 - 监听 8188 端口)
CUDA_VISIBLE_DEVICES=0 python main.py --port 8188 --listen 0.0.0.0 --disable-auto-launch

# Terminal 2 (GPU 1 - 监听 8189 端口)
CUDA_VISIBLE_DEVICES=1 python main.py --port 8189 --listen 0.0.0.0 --disable-auto-launch
```

---

## 📂 项目模块结构

```text
novel2hongguo/
├── config/
│   └── config.example.yaml          # 全局配置模板 (GPU 端口、Gemini API Key、分辨率)
├── data/
│   ├── raw_novels/                  # 原始小说 TXT 语料库
│   ├── processed_scripts/           # CIS 提炼高潮与 Gemini 分镜 JSON
│   └── output_videos/               # 最终剪辑交付的短剧成片 MP4
├── src/
│   ├── corpus/                      # 语料挖掘模块
│   │   ├── __init__.py
│   │   └── cleaner.py               # CIS 冲突密度流式计算器
│   ├── llm/                         # 剧本与 MiniMax 原生分镜中枢
│   │   ├── __init__.py
│   │   ├── story_engine.py          # Gemini 3.8 Flash 杂糅与 MiniMax-H3 Prompt 生成器
│   │   └── schemas.py               # MiniMax-H3 Pydantic V2 分镜协议数据模型
│   ├── scheduler/                   # 双卡 4090 异步调度矩阵
│   │   ├── __init__.py
│   │   └── dual_gpu_worker.py       # WebSocket 异步状态监听与任务派发 (8188/8189)
│   └── compositor/                  # 极简音视频后期拼接
│       ├── __init__.py
│       └── video_stitcher.py        # FFmpeg 流式 Concat 拼接
├── scripts/
│   └── fetch_hf_novels.py           # Hugging Face 小说高速流式下载器
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 极简两步生产流程

```bash
# 1. 批量提取小说高潮切片
python -m src.corpus.cleaner --input data/raw_novels

# 2. 调度 Gemini 3.8 Flash 杂糅并生成 MiniMax-H3 结构化分镜
python -m src.llm.story_engine --input data/processed_scripts/demo_urban_warrior_snippets.json --genre apocalypse

# 3. 驱动双卡 4090 异步渲染成片
python -m src.scheduler.dual_gpu_worker --script data/processed_scripts/episode_01_minimax.json
```

---

## 📄 开源许可
MIT License.
