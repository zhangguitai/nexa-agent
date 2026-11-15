from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT = OUTPUT_DIR / "NEXA-Agent-Workspace-技术文档.pdf"

FONT_REGULAR = Path(r"C:\Windows\Fonts\Deng.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\Dengb.ttf")
FONT_LIGHT = Path(r"C:\Windows\Fonts\Dengl.ttf")

PDF_FONT = "Deng"
PDF_FONT_BOLD = "DengBold"
PDF_FONT_LIGHT = "DengLight"

pdfmetrics.registerFont(TTFont(PDF_FONT, str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont(PDF_FONT_BOLD, str(FONT_BOLD)))
pdfmetrics.registerFont(TTFont(PDF_FONT_LIGHT, str(FONT_LIGHT)))

INK = colors.HexColor("#17211F")
INK_SOFT = colors.HexColor("#34413E")
MUTED = colors.HexColor("#68746F")
MUTED_LIGHT = colors.HexColor("#8A948F")
BORDER = colors.HexColor("#DFE5DF")
SURFACE = colors.HexColor("#FFFFFF")
SURFACE_SOFT = colors.HexColor("#F5F7F3")
MINT = colors.HexColor("#0D9075")
MINT_DARK = colors.HexColor("#08755F")
MINT_SOFT = colors.HexColor("#E3F5EE")
CORAL = colors.HexColor("#DF7546")
CORAL_SOFT = colors.HexColor("#FBE9E0")
BLUE = colors.HexColor("#3F78C5")
BLUE_SOFT = colors.HexColor("#E9F0FA")
VIOLET = colors.HexColor("#7163C7")
VIOLET_SOFT = colors.HexColor("#EFEDFA")
AMBER = colors.HexColor("#B57A21")
AMBER_SOFT = colors.HexColor("#FBF1DE")

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 44
RIGHT = 44
TOP = 56
BOTTOM = 42
CONTENT_WIDTH = PAGE_WIDTH - LEFT - RIGHT

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CNBody",
        fontName=PDF_FONT,
        fontSize=9.4,
        leading=16.2,
        textColor=INK_SOFT,
        wordWrap="CJK",
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="CNSmall",
        parent=styles["CNBody"],
        fontSize=8,
        leading=13,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="CNTiny",
        parent=styles["CNBody"],
        fontSize=6.8,
        leading=10.5,
        textColor=MUTED_LIGHT,
    )
)
styles.add(
    ParagraphStyle(
        name="CNH1",
        fontName=PDF_FONT_BOLD,
        fontSize=23,
        leading=30,
        textColor=INK,
        wordWrap="CJK",
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="CNH2",
        fontName=PDF_FONT_BOLD,
        fontSize=13,
        leading=19,
        textColor=INK,
        wordWrap="CJK",
        spaceBefore=5,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="CNH3",
        fontName=PDF_FONT_BOLD,
        fontSize=10.2,
        leading=15,
        textColor=INK,
        wordWrap="CJK",
        spaceBefore=3,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CNBullet",
        parent=styles["CNBody"],
        leftIndent=12,
        firstLineIndent=-8,
        bulletIndent=2,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CNKicker",
        fontName=PDF_FONT_BOLD,
        fontSize=7,
        leading=10,
        textColor=MINT,
        wordWrap="CJK",
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CNCaption",
        fontName=PDF_FONT,
        fontSize=7.2,
        leading=11,
        textColor=MUTED_LIGHT,
        alignment=TA_CENTER,
        wordWrap="CJK",
        spaceBefore=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CNTableHead",
        fontName=PDF_FONT_BOLD,
        fontSize=7.5,
        leading=11,
        textColor=INK,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="CNTableCell",
        fontName=PDF_FONT,
        fontSize=7.4,
        leading=11.4,
        textColor=INK_SOFT,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="CNCode",
        fontName="Courier",
        fontSize=7,
        leading=11,
        textColor=colors.HexColor("#EAF7F2"),
        backColor=colors.HexColor("#14221E"),
        borderPadding=9,
        wordWrap="CJK",
    )
)


def paragraph(text: str, style: str = "CNBody") -> Paragraph:
    return Paragraph(text, styles[style])


def bullet(text: str) -> Paragraph:
    return Paragraph(f"• {text}", styles["CNBullet"])


def numbered(index: int, text: str) -> Paragraph:
    return Paragraph(f"<b>{index:02d}</b>&nbsp;&nbsp;{text}", styles["CNBullet"])


class HRule(Flowable):
    def __init__(self, color=BORDER, thickness=0.7, space_before=3, space_after=8):
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.space_before = space_before
        self.space_after = space_after

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        self.height = self.space_before + self.thickness + self.space_after
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self.space_after + self.thickness / 2
        self.canv.line(0, y, self.width, y)


class SectionRule(Flowable):
    def __init__(self):
        super().__init__()
        self.width = CONTENT_WIDTH
        self.height = 12

    def draw(self):
        self.canv.setFillColor(MINT)
        self.canv.roundRect(0, 3, 28, 3, 1.5, stroke=0, fill=1)
        self.canv.setFillColor(colors.HexColor("#D9DFD9"))
        self.canv.rect(36, 4, CONTENT_WIDTH - 36, 1, stroke=0, fill=1)


def section_header(number: str, title: str, subtitle: str = "") -> list[Flowable]:
    blocks: list[Flowable] = [
        Spacer(1, 2),
        paragraph(f"SECTION {number}", "CNKicker"),
        paragraph(title, "CNH1"),
    ]
    if subtitle:
        blocks.append(paragraph(subtitle, "CNSmall"))
    blocks.extend([SectionRule(), Spacer(1, 10)])
    return blocks


