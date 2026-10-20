# -*- coding: utf-8 -*-
"""
Conflict Density Mining Engine (CIS Engine)
负责对海量小说 TXT 文件执行流式滑动窗口扫描、多维度戏剧冲突打分与高潮段落提炼。
"""

import os
import re
import json
import argparse
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

try:
    import charset_normalizer
except ImportError:
    charset_normalizer = None


@dataclass
class ConflictSnippet:
    novel_name: str
    snippet_id: str
    chapter_title: str
    start_char: int
    end_char: int
    conflict_score: float
    genre_tag: str
    dialogue_ratio: float
    text_content: str


class CorpusCleaner:
    def __init__(self):
        # 1. 冲突核心词库与加权矩阵
        self.lexicon = {
            "insult": {
                "words": [
                    "退婚", "废物", "赘婿", "下跪", "野种", "给老子滚", "掌嘴", 
                    "看门狗", "扫地出门", "蝼蚁", "磕头", "贱人", "小杂种", "断绝关系", 
                    "凭你也配", "拔掉氧气管", "死皮赖脸"
                ],
                "weight": 2.5
            },
            "slap": {
                "words": [
                    "住手", "龙王", "至尊", "首富", "战神", "一巴掌", "找死", 
                    "十万将士", "给我跪下", "轰杀", "激活系统", "殿下", "龙尊", 
                    "掌嘴三十", "黑金卡", "全城封锁", "拜见龙神"
                ],
                "weight": 3.0
            },
            "shock": {
                "words": [
                    "怎么可能", "倒吸一口凉气", "面如死灰", "双腿发软", "浑身发抖", 
                    "竟然是他", "战战兢兢", "噗通一声", "瞳孔骤缩", "惊恐万状", 
                    "眼珠子都快掉出来", "吓瘫在地"
                ],
                "weight": 2.0
            },
            "genre_apocalypse": {
                "words": [
                    "极寒", "避难所", "零元购", "囤货", "末世", "丧尸", 
                    "百亿物资", "零下六十度", "极寒风暴", "异化", "变异体"
                ],
                "weight": 2.8
            },
            "genre_real_fake": {
                "words": [
                    "亲子鉴定", "鸠占鹊巢", "真千金", "假千金", "掌上明珠", 
                    "血缘", "断绝父女关系", "滚出顾家", "偏心"
                ],
                "weight": 2.8
            },
            "genre_urban_wealth": {
                "words": [
                    "神豪", "继承万亿", "劳斯莱斯", "百亿集团", "首富之子", 
                    "不装了我是首富", "财阀"
                ],
                "weight": 2.8
            }
        }

        # 2. 垃圾广告水印过滤规则
        self.ad_patterns = [
            r"请记住本书首发域名.*?\n",
            r"最新网址：.*?\n",
            r"一秒记住【.*?】",
            r"手机用户请浏览.*?阅读",
            r"点击下一页继续阅读",
            r"喜欢.*?请大家收藏",
            r"天才一秒记住.*?\n",
            r"http[s]?://\S+"
        ]

    def read_file_safe(self, file_path: str) -> str:
        """安全读取 TXT 文件，自适应编码识别（解决 GBK / UTF-8 乱码问题）"""
        with open(file_path, "rb") as f:
            raw_bytes = f.read()

        # 尝试使用 charset-normalizer 探测编码
        encoding = "utf-8"
        if charset_normalizer:
            detection = charset_normalizer.detect(raw_bytes)
            if detection and detection.get("encoding"):
                encoding = detection["encoding"]

        # 优先使用检测到的编码，失败后按常规兜底
        for enc in [encoding, "utf-8", "gb18030", "gbk", "utf-16"]:
            try:
                return raw_bytes.decode(enc)
            except (UnicodeDecodeError, TypeError):
                continue

        # 终极容灾：忽略错误解码
        return raw_bytes.decode("utf-8", errors="ignore")

    def clean_raw_text(self, text: str) -> str:
        """剔除小说盗版水印、多余空行与网页广告"""
        for pattern in self.ad_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        # 合并多个换行与制表符
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()

    def score_text_window(self, text: str) -> Tuple[float, str, float]:
        """
        计算 1500~2000 字窗口的冲突张力得分 (Conflict Intensity Score, CIS)
        返回: (CIS得分, 检测到的题材标签, 对话比重)
        """
        total_score = 0.0
        text_len = max(len(text), 1)
        genre_scores = {
            "apocalypse": 0.0,
            "real_fake_daughter": 0.0,
            "urban_son_in_law": 0.0
        }

        # 1. 词频加权打分
        for category, config in self.lexicon.items():
            matches = sum(len(re.findall(re.escape(w), text)) for w in config["words"])
            category_score = matches * config["weight"]
            total_score += category_score

            if "apocalypse" in category:
                genre_scores["apocalypse"] += category_score
            elif "real_fake" in category:
                genre_scores["real_fake_daughter"] += category_score
            else:
                genre_scores["urban_son_in_law"] += category_score

        # 2. 标点符号张力 (叹号问号反映角色情绪失控与质问)
        exclamations = len(re.findall(r"[！!]", text))
        questions = len(re.findall(r"[？?]", text))
        punctuation_density = (exclamations * 1.5 + questions * 0.8) / (text_len / 100)
        total_score += punctuation_density

        # 3. 对话密集度加权 (短剧以角色交锋撕逼为主，排除枯燥背景描写)
        dialogue_chars = sum(len(m) for m in re.findall(r"[\"“](.*?)[\"”]", text))
        dialogue_ratio = dialogue_chars / text_len
        if dialogue_ratio > 0.45:
            total_score *= 1.3  # 对话占比高，显著加权
        elif dialogue_ratio < 0.20:
            total_score *= 0.7  # 几乎无对话，大概率为大段设定或心理描写，予以打折

        # 归一化得分 (以每千字为统一基准)
        normalized_score = (total_score / text_len) * 1000
        detected_genre = max(genre_scores, key=genre_scores.get)
        return round(normalized_score, 2), detected_genre, round(dialogue_ratio, 3)

    def extract_conflict_snippets(
        self,
        file_path: str,
        window_size: int = 1800,
        stride: int = 600,
        threshold: float = 30.0,
        top_k: int = 5
    ) -> List[ConflictSnippet]:
        """
        基于滑动窗口流式扫描并提取高冲突切片
        """
        novel_name = os.path.basename(file_path)
        raw_text = self.read_file_safe(file_path)
        cleaned_text = self.clean_raw_text(raw_text)
        text_len = len(cleaned_text)

        candidates = []
        for i in range(0, text_len, stride):
            window_end = min(i + window_size, text_len)
            chunk = cleaned_text[i:window_end]

            if len(chunk) < 600:
                continue

            score, genre, dialogue_ratio = self.score_text_window(chunk)

            if score >= threshold:
                # 寻找最近的章节标题
                context_before = cleaned_text[max(0, i - 400):i + 150]
                chapter_match = re.search(r"(第[\d一二三四五六七八九十百千]+章[^\n\r]{0,30})", context_before)
                chapter_title = chapter_match.group(1).strip() if chapter_match else "核心冲突高潮段落"

                # 自然段落边界吸附：向前寻找换行符或标点，向后寻找换行符，避免截断半句话
                adjusted_start = i
                first_nl = chunk.find("\n")
                if 0 <= first_nl < 100:
                    adjusted_start += first_nl + 1

                candidates.append({
                    "start": adjusted_start,
                    "end": window_end,
                    "score": score,
                    "genre": genre,
                    "dialogue_ratio": dialogue_ratio,
                    "chapter_title": chapter_title,
                    "content": cleaned_text[adjusted_start:window_end].strip()
                })

        # 执行非极大值抑制 (NMS)，合并过度重叠的相近高潮
        merged_snippets = self._apply_nms(candidates, overlap_ratio_thresh=0.4)

        # 整理成数据模型
        results = []
        for idx, item in enumerate(merged_snippets[:top_k], 1):
            results.append(ConflictSnippet(
                novel_name=novel_name,
                snippet_id=f"clip_{idx:02d}",
                chapter_title=item["chapter_title"],
                start_char=item["start"],
                end_char=item["end"],
                conflict_score=item["score"],
                genre_tag=item["genre"],
                dialogue_ratio=item["dialogue_ratio"],
                text_content=item["content"]
            ))

        return results

    def _apply_nms(self, candidates: List[Dict], overlap_ratio_thresh: float = 0.4) -> List[Dict]:
        """非极大值抑制算法：合并同区域内重复报警的高分窗口"""
        if not candidates:
            return []

        # 按得分从高到低排序
        candidates.sort(key=lambda x: x["score"], reverse=True)
        selected = []

        while candidates:
            best = candidates.pop(0)
            selected.append(best)

            remaining = []
            for item in candidates:
                # 计算两段文字的重合区间
                overlap_start = max(best["start"], item["start"])
                overlap_end = min(best["end"], item["end"])
                overlap_len = max(0, overlap_end - overlap_start)

                min_len = min(best["end"] - best["start"], item["end"] - item["start"])
                overlap_ratio = overlap_len / max(min_len, 1)

                # 重叠率小于阈值才保留为独立切片
                if overlap_ratio < overlap_ratio_thresh:
                    remaining.append(item)

            candidates = remaining

        return selected


