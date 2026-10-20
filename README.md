# novel2hongguo (小说 to 红果短剧)
> **全自动 AI 商业短剧工业级生产管线**  
> *Powered by Gemini 3.8 Flash + CosyVoice 2 + FLUX.1 + Wan2.1-I2V + Dual RTX 4090*

---

## 📖 项目定位与设计愿景

`novel2hongguo` 是一套专为**竖屏微短剧（红果/番茄/微短剧出海 9:16 商业标准）**打造的全自动、全流程工业级视频生产流水线。

项目旨在解决当前 AI 视频生成领域的三大核心痛点：
1. **角色漂移穿帮**：告别纯文本盲抽，通过 **“FLUX.1 + PuLID + 角色专属 LoRA”** 锚定绝对一致的首帧，并结合 **Wan2.1-I2V** 与面部修复防御矩阵，实现百集长剧人脸不走样。
2. **音画节奏脱节**：彻底摒弃传统“先画后声”导致的画面塞台词滑稽感，建立 **“先声后画（Voice-First）”** 时序基准，由 **CosyVoice 2** 多角色情感配音的毫秒级时长，反向严密计算 **Wan2.1 的 $4n+1$ 物理帧数**。
3. **多卡算力浪费**：针对 **双卡 RTX 4090（48GB/24GB × 2）** 架构，舍弃高通信损耗的模型并行，设计 **双无头（Headless）独立并发调度引擎**，实现吞吐量真翻倍（单分钟出片）。

---

## 🏗️ 全流程系统架构拓扑图 (Pipeline Topology)

```mermaid
flowchart TD
    subgraph S1["【阶段 1】小说语料挖掘与爽点切片 (Corpus Engine)"]
        A[数万本海量小说 TXT 语料库] --> B[CIS 冲突密度流式计算引擎]
        B -->|正则加权 + 标点/对话密度分析| C[高冲突黄金段落 JSON 语料]
    end

    subgraph S2["【阶段 2】Gemini 3.8 Flash 剧本杂糅与分镜中枢 (LLM Brain)"]
        C --> D[Gemini 3.8 Flash 架构师]
        D -->|去皮肤化 De-skining & 跨题材重组| E[100集宏观剧本 / 60秒单集工业节奏]
        E -->|结构化受控输出| F[工业级分镜协议 JSON (Pydantic V2)]
    end

    subgraph S3["【阶段 3】CosyVoice 2 多角色情感配音 (Voice-First Engine)"]
        F --> G[角色音色资产库 (Multi-Anchor)]
        G --> H[CosyVoice 2 情感语音合成]
        H -->|自然语言 Instruct + 副语言标记| I[角色对白 WAV 音频]
        I --> J[FunASR CIF 强制对齐]
        J --> K[毫秒级时长 T_ms & 精准 SRT 字幕]
    end

    subgraph S4["【阶段 4】视觉一致性与双卡视频渲染 (Dual-GPU Farm)"]
        K -->|传递时钟基准| L[Wan2.1 4n+1 帧数反向计算器]
        F --> M[首帧锁脸 T2I: FLUX.1 + PuLID + 角色 LoRA]
        M --> N[高清分镜首帧 Keyframe]
        N & L --> O[双卡 4090 异步调度器 (Least-Loaded)]
        O -->|Port 8188| P1[GPU 0: Wan2.1-I2V-14B Worker 0]
        O -->|Port 8189| P2[GPU 1: Wan2.1-I2V-14B Worker 1]
        P1 & P2 --> Q[原生 16fps 视频片段]
        Q --> R[大动态兜底: FaceDetailer / ReActor]
        R --> S[RIFE 4.7 光流插帧至 24fps]
    end

    subgraph S5["【阶段 5】全自动智能后期混流 (Post-Production)"]
        S & I & K --> T[FFmpeg 工业级自动化矩阵]
        T -->|BGM 智能侧链闪避 Ducking| U1[多轨平衡混音]
        T -->|9:16 毛玻璃居中填充| U2[画幅自适应]
        T -->|思源黑体描边高对比硬字幕| U3[字幕烧录]
        U1 & U2 & U3 --> V[🎬 最终成片 MP4 (1080x1920 竖屏)]
    end
```

---

## 🎬 红果/番茄商业爆款短剧叙事公式

