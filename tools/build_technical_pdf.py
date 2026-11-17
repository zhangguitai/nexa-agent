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
        ("文档版本", "V1.1"),
        ("项目形态", "Web + Node.js Agent Gateway"),
        ("日期", "2026-11-16"),
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
        ("03", "系统架构", "模块边界、API 契约、数据流与错误策略"),
        ("04", "AI 技术方案", "模型选型、Tool Calling、上下文管理与评估"),
        ("05", "核心功能实现", "对话、工作流、任务、知识库与运行记录"),
        ("06", "测试与部署", "用例矩阵、自动化验收、部署拓扑与上线路径"),
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
            paragraph("2.4 用户任务旅程与验收标准", "CNH2"),
            paragraph(
                "为避免只验证页面是否存在，项目以“用户目标是否被完成”作为核心验收标准。任务旅程覆盖输入、规划、执行、审核和复盘五个阶段，"
                "每个阶段都对应可观察的界面状态与数据结构。",
                "CNBody",
            ),
            data_table(
                ["阶段", "用户动作", "系统响应", "验收标准"],
                [
                    ("输入", "用自然语言描述目标", "识别任务并建立会话上下文", "空输入被阻止，发送后立即可见任务状态"),
                    ("规划", "等待 Agent 选择执行路径", "展示高层执行计划与步骤", "计划不展示隐藏思维链，只展示可理解的动作"),
                    ("执行", "观察工具调用或工作流推进", "调用白名单工具，记录状态与来源", "工具名称、摘要、成功/失败状态可见"),
                    ("审核", "确认发送、任务或高风险动作", "任务进入待审核，暂停后续写操作", "未确认前不执行外部写操作"),
                    ("复盘", "查看运行记录并重新运行", "展示轨迹、耗时、Token 与失败阶段", "失败记录可定位到具体节点或工具"),
                ],
                widths=[55, 118, 160, CONTENT_WIDTH - 333],
            ),
            Spacer(1, 12),
            paragraph("2.5 需求优先级与边界", "CNH2"),
            data_table(
                ["优先级", "需求", "本期实现", "边界说明"],
                [
                    ("P0", "自主规划与工具调用", "已实现", "受工具白名单与四轮循环限制"),
                    ("P0", "多轮对话与过程可见", "已实现", "同一会话保留有限历史，避免上下文无限增长"),
                    ("P0", "自动化工作流与人工审核", "已实现", "工作流运行为可观测模拟执行"),
                    ("P1", "企业知识与工具连接", "已实现", "比赛版使用内置知识与连接状态"),
                    ("P1", "运行记录与异常恢复", "已实现", "覆盖轨迹、耗时、Token 与失败阶段"),
                    ("P2", "真实企业 OAuth 与多租户", "预留接口", "不纳入当前比赛版本范围"),
                ],
                widths=[48, 150, 90, CONTENT_WIDTH - 288],
            ),
            Spacer(1, 12),
            paragraph("2.6 产品评价指标", "CNH2"),
            data_table(
                ["评价指标", "定义", "目标", "数据来源"],
                [
                    ("任务完成率", "用户目标形成结构化结果的比例", "核心场景可稳定完成", "会话结果与运行记录"),
                    ("工具成功率", "工具调用成功数占总调用数比例", "持续提升并保留失败轨迹", "toolTrace"),
                    ("轨迹完整度", "计划、工具、来源、状态齐全的比例", "关键步骤无缺失", "对话结果与运行详情"),
                    ("人工介入率", "需要人工审核或修正的任务比例", "高风险动作必须介入", "任务中心状态"),
                    ("降级可用性", "无 Key 或模型异常时仍能演示的比例", "核心流程始终可用", "DEMO / DEMO-FALLBACK 运行"),
                ],
                widths=[85, 205, 125, CONTENT_WIDTH - 415],
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
            paragraph("3.7 API 契约与错误处理", "CNH2"),
            paragraph(
                "前后端只通过明确的 JSON 接口交互。对话请求只接受用户与助手消息，服务端统一补充系统提示词和工具定义；"
                "模型输出经过结构化聚合后返回正文、计划、工具轨迹和知识来源，前端不直接接触模型原始协议。",
                "CNBody",
            ),
            code_block(
                """
POST /api/agent/run
{
  "messages": [
    {"role": "user", "content": "Generate weekly product operations report"}
  ]
}

200 OK
{
  "ok": true,
  "mode": "llm | demo",
  "content": "Weekly report generated",
  "plan": ["Understand goal", "Read metrics", "Search knowledge", "Generate report"],
  "toolTrace": [{"label": "Project metrics", "status": "done"}],
  "sources": [{"title": "Growth playbook", "type": "strategy"}]
}
                """
            ),
            Spacer(1, 10),
            data_table(
                ["异常类型", "服务端处理", "前端呈现"],
                [
                    ("消息为空或超长", "返回 400，限制单条消息长度", "提示用户补充或缩短输入"),
                    ("模型超时", "35 秒超时后进入演示降级", "保留结果结构并标记 DEMO"),
                    ("模型接口错误", "记录错误摘要，返回降级响应", "不中断会话，可继续追问"),
                    ("工具执行失败", "将结构化失败结果回写模型", "轨迹显示失败状态与影响"),
                    ("未知工具名称", "拒绝执行并返回错误结果", "不暴露任意代码执行能力"),
                ],
                widths=[95, 220, CONTENT_WIDTH - 315],
            ),
            Spacer(1, 10),
            info_callout(
                "错误处理原则",
                "系统错误对用户保持可读、对开发者保持可定位；模型失败不应导致页面不可用，工具失败不应伪造成功结果。",
                "amber",
            ),
            Spacer(1, 10),
            paragraph("3.8 可观测数据模型", "CNH2"),
            data_table(
                ["字段", "含义", "产生位置", "界面用途"],
                [
                    ("runId", "一次运行或消息执行的唯一标识", "Gateway 创建请求", "关联运行记录与工具轨迹"),
                    ("mode", "LLM、DEMO 或 DEMO-FALLBACK", "服务端响应", "标识真实模型或降级模式"),
                    ("plan", "高层执行步骤", "工具轨迹聚合", "消息顶部计划条"),
                    ("toolTrace", "工具名称、摘要和状态", "工具执行结果", "展开查看调用过程"),
                    ("sources", "知识文档标题与类型", "知识检索结果", "回答下方来源标签"),
                    ("duration", "执行耗时", "运行结束时间减开始时间", "运行记录与性能分析"),
                    ("status", "idle / running / done / error", "节点或运行状态机", "节点颜色、标签和异常恢复"),
                ],
                widths=[75, 170, 140, CONTENT_WIDTH - 385],
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
            paragraph("4.5 工具 Schema 与执行契约", "CNH2"),
            paragraph(
                "工具不是自由文本函数，而是带名称、用途、参数 Schema 和白名单边界的结构化能力。模型只能从已注册工具中选择，"
                "服务端在执行前解析参数、校验工具名，并把结果转换为模型可继续消费的 tool message。",
                "CNBody",
            ),
            code_block(
                """
{
  "type": "function",
  "function": {
    "name": "get_project_metrics",
    "description": "Read product operations metrics",
    "parameters": {
      "type": "object",
      "properties": {
        "scope": {"type": "string", "enum": ["product", "growth"]}
      },
      "required": ["scope"]
    }
  }
}
                """
            ),
            Spacer(1, 10),
            data_table(
                ["执行约束", "实现方式", "解决的问题"],
                [
                    ("工具白名单", "仅注册四个函数，未知名称返回错误", "防止模型调用任意代码或外部动作"),
                    ("参数 Schema", "按 JSON Schema 约束范围和枚举", "减少无效参数与歧义调用"),
                    ("最大循环", "单次请求最多四轮工具调用", "控制 Token、时延和失控风险"),
                    ("结果回写", "tool result 以结构化 JSON 注入上下文", "保证下一轮模型推理基于真实结果"),
                    ("可读轨迹", "将工具结果压缩为 label、detail、status", "兼顾调试信息与用户可读性"),
                ],
                widths=[90, 235, CONTENT_WIDTH - 325],
            ),
            Spacer(1, 12),
            paragraph("4.6 多轮上下文与 Token 优化", "CNH2"),
            paragraph(
                "前端仅将最近 10 条非执行中消息发送给服务端，单条内容限制为 12,000 字符。该策略保留必要的任务连续性，"
                "同时避免历史消息无限扩张导致模型成本、延迟和无关信息干扰持续上升。",
                "CNBody",
            ),
            data_table(
                ["策略", "当前实现", "优化目标"],
                [
                    ("历史裁剪", "仅保留最近 10 条消息", "控制上下文长度与响应时延"),
                    ("进行中隔离", "pending 消息不发送给模型", "避免模型看到未完成占位内容"),
                    ("工具结果压缩", "只回写结构化摘要，不注入整份前端页面", "减少无关 Token"),
                    ("来源限定", "知识工具返回标题、类型与命中内容", "支持引用核验，避免整库注入"),
                    ("生成令牌", "停止或覆盖旧请求时作废旧响应", "避免异步结果覆盖新会话"),
                ],
                widths=[95, 225, CONTENT_WIDTH - 320],
            ),
            info_callout(
                "上下文原则",
                "只向模型提供完成任务所需的最近上下文、当前目标和必要工具结果，不把全部页面状态和企业数据一次性注入模型。",
                "blue",
            ),
            PageBreak(),
            paragraph("4.7 模型评估与降级策略", "CNH2"),
            paragraph(
                "模型评估不仅关注回答是否流畅，还要检查工具选择是否正确、事实是否来自工具、写操作是否遵守边界，以及失败时能否给出可执行说明。"
                "项目将评估结果分为自动可验证项与人工可验证项，避免只看主观回答质量。",
                "CNBody",
            ),
            data_table(
                ["评估维度", "检查方法", "通过标准"],
                [
                    ("工具选择", "输入周报、竞品、会议等任务，检查是否调用对应只读工具", "不遗漏必要工具，不调用无关写工具"),
                    ("事实一致性", "对比回答指标与工具返回数据", "关键数字与来源一致"),
                    ("多轮连续性", "首轮生成后追问优先级或对象", "保留上下文并正确修改结果"),
                    ("写操作边界", "输入未明确要求发送的任务", "不擅自发送或创建任务"),
                    ("失败可解释", "模拟超时、工具错误和空响应", "说明失败影响并给出替代路径"),
                    ("响应性能", "记录首轮与工具轮耗时", "常规任务在可接受时延内完成"),
                ],
                widths=[95, 250, CONTENT_WIDTH - 345],
            ),
            Spacer(1, 12),
            data_table(
                ["运行状态", "触发条件", "系统行为", "用户可见结果"],
                [
                    ("LLM", "配置有效 Key 且接口正常", "真实模型调用与 Tool Calling", "显示 LLM 模式标记"),
                    ("DEMO", "未配置 Key", "本地结构化响应器", "完整演示规划、工具和结果"),
                    ("DEMO-FALLBACK", "模型或网络异常", "记录错误并返回演示结构", "会话不中断，标记降级模式"),
                ],
                widths=[90, 130, 175, CONTENT_WIDTH - 395],
            ),
            Spacer(1, 10),
            info_callout(
                "优化策略",
                "通过受限工具集、四轮上限、上下文裁剪、结构化结果压缩、超时控制和演示降级，在可靠性、成本与现场稳定性之间取得平衡。",
                "mint",
            ),
            Spacer(1, 12),
            paragraph("4.8 AI 方案选型对比", "CNH2"),
            data_table(
                ["候选方案", "优点", "局限", "本项目结论"],
                [
                    ("纯提示词问答", "接入快、实现简单", "不能读取企业事实，不能执行工具动作", "仅作为基础生成能力"),
                    ("自建 Agent 框架", "能力扩展空间大", "依赖多、调试和现场部署成本更高", "保留后续扩展，不作为比赛版最小依赖"),
                    ("OpenAI 兼容原生 Tool Calling", "协议标准、工具调用可靠、供应商可切换", "需要服务端管理白名单、超时与降级", "采用，作为核心集成方案"),
                    ("企业私有模型网关", "数据控制更强、可接入内网模型", "需要额外基础设施与接口适配", "通过兼容 Base URL 预留"),
                ],
                widths=[120, 150, 175, CONTENT_WIDTH - 445],
            ),
            Spacer(1, 10),
            info_callout(
                "选型结论",
                "选择 OpenAI 兼容原生 Tool Calling，而不是依赖文本协议模拟工具调用；同时保留模型供应商和私有网关替换能力。",
                "violet",
            ),
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
            paragraph("5.2.2 多轮对话与异步状态实现", "CNH2"),
            paragraph(
                "每次发送消息时，前端先写入用户消息和 pending 助手占位，再以最近历史发起服务端请求。服务端返回后，前端按消息 ID 替换占位；"
                "停止生成或重新发起时，生成令牌会递增，使旧请求结果失去写入资格。",
                "CNBody",
            ),
            data_table(
                ["步骤", "前端状态", "用户可见反馈", "异常处理"],
                [
                    ("1. 接收输入", "清理首尾空白，阻止空消息", "输入框立即清空", "空输入保持焦点，不创建消息"),
                    ("2. 创建占位", "写入 user 和 pending assistant", "显示理解、规划、工具、结果步骤", "生成中禁用发送按钮"),
                    ("3. 请求 Agent", "提交最近 10 条非 pending 消息", "显示“正在执行”阶段", "请求失败时切换本地响应"),
                    ("4. 写入结果", "按消息 ID 替换 pending", "展示 plan、toolTrace、sources", "旧令牌结果被丢弃"),
                    ("5. 继续追问", "保留当前会话历史", "用户可以继续补充要求", "停止后保留已生成内容"),
                ],
                widths=[70, 145, 165, CONTENT_WIDTH - 380],
            ),
            Spacer(1, 12),
            paragraph("5.2.3 运行时状态模型", "CNH2"),
            code_block(
                """
const state = {
  activeConversationId,
  conversations: [{ id, title, messages: [] }],
  generating,
  generationToken,
  mode: "llm" | "demo"
}

request started -> token = ++generationToken
request finished -> if token matches, replace pending message
user stops -> increment token, reject stale response
                """
            ),
            Spacer(1, 10),
            info_callout(
                "实现价值",
                "通过消息状态、生成令牌和结构化结果三层配合，避免重复发送、异步覆盖、历史污染和停止生成后仍写入旧答案。",
                "blue",
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
            paragraph("5.3.2 工作流执行状态机", "CNH2"),
            paragraph(
                "工作流运行以节点为单位产生状态变化。每个节点从 idle 进入 running，再进入 done；失败时可记录 error 并触发重试或人工处理。"
                "前端同步更新节点颜色、画布连线和执行日志，使运行过程与数据状态保持一致。",
                "CNBody",
            ),
            data_table(
                ["节点", "执行职责", "输入", "输出"],
                [
                    ("手动触发", "创建工作流运行实例", "任务目标、发起人", "runId 与初始上下文"),
                    ("任务规划", "解析目标并确定节点顺序", "目标与 Agent 配置", "可执行步骤计划"),
                    ("知识检索", "读取指标与知识来源", "检索条件", "指标、知识片段与来源"),
                    ("质量校验", "检查事实、格式与敏感信息", "生成内容和来源", "通过/拦截状态"),
                    ("生成交付物", "组织结构化结果", "校验后的上下文", "周报正文与建议"),
                    ("发送飞书", "执行通知或等待审核", "交付摘要与渠道", "发送结果或待审核状态"),
                ],
                widths=[78, 145, 130, CONTENT_WIDTH - 353],
            ),
            Spacer(1, 12),
            code_block(
                """
idle --run--> running --success--> done
                  |
                  +--error--> retry / manual_review / failed

runWorkflow():
  reset node status
  for each node in order:
    mark running, append log, render state
  mark all nodes done
  append run record and notify success
                """
            ),
            Spacer(1, 10),
            info_callout(
                "可观测设计",
                "节点状态、执行日志和运行记录使用同一套状态语义，避免界面显示完成但运行记录失败，或日志与画布状态不一致。",
                "mint",
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
            paragraph("5.5.1 企业知识检索流程", "CNH2"),
            paragraph(
                "知识检索不是简单全文搜索，而是将用户目标转换为检索条件，限定文档范围并返回可引用来源。比赛版使用内置知识与关键词匹配，"
                "接口保留可替换为向量数据库、混合检索和权限过滤的边界。",
                "CNBody",
            ),
            data_table(
                ["阶段", "处理逻辑", "落地实现", "可验证结果"],
                [
                    ("查询构建", "从任务目标提取主题、对象和时间范围", "query + limit 参数", "检索请求包含明确查询词"),
                    ("候选召回", "匹配标题、类型、正文和关键词", "本地知识库评分排序", "返回命中结果或默认知识"),
                    ("上下文筛选", "控制返回条数与内容长度", "limit 1–5，返回摘要结构", "不把完整知识库注入模型"),
                    ("来源绑定", "将文档 ID、标题、类型写入结果", "sources 字段", "回答下方可查看来源"),
                    ("权限边界", "按企业权限与文档范围控制", "比赛版使用演示知识空间", "敏感文档不进入外部模型上下文"),
                ],
                widths=[70, 190, 150, CONTENT_WIDTH - 410],
            ),
            Spacer(1, 12),
            paragraph("5.5.2 知识引用与可信回答", "CNH2"),
            bullet("<b>来源可追溯：</b>回答只引用工具返回的文档标题和类型，不伪造不存在的页面。"),
            bullet("<b>事实优先级：</b>涉及运营指标时必须读取指标工具，涉及制度或产品说明时必须检索知识库。"),
            bullet("<b>权限最小化：</b>只将命中片段和目标上下文发送给模型，不发送整库内容。"),
            bullet("<b>可替换性：</b>演示知识库可按相同返回结构替换为向量检索或企业检索服务。"),
            info_callout(
                "知识库目标",
                "让 Agent 的结论有来源、可核验，并能在企业真实权限边界内工作，而不是依赖模型记忆生成内部事实。",
                "blue",
            ),
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
            paragraph("5.7 安全、隐私与权限实现", "CNH2"),
            paragraph(
                "NEXA 的安全边界分为密钥安全、工具安全、知识安全和写操作安全四层。比赛版本不依赖前端保存敏感信息，"
                "所有模型调用和工具执行都经过服务端统一入口。",
                "CNBody",
            ),
            data_table(
                ["安全层", "风险", "实现措施", "验证方式"],
                [
                    ("模型密钥", "Key 暴露到浏览器或 Git", "只读服务端环境变量，.env 加入 .gitignore", "检查仓库不存在 .env"),
                    ("工具执行", "模型调用任意能力或代码", "白名单注册、参数 Schema、未知工具拒绝", "未知工具返回错误"),
                    ("知识数据", "整库或敏感文档进入模型", "最小命中片段、来源限定、权限过滤预留", "检查 tool result 结构"),
                    ("写操作", "未经确认发送或创建任务", "提示词约束、待审核状态、人工确认", "未确认时不执行后续动作"),
                    ("运行审计", "无法定位失败或越权", "记录发起人、节点、参数摘要和状态", "展开运行记录可追溯"),
                    ("网络访问", "模型或外部接口异常", "35 秒超时、错误降级、演示模式", "断网或无 Key 仍可演示"),
                ],
                widths=[70, 130, 205, CONTENT_WIDTH - 405],
            ),
            Spacer(1, 12),
            info_callout(
                "写操作边界",
                "创建任务和发送通知属于写操作，只在用户明确要求或人工审核通过后执行；运行记录保留调用状态，不以模型文本替代真实工具结果。",
                "amber",
            ),
            Spacer(1, 10),
            paragraph("5.7.1 个人与企业数据保护", "CNH2"),
            bullet("公开仓库不包含真实 API Key、访问令牌、Cookie 或企业凭据。"),
            bullet("演示数据使用虚构企业、人员和指标，不来自真实客户数据。"),
            bullet("工具返回内容只保留执行所需摘要，日志避免记录完整密钥和隐私字段。"),
            bullet("后续接入真实系统时应增加 OAuth、RBAC、审计留存和敏感字段脱敏。"),
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
            paragraph("6.4 测试用例与验收结果", "CNH2"),
            data_table(
                ["测试用例", "前置条件", "操作步骤", "预期结果", "当前结果"],
                [
                    ("周报任务", "服务已启动，演示模式可用", "打开对话，点击生成运营周报", "出现计划、指标、知识和来源", "通过"),
                    ("连续追问", "已生成首轮回答", "输入“按优先级排序”并发送", "保留上下文并生成第二轮回答", "通过"),
                    ("工作流运行", "进入工作流页面", "点击运行工作流，等待节点完成", "节点完成、日志新增、运行记录新增", "通过"),
                    ("人工审核", "存在待审核任务", "点击审核结果", "任务进入已完成并显示成功提示", "通过"),
                    ("知识上传", "进入知识库", "上传 txt 文件", "文档列表增加并显示解析状态", "通过"),
                    ("工具开关", "进入工具连接", "切换飞书启用状态", "状态改变并出现反馈", "通过"),
                    ("移动端导航", "390 × 844 视口", "点击菜单并打开导航抽屉", "侧栏可见、页面无横向溢出", "通过"),
                    ("模型降级", "未配置 LLM Key", "发送任意任务", "返回演示模式结构化结果", "通过"),
                ],
                widths=[72, 100, 140, 125, CONTENT_WIDTH - 437],
            ),
            Spacer(1, 12),
            paragraph("6.5 部署拓扑与运行环境", "CNH2"),
            data_table(
                ["层级", "部署组件", "职责", "环境要求"],
                [
                    ("客户端", "浏览器", "页面渲染、用户交互、状态展示", "Chrome / Edge / Firefox / Safari"),
                    ("静态服务", "Node.js HTTP Server", "提供 HTML、CSS、JS 和 API", "Node.js 20+"),
                    ("Agent Gateway", "server.mjs", "模型代理、工具调用、降级", "服务端环境变量"),
                    ("模型服务", "OpenAI 兼容接口", "推理与 Tool Calling", "LLM_BASE_URL / MODEL / KEY"),
                    ("企业工具", "知识、指标、任务、通知", "提供真实业务动作", "可按实际系统替换"),
                    ("可选容器", "Docker", "统一构建与部署", "Dockerfile 已提供"),
                ],
                widths=[75, 140, 180, CONTENT_WIDTH - 395],
            ),
            Spacer(1, 10),
            info_callout(
                "部署方案选择",
                "比赛演示优先使用无构建 Node.js 启动；在线评审可选用 Docker + 云平台，保持同一服务端入口和环境变量协议。",
                "violet",
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
            paragraph("7.2.1 创新点验证矩阵", "CNH2"),
            data_table(
                ["创新点", "解决的问题", "产品证据与验证方式"],
                [
                    ("Agent 过程可视化", "用户无法判断 AI 是否真的执行了任务", "执行计划、工具轨迹、来源和耗时；通过真实对话截图与轨迹展开验证"),
                    ("对话与工作流统一", "一次性探索与稳定复用割裂", "对话结果可转任务，工作流可运行；通过周报从对话到自动化的完整流程验证"),
                    ("运行级可观测性", "失败后只能看到笼统报错", "节点轨迹、失败阶段与重试入口；通过失败运行记录展开验证"),
                    ("真模型 + 演示双模式", "现场网络或模型不稳定", "LLM / DEMO / DEMO-FALLBACK 三种状态；通过无 Key 或断网场景验证"),
                    ("写操作人工审核", "自动化越权执行高风险动作", "待审核任务和人工确认门禁；通过未确认不发送的用例验证"),
                ],
                widths=[115, 190, CONTENT_WIDTH - 305],
            ),
            PageBreak(),
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