def info_callout(title: str, body: str, tone: str = "mint") -> Table:
    palette = {
        "mint": (MINT_SOFT, MINT_DARK),
        "coral": (CORAL_SOFT, CORAL),
        "blue": (BLUE_SOFT, BLUE),
        "violet": (VIOLET_SOFT, VIOLET),
        "amber": (AMBER_SOFT, AMBER),
    }
    background, accent = palette[tone]
    title_paragraph = Paragraph(
        f"<font color='{accent.hexval()}'><b>{title}</b></font>",
        styles["CNTableCell"],
    )
    body_paragraph = Paragraph(body, styles["CNSmall"])
    table = Table([[title_paragraph], [body_paragraph]], colWidths=[CONTENT_WIDTH])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.Color(accent.red, accent.green, accent.blue, alpha=0.22)),
                ("LINEBEFORE", (0, 0), (0, -1), 2.5, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
                ("TOPPADDING", (0, 1), (-1, 1), 2),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
            ]
        )
    )
    return table


def data_table(headers: Iterable[str], rows: Iterable[Iterable[str]], widths=None) -> Table:
    data = [
        [Paragraph(str(cell), styles["CNTableHead"]) for cell in headers],
        *[
            [Paragraph(str(cell), styles["CNTableCell"]) for cell in row]
            for row in rows
        ],
    ]
    if widths is None:
        widths = [CONTENT_WIDTH / len(data[0])] * len(data[0])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDF2ED")),
                ("TEXTCOLOR", (0, 0), (-1, 0), INK),
                ("GRID", (0, 0), (-1, -1), 0.45, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                *[
                    ("BACKGROUND", (0, row), (-1, row), SURFACE_SOFT if row % 2 == 0 else SURFACE)
                    for row in range(1, len(data))
                ],
            ]
        )
    )
    return table


def screenshot(path: str, caption: str, width: float = CONTENT_WIDTH, max_height: float = 310) -> list[Flowable]:
    image_path = ROOT / path
    if not image_path.exists():
        return [info_callout("图片缺失", f"未找到截图：{path}", "amber")]
    with PILImage.open(image_path) as image:
        ratio = image.height / image.width
    height = min(width * ratio, max_height)
    rendered_width = width if width * ratio <= max_height else max_height / ratio
    image = Image(str(image_path), width=rendered_width, height=height)
    image.hAlign = "CENTER"
    return [image, paragraph(caption, "CNCaption")]


def code_block(code: str) -> Table:
    code_style = ParagraphStyle(
        "CodeOnDark",
        fontName="Courier",
        fontSize=7,
        leading=11,
        textColor=colors.HexColor("#EAF7F2"),
        wordWrap="CJK",
    )
    block = Table(
        [[Preformatted(code.strip(), code_style)]],
        colWidths=[CONTENT_WIDTH],
        hAlign="LEFT",
    )
    block.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#14221E")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#21352F")),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return block