本项目严格按照字节跳动红果短剧（免费激励广告 IAA 模式）及头部微短剧平台的算法指标反推剧本逻辑：

### 1. 核心算法指标对齐
* **前 3 秒完播率（3s Retention）**：S级爆款生死线必须 $\ge 65\%$。前 3 秒严禁任何慢节奏抒情，**开局即死局、开局即反转**。
* **前 3 集完播率**：冷启动流量池决定项。第 1 集必须完成“世界观建立、受辱绝境、金手指激活、降维打脸”。
* **第 30 集卡点转化率**：全剧核心付费/广告闸口，主线矛盾在此引爆。

### 2. 60秒单集工业时间轴标准
| 时间段 | 叙事阶段 (Narrative Phase) | 视听公式与心理机制 |
| :--- | :--- | :--- |
| **00s - 05s** | **黄金钩子 (Hook)** | 破坏性拟音 + 极端特写 + 极具侮辱性台词（四大钩子：生死绝境、尊严践踏、马甲掉落、系统倒计时）。 |
| **05s - 20s** | **矛盾升级 (The Squeeze)** | 反派施加极端压迫（撕毁婚约、剥夺权利、武力威逼），将观众“憋屈感”推至顶峰。 |
| **20s - 40s** | **情绪对抗 (Tension Clash)** | 主角冷笑反击第一式，反派嘲讽拉扯，双方火药味升至爆炸临界点。 |
| **40s - 50s** | **底牌翻开 (The Reversal)** | 局势骤变！绝地金手指爆发、战神护卫破门而入，实现降维碾压反转。 |
| **50s - 60s** | **断章卡点 (Cliffhanger)** | **截断艺术**：巴掌在反派脸前 1mm 处定格、身份吐露一半、重低音 Bass Drop 瞬间黑屏，逼观众滑入下一集。 |

### 3. 第 1 集特殊性（90 ~ 120 秒高压漏斗）
浓缩网文前 5 章核心剧情：
* **第一幕 (00s-35s)**：极致之辱（豪门退婚/病房逼迁，受辱入骨）。
* **第二幕 (35s-65s)**：绝境觉醒（濒死染血玉佩/系统觉醒，金光入体）。
* **第三幕 (65s-95s)**：初显神威（单手折断恶仆手腕，全场震撼）。
* **终极断章 (95s-120s)**：全城顶豪率千名护卫破门下跪大喊“龙神降罪！”，主角抬手指向反派额头，瞬间黑屏！

---

## 🛠️ 核心模块与技术栈选型

### 模块一：语料清洗与 Gemini 3.8 Flash 剧本中枢 (`src/corpus/` & `src/llm/`)
* **小说冲突密度挖掘（CIS 引擎）**：
  基于多级滑动窗口与加权字典流式打分，计算文本冲突指数：
  $$CIS = w_1 \cdot D_{insult} + w_2 \cdot D_{slap} + w_3 \cdot D_{shock} + w_4 \cdot D_{genre} + w_5 \cdot P_{exclam} + w_6 \cdot R_{dialogue}$$
  秒级筛出 $CIS \ge 35.0$ 的高戏剧张力段落。
* **Gemini 3.8 Flash 杂糅方法论**：
  采用“去皮肤化（De-skining）”与“跨题材重组（Cross-Hybridization）”，将都市赘婿冲突嫁接至末日极寒、真假千金等题材，彻底规避版权风险，放大爽点。
* **受控 JSON 输出**：集成 Pydantic V2 严格约束输出，保证台词、角色 ID、镜头景别、运镜意图与中英双语提示词无缝传递给下游。

---

### 模块二：CosyVoice 2 多角色情感配音中枢 (`src/audio/`)
* **音色资产库（Character Voice Bible）**：
  为百集短剧建立角色声线注册表，采用 **多情绪三态锚点（Multi-Anchor）** 策略：
  * 日常态（Neutral）
  * 高张力态（Rage/Urgent）
  * 低能量态（Sorrow/Whisper）
  使用经过 Demucs 剥离纯化至 -20 LUFS 的 3~5 秒干音作为 Speaker Embedding。
* **双维度情绪控制**：
  * **自然语言 Instruct 模式**：`instruction="用咬牙切齿的声音低吼，语速加快"`。
  * **富文本副语言标记**：`[laughter]` (冷笑/狂笑)、`[quick_breath]` (急促喘息)、`<strong>...</strong>` (重音强调)。
