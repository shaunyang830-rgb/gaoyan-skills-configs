# GaoyanEngine Constants — 高岩科技PPT设计系统常量
# Based on: 20260403高岩PPT美化培训讲义分享.pdf + 高岩报告template--All-2026.pptx

from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

# ── Slide Dimensions ──
SW = Inches(13.333)   # Slide width (16:9)
SH = Inches(7.5)      # Slide height
LM = Inches(0.54)     # Left margin (content start)
RM = Inches(0.54)     # Right margin
CW = Inches(12.25)    # Content width (LM to right edge minus margin)
TAG_LM = Inches(0.08) # Tag label left margin

# ── Vertical Zones ──
TITLE_TOP = Inches(0)
TITLE_H = Inches(0.90)
SUBCON_TOP = Inches(0.98)       # Sub-conclusion bar top
SUBCON_H = Inches(0.86)         # Sub-conclusion bar height
CONTENT_TOP = Inches(2.00)      # Content area start (below sub-conclusion)
SOURCE_Y = Inches(7.11)         # Source line vertical position
SOURCE_H = Inches(0.40)         # Source line height

# ── Tag Label (左上角绿色标签条) ──
TAG_LEFT = Inches(0.08)
TAG_TOP = Inches(0)
TAG_W = Inches(0.46)
TAG_H = Inches(0.90)

# ── Sub-conclusion Bar ──
SUBCON_LEFT = Inches(0.60)
SUBCON_W = Inches(12.15)
SUBCON_TEXT_LEFT = Inches(0.75)
SUBCON_TEXT_W = Inches(12.20)
SUBCON_TEXT_H = Inches(0.81)
VLINE_X = Inches(0.60)          # Vertical accent line x
VLINE_TOP = Inches(1.08)        # Vertical accent line top
VLINE_H = Inches(0.71)          # Vertical accent line height
ICON_LEFT = Inches(0.45)        # Green circle icon left
ICON_TOP = Inches(1.29)         # Green circle icon top
ICON_SIZE = Inches(0.28)        # Green circle icon diameter

# ── Left Gradient Bar (optional) ──
GRAD_BAR_LEFT = Inches(-0.78)
GRAD_BAR_TOP = Inches(1.22)
GRAD_BAR_W = Inches(0.53)
GRAD_BAR_H = Inches(5.33)

# ── Source & Page Number ──
SOURCE_LEFT = Inches(0.51)
SOURCE_W = Inches(7.98)
BRAND_LEFT = Inches(11.23)      # "高岩 GAOYAN" brand text
BRAND_W = Inches(1.09)
PAGE_NUM_LEFT = Inches(9.78)
PAGE_NUM_W = Inches(3.00)

# ── Brand Colors ──
# Primary
GAOYAN_BLUE = RGBColor(0x06, 0x1F, 0x32)     # #061F32 - 高岩蓝（深蓝）
GAOYAN_DARK = RGBColor(0x05, 0x1C, 0x2C)     # #051C2C - 深蓝变体
GAOYAN_GREEN = RGBColor(0x01, 0xEF, 0xC1)    # #01EFC1 - 高岩绿
GAOYAN_GREEN2 = RGBColor(0x00, 0xEF, 0xC0)   # #00EFC0 - 高岩绿变体（标签条）
GAOYAN_GRAY = RGBColor(0x3E, 0x39, 0x39)     # #3E3939 - 高岩灰（正文）
CHEF_YELLOW = RGBColor(0xFC, 0xD2, 0x00)     # #FCD200 - 厨人黄

# Neutral
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
DARK_GRAY = RGBColor(0x0E, 0x0E, 0x0E)       # #0E0E0E - 深色文字
MED_GRAY = RGBColor(0x66, 0x66, 0x66)
LINE_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
BG_GRAY = RGBColor(0xF2, 0xF2, 0xF2)         # #F2F2F2 - 背景灰
LIGHT_BLUE_BG = RGBColor(0xDA, 0xF1, 0xFC)   # #DAF1FC - 浅蓝卡片底色