def architecture_flow() -> Table:
    cell_style = ParagraphStyle(
        "FlowCell",
        parent=styles["CNTableCell"],
        fontSize=7.5,
        leading=11,
        alignment=TA_CENTER,
    )

    def cell(title: str, subtitle: str, background: colors.Color):
        content = Paragraph(
            f"<b>{title}</b><br/><font size='6.5' color='#68746F'>{subtitle}</font>",
            cell_style,
        )
        return content

    top = cell("浏览器 Web 应用", "工作台 / 对话 / 任务 / 工作流", BLUE_SOFT)
    gateway = cell("Node.js Agent Gateway", "模型代理 / 工具注册 / 轨迹聚合", MINT_SOFT)
    model = cell("大模型服务", "OpenAI 兼容 Chat Completions", VIOLET_SOFT)
    tools = cell("企业能力工具", "知识 / 指标 / 任务 / 通知", CORAL_SOFT)

    flow = Table(
        [
            [top],
            [Paragraph("↓", cell_style)],
            [gateway],
            [Paragraph("↙ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↘", cell_style)],
            [Table([[model, "", tools]], colWidths=[220, 62, 220], rowHeights=[56])],
        ],
        colWidths=[CONTENT_WIDTH],
    )
    flow.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, 0), 0.6, BORDER),
                ("BACKGROUND", (0, 0), (-1, 0), BLUE_SOFT),
                ("BOX", (0, 2), (-1, 2), 0.6, MINT),
                ("BACKGROUND", (0, 2), (-1, 2), MINT_SOFT),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    bottom_table = flow._cellvalues[4][0]
    bottom_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), VIOLET_SOFT),
                ("BOX", (0, 0), (0, 0), 0.6, BORDER),
                ("BACKGROUND", (2, 0), (2, 0), CORAL_SOFT),
                ("BOX", (2, 0), (2, 0), 0.6, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return flow


def agent_loop_diagram() -> Table:
    style = ParagraphStyle(
        "LoopCell",
        fontName=PDF_FONT,
        fontSize=7.4,
        leading=10.5,
        textColor=INK_SOFT,
        alignment=TA_CENTER,
        wordWrap="CJK",
    )
    boxes = [
        ("01", "接收任务", "多轮消息与企业上下文", MINT_SOFT),
        ("02", "模型推理", "生成回答或 tool_calls", VIOLET_SOFT),
        ("03", "工具执行", "白名单工具与结果校验", BLUE_SOFT),
        ("04", "结果交付", "回答、来源与执行轨迹", CORAL_SOFT),
    ]
    cells = []
    for number, title, subtitle, background in boxes:
        cells.append(
            Table(
                [
                    [Paragraph(f"<font color='#8A948F'>{number}</font>", style)],
                    [Paragraph(f"<b>{title}</b><br/><font size='6.4' color='#68746F'>{subtitle}</font>", style)],
                ],
                colWidths=[105],
                rowHeights=[16, 43],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), background),
                        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ]
                ),
            )
        )
    arrow = Paragraph("<font color='#9EAAA3'>→</font>", style)
    table = Table(
        [[cells[0], arrow, cells[1], arrow, cells[2], arrow, cells[3]]],
        colWidths=[105, 20, 105, 20, 105, 20, 105],
        hAlign="CENTER",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#101916"))
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.025))
    for x in range(26, int(PAGE_WIDTH), 28):
        canvas.rect(x, 0, 0.4, PAGE_HEIGHT, stroke=0, fill=1)
    for y in range(20, int(PAGE_HEIGHT), 28):
        canvas.rect(0, y, PAGE_WIDTH, 0.4, stroke=0, fill=1)

    canvas.setStrokeColor(colors.Color(0.36, 0.88, 0.71, alpha=0.09))
    canvas.setLineWidth(0.7)
    canvas.circle(PAGE_WIDTH - 30, PAGE_HEIGHT - 10, 135, stroke=1, fill=0)
    canvas.circle(PAGE_WIDTH - 30, PAGE_HEIGHT - 10, 190, stroke=1, fill=0)

    canvas.setFillColor(colors.HexColor("#5CE0B5"))
    canvas.roundRect(44, PAGE_HEIGHT - 86, 30, 30, 6, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#101916"))
    canvas.setFont(PDF_FONT_BOLD, 15)
    canvas.drawCentredString(59, PAGE_HEIGHT - 77, "N")

    canvas.setFillColor(colors.HexColor("#F4FBF8"))
    canvas.setFont("Helvetica-Bold", 21)
    canvas.drawString(86, PAGE_HEIGHT - 76, "NEXA")
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.43))
    canvas.setFont("Helvetica", 6.5)
    canvas.drawString(87, PAGE_HEIGHT - 88, "AGENT WORKSPACE")

    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.46))
    canvas.setFont(PDF_FONT, 9)
    canvas.drawString(44, PAGE_HEIGHT - 178, "传智杯 AI Web 网页开发挑战赛")
    canvas.setFillColor(colors.HexColor("#F4FBF8"))
    canvas.setFont(PDF_FONT_BOLD, 34)
    canvas.drawString(44, PAGE_HEIGHT - 226, "NEXA Agent Workspace")
    canvas.setFont(PDF_FONT, 17)
    canvas.drawString(44, PAGE_HEIGHT - 258, "AI Agent 智能助手与自动化工作流平台")

    canvas.setStrokeColor(colors.Color(0.36, 0.88, 0.71, alpha=0.45))
    canvas.setLineWidth(1)
    canvas.line(44, PAGE_HEIGHT - 286, 160, PAGE_HEIGHT - 286)

    canvas.setFont(PDF_FONT, 10)
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.62))
    canvas.drawString(44, PAGE_HEIGHT - 315, "项目技术文档")
    canvas.setFont(PDF_FONT, 7.5)
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.36))
    canvas.drawString(44, PAGE_HEIGHT - 332, "项目概述 / 需求分析 / 系统架构 / AI 技术方案 / 测试部署")

    info_y = 155
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.045))
    canvas.roundRect(44, info_y, 506, 92, 7, stroke=0, fill=1)
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.08))
    canvas.roundRect(44, info_y, 506, 92, 7, stroke=1, fill=0)
    labels = [
        ("参赛团队", "NEXA Team"),
        ("文档版本", "V1.0"),
        ("项目形态", "Web + Node.js Agent Gateway"),
        ("日期", "2026-11-14"),
    ]
    for index, (label, value) in enumerate(labels):
        col = index % 2
        row = index // 2
        x = 62 + col * 240
        y = info_y + 57 - row * 35
        canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.31))
        canvas.setFont(PDF_FONT, 6.5)
        canvas.drawString(x, y + 10, label)
        canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.76))
        canvas.setFont(PDF_FONT, 8.5)
        canvas.drawString(x, y - 2, value)

    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.28))
    canvas.setFont(PDF_FONT, 7)
    canvas.drawString(44, 35, "基于大模型 · 自主规划 · 工具调用 · 多轮对话 · 自动化工作流")
    canvas.restoreState()


def draw_content_page(canvas, doc):
    page = canvas.getPageNumber()
    canvas.saveState()
    canvas.setFillColor(SURFACE)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

    canvas.setStrokeColor(colors.HexColor("#E7EBE6"))
    canvas.setLineWidth(0.55)
    canvas.line(LEFT, PAGE_HEIGHT - 34, PAGE_WIDTH - RIGHT, PAGE_HEIGHT - 34)

    canvas.setFillColor(MINT)
    canvas.roundRect(LEFT, PAGE_HEIGHT - 31, 7, 7, 2, stroke=0, fill=1)
    canvas.setFillColor(INK)
    canvas.setFont(PDF_FONT_BOLD, 7.2)
    canvas.drawString(LEFT + 13, PAGE_HEIGHT - 31, "NEXA AGENT WORKSPACE")
    canvas.setFillColor(MUTED_LIGHT)
    canvas.setFont(PDF_FONT, 6.6)
    canvas.drawRightString(
        PAGE_WIDTH - RIGHT,
        PAGE_HEIGHT - 31,
        "传智杯 AI Web 网页开发挑战赛 · 技术文档",
    )

    canvas.setStrokeColor(colors.HexColor("#E7EBE6"))
    canvas.line(LEFT, 29, PAGE_WIDTH - RIGHT, 29)
    canvas.setFillColor(MUTED_LIGHT)
    canvas.setFont(PDF_FONT, 6.6)
    canvas.drawString(LEFT, 18, "NEXA Team · 2026")
    canvas.setFont("Courier", 7)
    canvas.drawRightString(PAGE_WIDTH - RIGHT, 18, f"{page:02d}")
    canvas.restoreState()