* **时序与字幕提取**：
  * 直接读取生成 WAV 文件的物理采样帧数，获取毫秒级准确时长。
  * 搭载 **FunASR Paraformer + CIF** 执行字级硬对齐，输出零漂移的毫秒级 SRT 字幕。

---

### 模块三：视觉一致性与视频生成引擎 (`src/render/`)
* **黄金首帧锁脸组合（FLUX.1-dev + PuLID + 角色 LoRA）**：
  * **角色专属 LoRA（权重 0.68 ~ 0.72）**：锁定标志性发型、服装风格与身材体态骨架。
  * **PuLID-Flux（权重 0.78，注入步长 `start=0.0, end=0.68`）**：锁定眼角、鼻梁、唇部生物级骨骼。后 32% 步数释放给原生 FLUX 解码，消除塑料假面感，原生融合环境光影。
* **时空演化渲染（Wan2.1-I2V-14B）**：
  * 采用 `kijai/ComfyUI-WanVideoWrapper`，以 FP8 量化全权重常驻显存。
  * 叠加热点加速：**SageAttention 2**（提速 20%）+ **TeaCache (阈值 0.28)**（提速 35%~50%）。
* **极端动态三级防御兜底**：
  * **一级轻微形变**：FaceDetailer 视频批处理微修容。
  * **二级重度失真**：ReActor 节点（强制切换为 `retinaface_resnet50` 检测器 + `CodeFormer: 0.6` 适度修复），结合 RIFE 光流时序平滑彻底杜绝帧间频闪。

---

### 模块四：音画数学约束法则（$4n+1$ 规则与自适应帧率）
由于 Wan2.1 采用 3D Causal Convolution VAE 时间下采样（4x 倍率），视频帧数存在严格数学刚性约束：

$$\text{Valid\_Frames} = 4n + 1 \quad (n \in \mathbb{N}^+)$$
* 合法帧数系列：`17, 33, 49, 65, 81, 97, 113...`
* **先声后画反向推导公式**：
  若音频时长为 $T_{\text{audio}}$ 秒，Wan2.1 原生帧率为 $16\text{ fps}$，目标交付帧率为 $24\text{ fps}$：
  $$n = \max\left(1, \left\lfloor \frac{T_{\text{audio}} \times 16 - 1}{4} + 0.5 \right\rfloor\right)$$
  $$F_{\text{wan}} = 4n + 1$$
  通过 **RIFE 4.7** 插帧升频至 24fps 影视标准，毫秒级微小时差由尾端静音气口自然吸收。

---

### 模块五：双卡 4090 独立无头异步并发调度 (`src/scheduler/`)
* **架构设计**：双独立无头实例（2 Independent Workers）
  * **Worker 0**：绑定 GPU 0，监听端口 `8188`
  * **Worker 1**：绑定 GPU 1，监听端口 `8189`
  * **共享模型库**：通过 `extra_model_paths.yaml` 共享 NVMe 上的百 G 模型权重，避免硬盘冗余。
* **异步调度机制**：
  * 基于 Python `aiohttp` + `websockets` 实现 **最小负载优先（Least-Loaded）** 派发。
  * 奇偶镜头双并发异步渲染，480P 模式下双卡吞吐达 **~1 分钟产出一条 5 秒分镜**，720P 模式下单镜仅需 ~2.5 分钟。

---

### 模块六：全自动智能后期混流 (`src/compositor/`)
* **BGM 智能侧链闪避（Audio Ducking）**：
  利用 FFmpeg `sidechaincompress` 滤镜，当角色说话时，BGM 自动压低 12dB；台词停顿时，BGM 在 350ms 内平滑回升。
* **9:16 画幅自适应毛玻璃（Split-scale Blur Pad）**：
  底层画面拉伸至 720x1280 施加高斯模糊（`boxblur=25:5`）并轻度调暗，顶层保持比例居中叠加，解决不同比例构图出画穿帮。
* **影视级硬字幕烧录**：
  挂载思源黑体（Source Han Sans CN Bold），配置黑色高对比描边与轻微阴影，底部居中悬浮。

---

## 📂 完整项目结构规范