# Data Visualization Palette (蓝色渐进系列)
DATA_BLUE_1 = RGBColor(0x00, 0x20, 0x60)     # #002060 - 深蓝（header条）
DATA_BLUE_2 = RGBColor(0x01, 0x2D, 0x88)     # #012D88
DATA_BLUE_3 = RGBColor(0x11, 0x33, 0x61)     # #113361
DATA_BLUE_4 = RGBColor(0x21, 0x56, 0xC7)     # #2156C7 - 中蓝（重要数据）
DATA_BLUE_5 = RGBColor(0x22, 0x76, 0xBC)     # #2276BC
DATA_BLUE_6 = RGBColor(0x05, 0xAE, 0xE5)     # #05AEE5 - 浅蓝
DATA_BLUE_7 = RGBColor(0x20, 0xA6, 0xC7)     # #20A6C7 - 青蓝
DATA_BLUE_8 = RGBColor(0x64, 0xD5, 0xFF)     # #64D5FF - 亮蓝

# Accent colors for multi-item differentiation
ACCENT_GREEN = RGBColor(0x09, 0xA4, 0x77)    # #09A477 - 正面/增长
ACCENT_YELLOW = RGBColor(0xE9, 0xC6, 0x00)   # #E9C600 - 警示
ACCENT_ORANGE = RGBColor(0xED, 0x7E, 0x2C)   # #ED7E2C - 中等风险
ACCENT_RED = RGBColor(0xFB, 0x44, 0x0F)      # #FB440F - 负面/高风险
POSITIVE_GREEN = RGBColor(0x00, 0xB0, 0x50)  # #00B050 - 正增长

# Chart series default palette (ordered for stacked/grouped charts)
CHART_PALETTE = [
    DATA_BLUE_1,   # #002060
    DATA_BLUE_3,   # #113361
    DATA_BLUE_4,   # #2156C7
    DATA_BLUE_5,   # #2276BC
    DATA_BLUE_6,   # #05AEE5
    GAOYAN_GREEN,  # #01EFC1
    ACCENT_RED,    # #FB440F
    ACCENT_YELLOW, # #E9C600
]

# ── Typography ──
FONT_CN = 'Microsoft YaHei'       # 微软雅黑 - 中文主字体
FONT_CN_LIGHT = 'Microsoft YaHei Light'  # 微软雅黑 Light
FONT_EN = 'Century Gothic'        # 英文主字体
FONT_NUM = 'Century Gothic'       # 数字字体
FONT_ALT_NUM = 'Arial'            # 备用数字字体
FONT_SOURCE = 'Arial'             # Source行字体

# Font sizes (strict hierarchy)
COVER_TITLE_SIZE = Pt(44)         # 封面主标题
COVER_SUB_SIZE = Pt(32)           # 封面英文副标题
SECTION_TITLE_SIZE = Pt(40)       # 章节页标题
ACTION_TITLE_SIZE = Pt(24)        # 详情页标题（结论句）
SUB_HEADER_SIZE = Pt(20)          # 子标题
CATEGORY_SIZE = Pt(18)            # 分类标题
EMPHASIS_SIZE = Pt(16)            # 强调文本
BODY_SIZE = Pt(14)                # ⭐正文主体（最常用）
BODY_SMALL_SIZE = Pt(12)          # 次要正文/图表标签
CAPTION_SIZE = Pt(11)             # 辅助说明
TAG_SIZE = Pt(10)                 # 标签条文字/小注
SOURCE_SIZE = Pt(9)               # Source行
FOOTNOTE_SIZE = Pt(8)             # 数据来源/脚注

# ── Shape Constants ──
CORNER_RADIUS = Inches(0.15)      # 圆角矩形默认圆角半径（高岩风格：圆角）
CARD_CORNER_RADIUS = Inches(0.10) # 小卡片圆角

# ── Gaoyan-specific layout constants ──
INSIGHT_PANEL_VLINE_X = Inches(8.73)   # 右侧洞察面板竖线位置
INSIGHT_PANEL_LEFT = Inches(8.86)      # 右侧洞察面板左边
INSIGHT_PANEL_W = Inches(3.87)         # 右侧洞察面板宽度