def build_document() -> None:
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="NEXA Agent Workspace 技术文档",
        author="NEXA Team",
        subject="传智杯 AI Web 网页开发挑战赛技术文档",
    )
    cover_frame = Frame(
        0,
        0,
        PAGE_WIDTH,
        PAGE_HEIGHT,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="cover",
    )
    content_frame = Frame(
        LEFT,
        BOTTOM,
        CONTENT_WIDTH,
        PAGE_HEIGHT - TOP - BOTTOM,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="content",
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
            PageTemplate(id="content", frames=[content_frame], onPage=draw_content_page),
        ]
    )

    story: list[Flowable] = [Spacer(1, PAGE_HEIGHT - 10), PageBreak()]
    from reportlab.platypus import NextPageTemplate

    story.insert(0, NextPageTemplate("content"))

    story.extend(
        [
            Spacer(1, 4),
            paragraph("DOCUMENT MAP", "CNKicker"),
            paragraph("文档导览", "CNH1"),
            paragraph(
                "本技术文档面向大赛评审，完整说明 NEXA 如何将大模型能力转化为可执行、可审核、可观测的智能体工作流。",
                "CNSmall",
            ),
            Spacer(1, 12),
        ]
    )

    guide_rows = [
        ("01", "项目概述", "产品定位、目标用户、核心场景与完成度"),
        ("02", "需求分析", "业务痛点、用户需求与赛题能力映射"),
        ("03", "系统架构", "前端、Agent Gateway、模型与企业工具"),
        ("04", "AI 技术方案", "模型选型、Tool Calling、提示词与优化策略"),
        ("05", "核心功能实现", "对话、工作流、任务、知识库与运行记录"),
        ("06", "测试与部署", "自动化验收、环境配置、演示降级与上线路径"),
        ("07", "创新与总结", "技术、应用、安全创新及后续展望"),
    ]
    guide_table = Table(
        [
            [
                Paragraph(f"<font color='#0D9075'><b>{number}</b></font>", styles["CNTableCell"]),
                Paragraph(f"<b>{title}</b>", styles["CNTableCell"]),
                Paragraph(description, styles["CNTableCell"]),
            ]
            for number, title, description in guide_rows
        ],
        colWidths=[36, 100, CONTENT_WIDTH - 136],
    )
    guide_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -2), 0.45, BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.extend(
        [
            guide_table,
            Spacer(1, 18),
            info_callout(
                "阅读重点",
                "建议评审重点查看第 04 章的 AI 技术方案、第 05 章的核心功能实现，以及第 07 章列出的技术创新点与应用创新点。",
                "mint",
            ),
            Spacer(1, 16),
            paragraph("项目摘要", "CNH2"),
            paragraph(
                "NEXA 是一个面向企业知识工作者的 AI Agent 工作台。用户只需描述目标，Agent 即可自主拆解任务、调用企业知识与业务工具、生成可追溯交付物，并通过人工审核完成关键动作。"
                "项目以原生 Web 前端保证比赛现场启动稳定，以 Node.js 服务端实现真实模型代理与工具调用循环；在未配置模型密钥时自动进入本地演示模式，实现从技术能力到现场可用性的双重保障。",
                "CNBody",
            ),
            Spacer(1, 8),
            Table(
                [
                    [
                        Paragraph("<font size='18' color='#08755F'><b>7</b></font><br/><font size='6.8' color='#68746F'>完整页面</font>", styles["CNTableCell"]),
                        Paragraph("<font size='18' color='#3F78C5'><b>4</b></font><br/><font size='6.8' color='#68746F'>注册工具</font>", styles["CNTableCell"]),
                        Paragraph("<font size='18' color='#7163C7'><b>6</b></font><br/><font size='6.8' color='#68746F'>工作流节点</font>", styles["CNTableCell"]),
                        Paragraph("<font size='18' color='#DF7546'><b>390px</b></font><br/><font size='6.8' color='#68746F'>移动端适配</font>", styles["CNTableCell"]),
                    ]
                ],
                colWidths=[CONTENT_WIDTH / 4] * 4,
                rowHeights=[46],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), SURFACE_SOFT),
                        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                        ("INNERGRID", (0, 0), (-1, -1), 0.4, BORDER),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]
                ),
            ),
            PageBreak(),
        ]
    )

    # 01 项目概述
    story.extend(
        section_header(
            "01",
            "项目概述",
            "从“生成内容”升级为“完成工作”的可观测 Agent 工作台。",
        )
    )
    story.extend(
        [
            paragraph("1.1 项目背景", "CNH2"),
            paragraph(
                "传统 AI 问答产品主要解决文本生成问题，但知识工作者真正需要的是完成一项任务。一个完整任务通常包含理解目标、查找资料、读取业务数据、调用多个系统、形成交付物、通知协作方和等待人工确认等步骤。"
                "NEXA 将这些步骤整合到同一个 Web 产品中，使大模型从聊天助手升级为可执行任务的智能体。",
                "CNBody",
            ),
            Spacer(1, 5),
            info_callout(
                "产品定位",
                "可观测的企业级 AI Agent 工作台：智能对话用于探索任务，工作流用于稳定复用，任务中心用于人工审核，运行记录用于过程追溯。",
                "mint",
            ),
            Spacer(1, 9),
            paragraph("1.2 目标用户与核心痛点", "CNH2"),
            data_table(
                ["用户角色", "主要任务", "现有痛点"],
                [
                    ("运营人员", "周报、复盘、渠道分析", "数据分散、重复整理、指标口径不一致"),
                    ("产品/市场", "竞品追踪、客户洞察", "信息过载、来源不清、结论难验证"),
                    ("项目管理者", "会议纪要、行动项跟进", "决策与执行脱节、负责人不明确"),
                    ("企业开发者", "内部能力接入", "系统烟囱、工具权限复杂、缺少统一编排"),
                ],
                widths=[90, 165, CONTENT_WIDTH - 255],
            ),
            Spacer(1, 11),
            paragraph("1.3 项目完成度", "CNH2"),
            bullet("<b>产品层：</b>工作台、对话、任务、工作流、知识库、工具连接、运行记录 7 个完整页面。"),
            bullet("<b>Agent 层：</b>自主规划、模型 Tool Calling、多轮上下文、知识来源和工具轨迹。"),
            bullet("<b>工程层：</b>无第三方前端依赖、OpenAI 兼容接口、本地演示降级、Playwright 自动化验收。"),
            bullet("<b>交付层：</b>README、环境变量模板、技术文档、演示脚本、运行截图和提交清单。"),
            PageBreak(),
        ]
    )

    # 02 需求分析
    story.extend(
        section_header(
            "02",
            "需求分析",
            "围绕赛题能力与真实工作流，定义功能边界、交互要求和安全要求。",
        )
    )
    story.extend(
        [
            paragraph("2.1 赛题能力映射", "CNH2"),
            data_table(
                ["赛题要求", "产品响应", "可验证证据"],
                [
                    ("基于大模型", "接入 OpenAI 兼容 Chat Completions", "配置 Key 后显示 LLM 在线，服务端真实调用模型"),
                    ("自主规划", "模型拆解目标并展示高层执行计划", "对话结果中的“执行计划”"),
                    ("工具调用", "原生 tool_calls 白名单执行", "知识、指标、任务、通知工具轨迹"),
                    ("多轮对话", "保存历史消息并在会话内连续追问", "同一会话多次发送与重新生成"),
                    ("自动化工作流", "可视化节点、运行状态、日志和人工审核", "运营周报六节点流程"),
                    ("Web 应用", "七个一级页面与移动端适配", "桌面和 390px 视口自动化截图"),
                ],
                widths=[90, 185, CONTENT_WIDTH - 275],
            ),
            Spacer(1, 13),
            paragraph("2.2 功能性需求", "CNH2"),
            numbered(1, "用户能够以自然语言描述目标，并获得 Agent 的执行计划与最终结果。"),
            numbered(2, "Agent 能够根据任务需要选择知识、数据、任务或通知工具，并记录执行状态。"),
            numbered(3, "用户能够继续追问、停止执行、重新生成，并将回答转为可追踪任务。"),
            numbered(4, "用户能够查看和运行可复用工作流，编辑节点并查看执行日志。"),
            numbered(5, "用户能够检索企业知识、上传文档、管理工具授权和查看运行记录。"),
            Spacer(1, 12),
            paragraph("2.3 非功能性需求", "CNH2"),
            Table(
                [
                    [
                        info_callout("稳定性", "无 Key、无网络时自动进入演示模式，保证比赛现场可运行。", "mint"),
                        info_callout("可观测", "计划、工具、来源、耗时、Token 与错误阶段均可查看。", "blue"),
                    ],
                    [
                        info_callout("安全性", "密钥仅在服务端；写操作工具受提示词和人工审核约束。", "amber"),
                        info_callout("可用性", "桌面与移动端适配，关键操作均有明确状态反馈。", "violet"),
                    ],
                ],
                colWidths=[CONTENT_WIDTH / 2 - 4, CONTENT_WIDTH / 2 - 4],
                hAlign="LEFT",
                style=TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (0, -1), 8),
                        ("RIGHTPADDING", (1, 0), (1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
                    ]
                ),
            ),
            PageBreak(),
        ]
    )

    # 03 系统架构
    story.extend(
        section_header(
            "03",
            "系统架构设计",
            "浏览器体验层、Agent Gateway 层与企业能力层解耦，兼顾现场稳定性与真实模型能力。",
        )
    )
    story.extend(
        [
            paragraph("3.1 总体架构", "CNH2"),
            architecture_flow(),
            paragraph("图 3-1 NEXA 总体架构", "CNCaption"),
            Spacer(1, 12),
            paragraph("3.2 浏览器体验层", "CNH2"),
            paragraph(
                "前端使用原生 HTML、CSS 与 ES6 JavaScript，无第三方运行时依赖。状态集中维护在 assets/app.js 中，页面通过模板渲染更新。"
                "选择原生方案的原因是降低比赛现场安装和构建风险，同时保留组件化模板、统一状态、响应式布局与完整交互能力。",
                "CNBody",
            ),
            data_table(
                ["模块", "职责", "关键实现"],
                [
                    ("index.html", "应用入口、侧栏、顶栏、全局浮层", "语义化布局与本地图标系统"),
                    ("styles.css", "设计系统、七个页面、响应式", "CSS 变量、Grid/Flex、断点适配"),
                    ("app.js", "状态、渲染、事件、交互", "统一 renderView、事件委托、生成令牌"),
                    ("icons.js", "线性图标", "本地 Lucide 路径，无网络依赖"),
                ],
                widths=[90, 180, CONTENT_WIDTH - 270],
            ),
            Spacer(1, 12),
            paragraph("3.3 Agent Gateway 层", "CNH2"),
            paragraph(
                "Node.js 服务端提供静态资源、健康检查和 Agent 运行接口。它读取服务端环境变量，将多轮消息与系统提示词发送给 OpenAI 兼容接口；"
                "当模型返回 tool_calls 时，通过白名单工具注册表执行工具，再将结构化结果写回上下文。",
                "CNBody",
            ),
            code_block(
                """
POST /api/agent/run
messages + system prompt
  -> Chat Completions API
  -> tool_calls? -> execute whitelist tool -> append tool result
  -> final response + plan + toolTrace + sources
                """
            ),
            Spacer(1, 10),
            paragraph("3.4 企业能力层", "CNH2"),
            paragraph(
                "比赛版本使用内置演示数据和结构化返回，接口形态与真实企业系统保持一致。后续可将知识检索替换为向量数据库，"
                "将指标工具替换为数据仓库 API，将任务与通知替换为飞书、企业微信或 Jira。",
                "CNBody",
            ),
            Spacer(1, 8),
            paragraph("3.5 数据流与状态设计", "CNH2"),
            data_table(
                ["执行阶段", "输入", "输出与状态"],
                [
                    ("接收请求", "多轮消息、Agent 配置、会话标识", "标准化消息数组与运行 ID"),
                    ("模型推理", "系统提示词、上下文、工具 Schema", "文本回答或结构化 tool_calls"),
                    ("工具执行", "工具名称、参数、权限边界", "结构化结果、状态与可读摘要"),
                    ("结果交付", "模型最终回答、工具轨迹、来源", "前端消息、运行记录与任务状态"),
                ],
                widths=[85, 180, CONTENT_WIDTH - 265],
            ),
            Spacer(1, 12),
            paragraph("3.6 关键工程决策", "CNH2"),
            data_table(
                ["决策", "选择", "权衡"],
                [
                    ("前端方案", "原生 Web，无第三方运行时依赖", "减少构建风险，组件抽象由模板函数承担"),
                    ("Agent 网关", "Node.js 内置 HTTP 与 fetch", "部署简单，后续可替换为 Express/Fastify"),
                    ("模型协议", "OpenAI 兼容 Chat Completions", "供应商可切换，覆盖主流工具调用能力"),
                    ("演示降级", "本地结构化响应器", "无 Key 或无网络仍可完整展示交互"),
                ],
                widths=[90, 210, CONTENT_WIDTH - 300],
            ),
            info_callout(
                "架构原则",
                "体验层、Agent Gateway 层与企业能力层保持清晰边界，使比赛版本可以稳定运行，同时为企业级替换保留接口空间。",
                "blue",
            ),
            PageBreak(),
        ]
    )

    # 04 AI
    story.extend(
        section_header(
            "04",
            "AI 技术方案",
            "重点说明模型选型、集成方式、Tool Calling 循环、提示词约束与优化策略。",
        )
    )
    story.extend(
        [
            paragraph("4.1 模型选型理由", "CNH2"),
            paragraph(
                "项目选择 OpenAI 兼容 Chat Completions 协议作为模型抽象层。该协议支持多轮消息、系统提示词、JSON Schema 工具定义与 tool_calls，"
                "能够覆盖 Agent 所需的核心能力，同时兼容 DeepSeek、OpenAI、企业私有模型网关等多种实现。",
                "CNBody",
            ),
            data_table(
                ["评估维度", "选择逻辑", "项目收益"],
                [
                    ("工具调用", "原生 tools 参数与 tool_calls 返回", "无需自行解析文本协议，可靠性和扩展性更高"),
                    ("多轮上下文", "标准 messages 数组", "会话历史与工具结果自然进入上下文"),
                    ("供应商兼容", "OpenAI 兼容协议生态成熟", "通过 Base URL 与 Model 切换供应商"),
                    ("现场稳定", "服务端可统一超时、降级与错误处理", "模型不可用时保留完整演示"),
                ],
                widths=[90, 200, CONTENT_WIDTH - 290],
            ),
            Spacer(1, 12),
            paragraph("4.2 Agent 集成方式", "CNH2"),
            agent_loop_diagram(),
            paragraph("图 4-1 Agent 执行循环", "CNCaption"),
            Spacer(1, 9),
            paragraph(
                "服务端最多执行四轮工具调用，每次工具结果都写回 messages。该上限避免模型无限选择工具，同时足以覆盖“读取多个数据源 → 创建任务 → 发送通知”等常见任务。",
                "CNBody",
            ),
            paragraph("4.3 工具调用设计", "CNH2"),
            data_table(
                ["工具", "参数", "用途", "边界"],
                [
                    ("search_knowledge", "query, limit", "检索企业知识和来源", "只读"),
                    ("get_project_metrics", "scope", "读取运营指标", "只读"),
                    ("create_follow_up", "title, owner, due", "创建后续任务", "写操作"),
                    ("send_notification", "channel, summary", "发送协作摘要", "写操作"),
                ],
                widths=[105, 125, 180, CONTENT_WIDTH - 410],
            ),
            Spacer(1, 12),
            paragraph("4.4 提示词与优化策略", "CNH2"),
            bullet("<b>目标优先：</b>要求模型先理解目标、约束和期望交付物，再决定步骤。"),
            bullet("<b>事实约束：</b>涉及内部事实、产品数据和市场情报时必须调用工具。"),
            bullet("<b>失败可解释：</b>工具失败时说明影响并给出替代方案，而不是重复调用。"),
            bullet("<b>高层计划：</b>只展示执行计划，不要求模型输出隐藏思维链。"),
            bullet("<b>写操作确认：</b>发送与创建任务只在用户明确要求时调用。"),
            PageBreak(),
        ]
    )

    # 05 核心功能
    story.extend(
        section_header(
            "05",
            "核心功能实现",
            "以真实运行截图说明产品交互、Agent 过程展示和自动化闭环。",
        )
    )
    story.extend(
        [
            paragraph("5.1 工作台与 Agent 团队", "CNH2"),
            paragraph(
                "工作台将任务入口、效率指标、Agent 团队、实时执行、自动化和最近动态整合在同一信息层级中。用户可以直接输入目标，也可以选择预设任务或进入具体 Agent。",
                "CNBody",
            ),
            *screenshot("screenshots/01-dashboard.png", "图 5-1 工作台首屏：任务入口、指标与 Agent 团队"),
            PageBreak(),
            paragraph("5.2 智能对话与工具轨迹", "CNH2"),
            paragraph(
                "输入“生成运营周报”后，Agent 展示执行计划、读取项目指标、检索企业知识并创建后续任务。最终回答包含关键数据、洞察、建议和来源。"
                "工具调用区域可展开查看每个工具的结果摘要和完成状态。",
                "CNBody",
            ),
            *screenshot("screenshots/02-agent-chat.png", "图 5-2 智能对话：执行计划、工具轨迹与知识来源"),
            Spacer(1, 8),
            paragraph("5.2.1 对话结果的数据结构", "CNH2"),
            data_table(
                ["字段", "作用", "界面呈现"],
                [
                    ("content", "模型生成的最终回答", "正文消息与结构化结论"),
                    ("plan", "高层执行计划", "消息上方的步骤条"),
                    ("toolTrace", "工具名称、摘要与状态", "可展开的工具调用记录"),
                    ("sources", "知识文档标题与类型", "回答下方的参考来源"),
                    ("mode", "真实模型或演示模式", "消息标题旁的 LLM / DEMO 标识"),
                ],
                widths=[80, 190, CONTENT_WIDTH - 270],
            ),
            PageBreak(),
            paragraph("5.3 可视化工作流", "CNH2"),
            paragraph(
                "工作流画布包含触发器、任务规划、知识检索、质量校验、生成交付物和发送通知六个节点。节点可拖拽和缩放，右侧检查器可配置模型、超时、失败重试和人工审核。",
                "CNBody",
            ),
            *screenshot("screenshots/03-workflow-builder.png", "图 5-3 工作流编排：节点画布与配置检查器", max_height=290),
            Spacer(1, 5),
            info_callout(
                "执行闭环",
                "点击运行后，节点按执行顺序变色并写入日志，完成后自动新增一条运行记录，体现从编排到可观测执行的完整过程。",
                "blue",
            ),
            Spacer(1, 10),
            paragraph("5.3.1 节点类型", "CNH2"),
            data_table(
                ["节点类型", "职责", "示例"],
                [
                    ("触发器", "接收手动、定时或 Webhook 事件", "每周五自动运行"),
                    ("Agent 节点", "完成理解、推理、生成或判断", "任务规划、生成交付物"),
                    ("工具节点", "调用知识、数据或协作系统", "知识检索、发送飞书"),
                    ("条件节点", "根据变量或模型判断控制流程", "质量校验、人工审核"),
                ],
                widths=[85, 205, CONTENT_WIDTH - 290],
            ),
            PageBreak(),
            paragraph("5.4 任务中心与人工审核", "CNH2"),
            paragraph(
                "任务中心用四阶段看板管理 Agent 工作：待处理、进行中、等待审核和已完成。涉及发送通知等关键动作时，任务进入待审核，人工确认后才继续执行。",
                "CNBody",
            ),
            *screenshot("screenshots/05-task-center.png", "图 5-4 任务中心：四阶段看板与人工审核"),
            Spacer(1, 9),
            paragraph("5.5 企业知识与工具连接", "CNH2"),
            paragraph(
                "知识库提供文档分类、检索、引用统计、上传解析与内容预览；工具连接管理飞书、企业微信、Notion、GitHub、Webhook 和自定义 REST API 的授权与启停。"
                "这两部分共同构成 Agent 的企业事实与执行能力边界。",
                "CNBody",
            ),
            *screenshot("screenshots/06-knowledge-base.png", "图 5-5 企业知识库：分类、引用和内容预览", max_height=260),
            PageBreak(),
            paragraph("5.6 运行可观测性", "CNH2"),
            paragraph(
                "运行记录展示总运行次数、成功率、平均耗时、异常数量和执行轨迹。展开记录可查看每个节点的状态、错误阶段、Token 用量与输出摘要，"
                "将“AI 是否完成”转化为可审计的工程事实。",
                "CNBody",
            ),
            *screenshot("screenshots/08-run-observability.png", "图 5-6 运行记录：轨迹、状态、耗时与异常恢复"),
            Spacer(1, 8),
            paragraph("5.6.1 可观测指标与异常恢复", "CNH2"),
            data_table(
                ["指标 / 机制", "含义", "产品价值"],
                [
                    ("成功率", "成功运行数占总运行数比例", "判断工作流整体稳定性"),
                    ("平均耗时", "任务从触发到交付的平均时间", "评估 Agent 效率与体验"),
                    ("Token 用量", "单次运行的模型消耗", "支持成本分析与模型路由"),
                    ("失败阶段", "具体失败节点与错误摘要", "快速定位权限、数据或配置问题"),
                    ("重新运行", "使用最新凭据重新发起任务", "缩短故障恢复路径"),
                ],
                widths=[95, 195, CONTENT_WIDTH - 290],
            ),
            PageBreak(),
        ]
    )

    # 06 测试与部署
    story.extend(
        section_header(
            "06",
            "测试与部署",
            "通过语法检查、真实浏览器交互、截图和移动端视口验证产品可用性。",
        )
    )
    story.extend(
        [
            paragraph("6.1 测试策略", "CNH2"),
            data_table(
                ["测试层级", "验证内容", "执行方式"],
                [
                    ("语法检查", "server.mjs、app.js、icons.js", "npm run check"),
                    ("桌面交互", "对话生成、连续追问、工作流运行、上传、工具开关", "Playwright + Edge"),
                    ("视觉验收", "11 张关键页面截图", "自动截图并人工检查"),
                    ("移动端", "390 × 844 视口与抽屉导航", "Playwright viewport"),
                    ("异常检查", "控制台错误与页面横向溢出", "自动化断言"),
                ],
                widths=[90, 260, CONTENT_WIDTH - 350],
            ),
            Spacer(1, 12),
            paragraph("6.2 环境配置", "CNH2"),
            code_block(
                """
Node.js >= 20
npm run dev

.env
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
LLM_API_KEY=your_api_key
PORT=4173
                """
            ),
            Spacer(1, 10),
            paragraph(
                "项目前端没有第三方依赖，Node 服务使用内置 HTTP、文件系统和 fetch 能力。浏览器自动化验收可选安装 Python Playwright，并复用本机 Edge。",
                "CNBody",
            ),
            paragraph("6.3 部署路径", "CNH2"),
            numbered(1, "将代码推送到 GitHub 或 Gitee 公开仓库，确认 .env 未提交。"),
            numbered(2, "在支持 Node.js 20 的云平台创建 Web 服务，启动命令为 node server.mjs。"),
            numbered(3, "在平台环境变量中配置 LLM_BASE_URL、LLM_MODEL、LLM_API_KEY 和 PORT。"),
            numbered(4, "使用平台提供的公网地址完成评审访问验证。"),
            Spacer(1, 10),
            info_callout(
                "现场稳定性",
                "若比赛现场无法访问外网或模型接口异常，系统自动进入本地演示模式。模型代理、工具结构和前端交互保持一致。",
                "amber",
            ),
            PageBreak(),
        ]
    )

    # 07 创新与总结
    story.extend(
        section_header(
            "07",
            "创新点与总结展望",
            "明确区分技术创新与应用创新，并给出企业级扩展路线。",
        )
    )
    story.extend(
        [
            paragraph("7.1 技术创新点", "CNH2"),
            data_table(
                ["创新点", "说明", "价值"],
                [
                    ("Agent 过程可视化", "展示计划、工具、来源、状态与耗时", "降低黑盒感，提升结果可信度"),
                    ("对话与工作流统一", "对话探索、工作流固化、任务审核", "覆盖一次性和重复性工作"),
                    ("真模型 + 演示双模式", "OpenAI 兼容真实调用与本地结构化降级", "兼顾技术真实性与比赛稳定性"),
                    ("运行级可观测性", "Token、耗时、工具状态和失败阶段", "便于定位问题和持续优化"),
                    ("无构建前端架构", "原生 Web + 本地图标系统", "启动快、依赖少、现场风险低"),
                ],
                widths=[125, 220, CONTENT_WIDTH - 345],
            ),
            Spacer(1, 13),
            paragraph("7.2 应用创新点", "CNH2"),
            bullet("<b>周报自动交付：</b>指标读取、知识检索、洞察生成和任务创建一次完成。"),
            bullet("<b>人工审核闭环：</b>将发送与任务创建等写操作放入可审核节点。"),
            bullet("<b>企业知识优先：</b>回答展示来源，便于用户核验内部事实。"),
            bullet("<b>业务人员可读：</b>用自然语言发起任务，不需要理解模型参数或 API。"),
            bullet("<b>移动端可追踪：</b>在手机上查看任务、运行状态和审核动作。"),
            Spacer(1, 12),
            paragraph("7.3 总结", "CNH2"),
            paragraph(
                "NEXA 完成了从目标输入、自主规划、工具调用、知识引用、结果交付到人工审核的完整 Agent 闭环。项目没有停留在静态界面或单轮问答，"
                "而是以真实服务端调用、结构化工具结果、可观测运行记录和自动化测试证明其可用性。",
                "CNBody",
            ),
            paragraph("7.4 展望", "CNH2"),
            data_table(
                ["阶段", "扩展方向"],
                [
                    ("模型层", "SSE 流式输出、多模型路由、成本与延迟策略"),
                    ("知识层", "文档解析、向量数据库、混合检索、权限过滤"),
                    ("工具层", "OAuth、RBAC、OpenAPI 自动注册、企业系统深度连接"),
                    ("工作流", "版本管理、发布审批、回滚、条件分支与循环"),
                    ("协作层", "多 Agent 协作、任务交接、团队共享与评论"),
                ],
                widths=[90, CONTENT_WIDTH - 90],
            ),
            Spacer(1, 14),
            info_callout(
                "项目结论",
                "NEXA 将大模型能力封装为可规划、可执行、可审核、可追溯的智能体工作台，符合传智杯 AI Web 网页开发挑战赛对 AI Agent、自动化工作流与 Web 应用的综合要求。",
                "mint",
            ),
            Spacer(1, 12),
            paragraph("附录 A：核心文件", "CNH2"),
            data_table(
                ["文件", "说明"],
                [
                    ("server.mjs", "Agent Gateway、模型调用、工具注册与执行循环"),
                    ("assets/app.js", "前端状态、页面模板、事件与交互逻辑"),
                    ("assets/styles.css", "设计系统与桌面/移动端响应式样式"),
                    ("tests/visual_check.py", "Playwright 视觉与交互自动化验收"),
                    ("docs/", "项目说明、技术方案、演示脚本和提交清单"),
                ],
                widths=[135, CONTENT_WIDTH - 135],
            ),
        ]
    )

    doc.build(story)


if __name__ == "__main__":
    build_document()
    print(OUTPUT)