```text
novel2hongguo/
├── config/
│   ├── config.example.yaml          # 全局配置模板 (API Key、GPU 端口、分辨率)
│   └── characters_master.yaml       # 全剧核心角色资产库 (LoRA、PuLID、CosyVoice 绑定)
├── data/
│   ├── raw_novels/                  # 原始小说 TXT 语料库
│   ├── processed_scripts/           # 提取出的高冲突剧本与分镜 JSON
│   └── output_videos/               # 最终剪辑交付的短剧成片 MP4
├── src/
│   ├── corpus/                      # 语料挖掘模块
│   │   ├── __init__.py
│   │   └── cleaner.py               # CIS 冲突密度流式计算器
│   ├── llm/                         # 剧本与分镜大模型中枢
│   │   ├── __init__.py
│   │   ├── story_engine.py          # Gemini 3.8 Flash 杂糅与剧本重组
│   │   └── schemas.py               # 工业级 Pydantic V2 分镜协议模型
│   ├── audio/                       # 情感语音与时钟中枢
│   │   ├── __init__.py
│   │   ├── cosyvoice_engine.py      # CosyVoice 2 情感驱动与克隆引擎
│   │   └── subtitle_aligner.py      # FunASR CIF 强制字级对齐器
│   ├── scheduler/                   # 双卡 4090 异步调度矩阵
│   │   ├── __init__.py
│   │   ├── dual_gpu_worker.py       # WebSocket 异步状态监听与任务派发
│   │   └── temporal_calculator.py   # Wan2.1 4n+1 帧数反向推导器
│   ├── render/                      # 视觉与视频渲染客户端
│   │   ├── __init__.py
│   │   ├── flux_client.py           # FLUX.1 + PuLID + LoRA 首帧生成
│   │   └── wan_video_client.py      # Wan2.1-I2V-14B 视频渲染接入
│   └── compositor/                  # 智能音视频后期合成
│       ├── __init__.py
│       └── video_stitcher.py        # FFmpeg 侧链闪避、毛玻璃画幅与字幕烧录
├── workflows/                       # ComfyUI API 生产工作流 JSON
│   ├── flux_pulid_lora_t2i.json     # 首帧锁脸确定性出图工作流
│   └── wan2.1_i2v_fp8_teacache.json # Wan2.1-I2V 极速推理工作流
├── scripts/                         # 运维与启动脚本
│   ├── launch_dual_comfyui.sh       # Linux 双实例无头启动脚本
│   └── launch_dual_comfyui.ps1      # Windows PowerShell 双卡启动脚本
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚡ 工业落地避坑指南 (Engineering Pitfalls)

1. **PyTorch 显存碎片化崩溃**：
   * *现象*：连续渲染多个视频后突然抛出 `CUDA out of memory`。
   * *对策*：启动脚本中必须强制注入：`export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`。
2. **多角色同框“面部污染 (Face Bleed)”**：
   * *现象*：男女主角同框对话分镜中，女主角脸上出现男主角五官。
   * *对策*：多人镜头**严禁使用全局 PuLID**！首帧生成阶段必须采用 `Regional Conditioning` 或 `BBox Masking` 分区遮罩，按区域独立注入对应人物特征。
3. **音频数字削波爆音**：
   * *现象*：角色配音在怒吼、大喊台词时产生破音。
   * *对策*：在 FFmpeg 混音总线上挂载高精度限幅器：`alimiter=limit=-1dB:attack=5:release=50`。
4. **长台词注意力衰减**：
   * *现象*：CosyVoice 遇到超过 35 字的长台词时尾端容易吞字或突然加速。
   * *对策*：单次合成台词严格控制在 25~30 字内；标点断句处自动插入 `[quick_breath]` 或 150~250ms 静音气口。

---

## 🚀 快速上手与运行流程

### 1. 启动双卡 ComfyUI 无头实例
```bash
# Windows PowerShell
.\scripts\launch_dual_comfyui.ps1

# Linux
bash ./scripts/launch_dual_comfyui.sh
```

### 2. 执行小说提炼与全自动短剧合成
```bash
# 激活环境
pip install -r requirements.txt

# 运行小说语料挖掘与剧本生成
python -m src.corpus.cleaner --input data/raw_novels/sample.txt
python -m src.llm.story_engine --genre apocalypse

# 启动全自动音画双卡合成流水线
python -m src.scheduler.dual_gpu_worker
```

---

## 📄 开源许可
MIT License.