def process_novel_file(input_file: str, output_dir: str = "data/processed_scripts") -> str:
    """处理单个小说文件并导出标准化 JSON 语料卡"""
    cleaner = CorpusCleaner()
    snippets = cleaner.extract_conflict_snippets(input_file)

    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    out_file = os.path.join(output_dir, f"{base_name}_snippets.json")

    output_data = {
        "source_file": os.path.basename(input_file),
        "total_extracted": len(snippets),
        "snippets": [asdict(s) for s in snippets]
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    return out_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小说冲突密度流式提取器 (CIS Engine)")
    parser.add_argument("--input", type=str, required=True, help="输入小说 TXT 路径或目录")
    parser.add_argument("--outdir", type=str, default="data/processed_scripts", help="输出 JSON 目录")
    args = parser.parse_args()

    if os.path.isfile(args.input):
        out = process_novel_file(args.input, args.outdir)
        print(f"[Success] 处理完成，结果已保存至: {out}")
    elif os.path.isdir(args.input):
        txt_files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith(".txt")]
        print(f"[Batch] 发现 {len(txt_files)} 个小说文件，开始批量挖掘...")
        for tf in txt_files:
            try:
                out = process_novel_file(tf, args.outdir)
                print(f"  -> 已提取: {os.path.basename(tf)} -> {out}")
            except Exception as e:
                print(f"  [Error] 处理失败 {tf}: {e}")
