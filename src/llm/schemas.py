# -*- coding: utf-8 -*-
"""
MiniMax-H3 Omni-Modal Storyboard Schemas
基于 Pydantic V2 构建的结构化短剧分镜协议，原生适配 MiniMax-H3 语法（(S1) 说话人与 <d>[Chinese] 台词</d> 唇形对齐标签）。
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class NarrativePhase(str, Enum):
    HOOK_0_5S = "HOOK_0_5S"               # 黄金前3~5秒钩子 (生死/羞辱/反转)
    ESCALATION_5_20S = "ESCALATION_5_20S"   # 矛盾升级 (极致压迫/剥夺权利)
    TENSION_CLASH_20_40S = "TENSION_CLASH_20_40S" # 情绪对抗 (反抗第一式/语言拉扯)
    REVERSAL_40_50S = "REVERSAL_40_50S"   # 底牌翻开 (降维打击/神威爆发)
    CLIFFHANGER_50_60S = "CLIFFHANGER_50_60S" # 断章卡点 (动作定格/未吐真相/黑屏)


class CameraMovement(str, Enum):
    STATIC = "Static"
    CRASH_ZOOM_IN = "Crash_Zoom_In"
    SLOW_PUSH_IN = "Slow_Push_In"
    PULL_OUT = "Pull_Out"
    PAN_LEFT = "Pan_Left"
    PAN_RIGHT = "Pan_Right"
    DOLLY_TRACK = "Dolly_Track"
    DUTCH_ANGLE = "Dutch_Angle_Tilt"


class CharacterProfile(BaseModel):
    speaker_id: str = Field(description="MiniMax-H3 说话人标识，如 (S1), (S2)")
    name: str = Field(description="角色名字，如 林浩")
    role_type: str = Field(description="角色定位，如 Protagonist / Antagonist")
    visual_description: str = Field(description="角色外观与服装特征描述 (英文)")
    voice_description: str = Field(description="角色音色与说话风格描述 (如 cold deep commanding voice)")


class MiniMaxShotPrompt(BaseModel):
    shot_number: int = Field(description="镜头序号")
    narrative_phase: NarrativePhase = Field(description="叙事节奏阶段")
    duration_seconds: float = Field(default=5.0, description="镜头时长 (MiniMax 推荐 5~6秒)")
    speaker_id: Optional[str] = Field(default=None, description="主导说话人 ID，如 (S1)，无台词则为 None")
    dialogue_chinese: str = Field(default="", description="纯中文台词文本 (供字幕使用)")
    camera_movement: CameraMovement = Field(description="运镜方式")
    
    # MiniMax-H3 核心三大全模态字段
    integrated_multimodal_description: str = Field(
        description="包含时间顺序的画面、角色动作、运镜、唇形对齐台词 (<d>[Chinese]...</d>) 与动作拟音的完整描述"
    )
    overall_soundscape: str = Field(
        description="整个镜头持续的环境音效、房间底噪、脚步、天气声等"
    )
    non_diegetic_music: str = Field(
        default="N/A", 
        description="观众听到的背景音乐氛围描述，无配乐填 N/A"
    )


class MiniMaxEpisodeStoryboard(BaseModel):
    episode_number: int = Field(description="短剧集数")
    episode_title: str = Field(description="单集爆款标题")
    genre: str = Field(description="短剧题材，如 apocalypse / urban_son_in_law / real_fake_daughter")
    core_hook: str = Field(description="本集核心爽点与反转一句话概括")
    characters: List[CharacterProfile] = Field(description="本集出场人物列表")
    shots: List[MiniMaxShotPrompt] = Field(description="分镜列表 (单集通常包含 10~15 个镜头)")
