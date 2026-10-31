# -*- coding: utf-8 -*-
"""
MiniMax-H3 Visual Storyboard Preview Generator
将结构化剧本与分镜 JSON 转化为具备电影视听临场感的单文件交互式 HTML 剧本阅读器。
"""

import os
import json


def generate_html_preview(bible_json: str, episodes_json: str, output_html: str = "preview_drama.html"):
    with open(bible_json, "r", encoding="utf-8") as f:
        bible = json.load(f)

    with open(episodes_json, "r", encoding="utf-8") as f:
        ep_data = json.load(f)

    # 1. 被审嫌疑人 (妹妹)
    def_data = bible.get("defendant", {})
    defendant_html = f"""
    <div class="character-card defendant-card">
        <div class="char-header">
            <span class="speaker-tag" style="background: var(--accent-red); color: #fff;">{def_data['speaker_id']}</span>
            <span class="seat-badge" style="color: var(--accent-red); border-color: var(--accent-red);">🔴 被审判席 (受审嫌疑人·无投票权)</span>
            <h3>{def_data['name']}</h3>
        </div>
        <p class="role-desc"><strong>身份定位：</strong>{def_data['role']} (年龄: {def_data.get('age', '未知')})</p>
        <p class="spark-desc" style="border-left-color: var(--accent-red);"><strong>🌟 人性闪光点 / 核心动机：</strong>{def_data.get('human_spark', '暂无')}</p>
        <p class="voice-desc"><strong>MiniMax 音色特征：</strong>{def_data['voice_description']}</p>
        <p class="prompt-desc"><strong>视觉 Prompt：</strong><code>{def_data['visual_prompt']}</code></p>
    </div>
    """

    # 2. 长桌 12 位投票仲裁人
    jurors_html = ""
    for char in bible.get("jurors_12", []):
        jurors_html += f"""
        <div class="character-card">
            <div class="char-header">
                <span class="speaker-tag">{char['speaker_id']}</span>
                <span class="seat-badge">席位 #{char['seat_id']} (投票仲裁人)</span>
                <h3>{char['name']}</h3>
            </div>
            <p class="role-desc"><strong>身份定位：</strong>{char['role']} (年龄: {char.get('age', '未知')})</p>
            <p class="spark-desc"><strong>🌟 人性闪光点 / 核心动机：</strong>{char.get('human_spark', '暂无')}</p>
            <p class="voice-desc"><strong>MiniMax 音色特征：</strong>{char['voice_description']}</p>
            <p class="prompt-desc"><strong>视觉 Prompt：</strong><code>{char['visual_prompt']}</code></p>
        </div>
        """

    blueprint = bible.get("hundred_episodes_blueprint", {})
    acts_html = ""
    for act_key, act_info in blueprint.items():
        acts_html += f"""
        <div class="act-card">
            <div class="act-header">
                <span class="act-episodes">{act_info['episodes']}</span>
                <span class="act-vote">票数跃迁：{act_info['vote_progression']}</span>
            </div>
            <h4>{act_info['title']}</h4>
            <p class="act-target"><strong>攻破目标：</strong>{act_info['core_target']}</p>
            <p class="act-summary">{act_info['summary']}</p>
        </div>
        """

    episodes_html = ""
    for ep in ep_data.get("episodes", []):
        shots_html = ""
        for shot in ep.get("shots", []):
            phase_colors = {
                "HOOK_0_5S": "#ff4d4f",
                "ESCALATION_5_20S": "#fa8c16",
                "TENSION_CLASH_20_40S": "#faad14",
                "REVERSAL_40_50S": "#52c41a",
                "CLIFFHANGER_50_60S": "#722ed1"
            }
            phase_labels = {
                "HOOK_0_5S": "00-05s 黄金钩子",
                "ESCALATION_5_20S": "05-20s 矛盾施压",
                "TENSION_CLASH_20_40S": "20-40s 心理交锋",
                "REVERSAL_40_50S": "40-50s 致命底牌",
                "CLIFFHANGER_50_60S": "50-60s 绝命断章"
            }
            phase_color = phase_colors.get(shot['narrative_phase'], '#1890ff')
            phase_label = phase_labels.get(shot['narrative_phase'], shot['narrative_phase'])

            shots_html += f"""
            <div class="shot-card">
                <div class="shot-header">
                    <span class="shot-num">镜头 #{shot['shot_number']:02d}</span>
                    <span class="phase-tag" style="background-color: {phase_color};">{phase_label}</span>
                    <span class="camera-tag">🎥 {shot['camera_movement']} ({shot['duration_seconds']}s)</span>
                </div>
                <div class="dialogue-box">
                    <span class="speaker-label">{shot['speaker_id']} 对白：</span>
                    <span class="dialogue-text">“{shot['dialogue_chinese']}”</span>
                </div>
                <div class="prompt-section">
                    <div class="prompt-block">
                        <strong>🎬 MiniMax-H3 全模态时空描述：</strong>
                        <p>{shot['integrated_multimodal_description']}</p>
                    </div>
                    <div class="audio-block">
                        <p><strong>🔊 现场拟音与环境底噪：</strong>{shot['overall_soundscape']}</p>
                        <p><strong>🎵 氛围背景配乐：</strong>{shot['non_diegetic_music']}</p>
                    </div>
                </div>
            </div>
            """

        episodes_html += f"""
        <div class="episode-container">
            <h2 class="episode-title">{ep['episode_title']} <span class="badge">60秒工业短剧</span></h2>
            <div class="shots-grid">
                {shots_html}
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bible['project_title']} - 商业短剧全模态分镜工坊</title>
    <style>
        :root {{
            --bg-dark: #0b0e14;
            --panel-bg: #151921;
            --card-bg: #1c212c;
            --border-color: #2d333b;
            --accent-gold: #f59e0b;
            --accent-red: #f43f5e;
            --accent-cyan: #06b6d4;
            --text-main: #adbac7;
            --text-title: #f0f6fc;
        }}
        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", sans-serif;
            margin: 0;
            padding: 24px;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}
        .header h1 {{
            color: var(--accent-gold);
            margin: 0 0 12px 0;
            font-size: 34px;
            letter-spacing: 1px;
        }}
        .header .meta {{
            font-size: 14px;
            color: #8b949e;
        }}
        .rules-bar {{
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-top: 14px;
            flex-wrap: wrap;
        }}
        .rule-pill {{
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: var(--accent-gold);
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 12px;
        }}
        .show-bible, .blueprint-section {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
        }}
        .defendant-card {{
            border-color: var(--accent-red) !important;
            background: rgba(244, 63, 94, 0.05) !important;
            margin-bottom: 24px;
        }}
        .characters-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .character-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            flex-direction: column;
        }}
        .char-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }}
        .char-header h3 {{
            margin: 0;
            color: var(--text-title);
            font-size: 18px;
        }}
        .speaker-tag {{
            background: var(--accent-gold);
            color: #000;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }}
        .seat-badge {{
            background: #21262d;
            border: 1px solid #30363d;
            color: #58a6ff;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
        }}
        .spark-desc {{
            background: rgba(6, 182, 212, 0.08);
            border-left: 2px solid var(--accent-cyan);
            padding: 6px 10px;
            border-radius: 4px;
            margin: 8px 0;
            font-size: 13px;
            color: #c9d1d9;
        }}
        .acts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .act-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 18px;
        }}
        .act-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .act-episodes {{
            font-weight: bold;
            color: var(--accent-gold);
            font-size: 14px;
        }}
        .act-vote {{
            font-size: 12px;
            background: #30363d;
            color: #58a6ff;
            padding: 2px 8px;
            border-radius: 10px;
        }}
        .act-card h4 {{
            margin: 0 0 8px 0;
            color: var(--text-title);
            font-size: 16px;
        }}
        .act-target {{
            color: var(--accent-red);
            font-size: 13px;
            margin: 4px 0;
        }}
        .act-summary {{
            font-size: 13px;
            color: #8b949e;
            margin: 8px 0 0 0;
            line-height: 1.5;
        }}
        .episode-container {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
        }}
        .episode-title {{
            color: var(--text-title);
            margin-top: 0;
            border-left: 4px solid var(--accent-gold);
            padding-left: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .badge {{
            font-size: 12px;
            background: #238636;
            color: #fff;
            padding: 2px 8px;
            border-radius: 12px;
        }}
        .shots-grid {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-top: 16px;
        }}
        .shot-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
        }}
        .shot-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 8px;
        }}
        .shot-num {{
            font-weight: bold;
            color: var(--text-title);
        }}
        .phase-tag {{
            color: #fff;
            font-size: 12px;
            font-weight: bold;
            padding: 2px 10px;
            border-radius: 10px;
        }}
        .camera-tag {{
            font-size: 13px;
            color: #58a6ff;
            margin-left: auto;
        }}
        .dialogue-box {{
            background: rgba(245, 158, 11, 0.1);
            border-left: 3px solid var(--accent-gold);
            padding: 10px 14px;
            border-radius: 4px;
            margin-bottom: 14px;
        }}
        .speaker-label {{
            font-weight: bold;
            color: var(--accent-gold);
            margin-right: 8px;
        }}
        .dialogue-text {{
            font-size: 16px;
            color: #fff;
            font-weight: 500;
        }}
        .prompt-section {{
            font-size: 13px;
        }}
        .prompt-block {{
            background: #111418;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 8px;
        }}
        .prompt-block strong {{
            color: #7ee787;
        }}
        .prompt-block p {{
            margin: 6px 0 0 0;
            color: #adbac7;
            font-family: Consolas, monospace;
        }}
        .audio-block p {{
            margin: 4px 0;
            color: #8b949e;
        }}
        .audio-block strong {{
            color: #d2a8ff;
        }}
        code {{
            background: #111418;
            color: #58a6ff;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎬 {bible['project_title']}</h1>
        <div class="meta">
            <span><strong>题材体量：</strong>100集商业短剧 (单集60秒 / 总计100分钟)</span> | 
            <span><strong>经典源泉：</strong>{bible['adapted_from']}</span>
        </div>
        <div class="rules-bar">
            <span class="rule-pill">⚖️ 严格席位架构：长桌 12 位合法仲裁人 + 1 位受审嫌疑人 (共计 13 人)</span>
            <span class="rule-pill">🛡️ 100% 纯密室法则 (0 外部武装机械降神)</span>
            <span class="rule-pill">⏱️ 60秒五段式极速呼吸律动</span>
            <span class="rule-pill">💣 第100集恶魔白花核弹级大反转</span>
        </div>
        <p style="max-width: 860px; margin: 16px auto 0 auto; color: #8b949e; font-size: 15px;">{bible['logline']}</p>
    </div>

    <div class="blueprint-section">
        <h2 style="color: var(--text-title); margin-top: 0;">🗺️ 100集五大叙事大幕波形蓝图 (100 Episodes Blueprint)</h2>
        <div class="acts-grid">
            {acts_html}
        </div>
    </div>

    <div class="show-bible">
        <h2 style="color: var(--text-title); margin-top: 0;">🔴 被审判席·受审嫌疑人 (Defendant)</h2>
        {defendant_html}

        <h2 style="color: var(--text-title); margin-top: 32px;">⚖️ 长桌 12 位合法投票仲裁人 (The 12 Juror Moguls)</h2>
        <div class="characters-grid">
            {jurors_html}
        </div>
    </div>

    <div class="episodes-list">
        <h2 style="color: var(--text-title); margin-left: 8px;">🎬 前3集已就绪分镜 (MiniMax-H3 全模态时空协议)</h2>
        {episodes_html}
    </div>
</body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[Success] 全新 13 人严格席位交互式短剧分镜阅读器已生成: {output_html}")
    return output_html


if __name__ == "__main__":
    generate_html_preview(
        bible_json="data/processed_scripts/twelve_angry_moguls_bible.json",
        episodes_json="data/processed_scripts/twelve_angry_moguls_episodes_1_3.json",
        output_html="preview_drama.html"
    )
