# novel2hongguo (小说 to 红果短剧)

An automated open-source pipeline transforming raw web novel corpora into high-octane AI short dramas ("Hongguo" style) powered by **Gemini 3.8 Flash** and **Dual RTX 4090 (48GB x 2)**.

---

## 🌟 Architecture Overview

```
[Web Novel TXT Corpus (Tens of Thousands)]
                │
                ▼
      [Corpus Preprocessing]
   (Chunking, conflict & hook extraction)
                │
                ▼
    [Gemini 3.8 Flash / Antigravity]
   ├── Story Remixing & Scriptwriting
   ├── Structured Storyboard (JSON)
   └── Wan2.1 / FLUX Prompt Engineering
                │
                ▼
       [Dual GPU Scheduler]
   ┌────────────┴────────────┐
   ▼                         ▼
[GPU 0 (48GB)]            [GPU 1 (48GB)]
Wan2.1-14B (Odd Shots)   Wan2.1-14B (Even Shots)
   └────────────┬────────────┘
                ▼
   [Audio & Video Compositing]
 (TTS Voiceover + Subtitles + FFmpeg)
                │
                ▼
       [Finished Short Drama MP4]
```

---

## 🚀 Key Advantages

1. **Dual RTX 4090 48GB (96GB Total VRAM)**:
   - **Zero-offload BF16 Inference**: Full native loading of state-of-the-art 14B video models (`Wan2.1-T2V-14B`, `HunyuanVideo`).
   - **200% Throughput via Dual Workers**: GPU 0 and GPU 1 process independent video shots in parallel without PCIe cross-talk overhead.
2. **Zero-Local-Cost LLM Brain**:
   - Offloads heavy novel reading, analysis, and story remixing to **Gemini 3.8 Flash**, reserving 100% local GPU memory and compute for rendering.
3. **High-Tension "Hongguo" Narrative Logic**:
   - Automated detection and extraction of high-conflict hooks (betrayal, rebirth, system awakenings, face-slapping, survival countdowns).

---

## 📂 Project Structure

```
novel2hongguo/
├── config/
│   └── config.example.yaml          # GPU, ComfyUI, and API configurations
├── data/
│   ├── raw_novels/                  # Place raw .txt novel files here
│   ├── processed_scripts/           # Generated storyboard JSON files
│   └── output_videos/               # Final rendered short drama videos
├── src/
│   ├── corpus/                      # Novel cleaning, chunking, and hook extraction
│   ├── llm/                         # Gemini integration, script remixing & prompt generation
│   ├── scheduler/                   # Dual-GPU worker dispatch and queue management
│   ├── render/                      # ComfyUI API client for Wan2.1 / HunyuanVideo
│   └── compositor/                  # Audio synthesis, subtitle sync, and video stitching
├── workflows/                       # ComfyUI API workflow templates (JSON)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Quick Start

### 1. Prerequisites
- **OS**: Linux / Windows
- **GPUs**: 2x NVIDIA GPUs (Recommended: RTX 4090 48GB or 24GB)
- **Python**: 3.10+
- **ComfyUI**: Installed with `ComfyUI-WanVideoWrapper` or `ComfyUI-HunyuanVideoWrapper`

### 2. Installation
```bash
git clone https://github.com/huh7i5/novel2hongguo.git
cd novel2hongguo
pip install -r requirements.txt
```

### 3. Dual ComfyUI Worker Launch
Launch two independent ComfyUI instances on separate ports:
```bash
# Terminal 1 (GPU 0)
CUDA_VISIBLE_DEVICES=0 python main.py --port 8188

# Terminal 2 (GPU 1)
CUDA_VISIBLE_DEVICES=1 python main.py --port 8189
```

---

## 📄 License
MIT License.
