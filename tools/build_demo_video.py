from __future__ import annotations

import subprocess
import shutil
import sys
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp" / "video"
CAPTURES = WORK / "captures"
SEGMENTS = WORK / "segments"
AUDIO = WORK / "audio"
SLIDES = WORK / "slides"
OUTPUT_DIR = ROOT / "output" / "video"

for directory in (SEGMENTS, AUDIO, SLIDES, OUTPUT_DIR):
    directory.mkdir(parents=True, exist_ok=True)

FFMPEG = Path(imageio_ffmpeg.get_ffmpeg_exe())
FONT_REG = Path(r"C:\Windows\Fonts\Deng.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\Dengb.ttf")
FONT_LIGHT = Path(r"C:\Windows\Fonts\Dengl.ttf")

WIDTH = 1920
HEIGHT = 1080

INK = "#17211F"
INK_SOFT = "#34413E"
MUTED = "#68746F"
MUTED_2 = "#8A948F"
BORDER = "#DFE5DF"
SURFACE = "#FFFFFF"
SURFACE_SOFT = "#F5F7F3"
MINT = "#0D9075"
MINT_BRIGHT = "#5CE0B5"
MINT_SOFT = "#E3F5EE"
CORAL = "#DF7546"
CORAL_SOFT = "#FBE9E0"
BLUE = "#3F78C5"
BLUE_SOFT = "#E9F0FA"
VIOLET = "#7163C7"
VIOLET_SOFT = "#EFEDFA"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size=size)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    max_width: int,
    font_obj: ImageFont.FreeTypeFont,
    fill: str,
    line_gap: int = 12,
) -> int:
    x, y = xy
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if draw.textlength(candidate, font=font_obj) > max_width and current:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap
    return y


def fit_image(image_path: Path, box: tuple[int, int, int, int]) -> tuple[Image.Image, tuple[int, int]]:
    image = Image.open(image_path).convert("RGB")
    bx, by, bw, bh = box
    ratio = min(bw / image.width, bh / image.height)
    size = (max(1, int(image.width * ratio)), max(1, int(image.height * ratio)))
    image = image.resize(size, Image.Resampling.LANCZOS)
    position = (bx + (bw - size[0]) // 2, by + (bh - size[1]) // 2)
    return image, position


def base_slide(section: str, title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), SURFACE)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, WIDTH, 7), fill=MINT)
    draw.rounded_rectangle((74, 44, 104, 74), radius=7, fill=MINT)
    draw.text((80, 49), "N", font=font(20, True), fill="#0B1A15")
    draw.text((118, 44), "NEXA", font=font(24, True), fill=INK)
    draw.text((119, 73), "AGENT WORKSPACE", font=font(11), fill=MUTED_2)

    draw.text((WIDTH - 530, 48), "传智杯 AI Web 网页开发挑战赛", font=font(15), fill=MUTED)
    draw.text((WIDTH - 530, 72), "NEXA Agent Workspace 演示视频", font=font(12), fill=MUTED_2)

    draw.text((78, 132), section, font=font(15, True), fill=MINT)
    draw.text((76, 159), title, font=font(42, True), fill=INK)
    draw.text((78, 216), subtitle, font=font(20), fill=MUTED)
    draw.line((78, 252, 1842, 252), fill=BORDER, width=2)
    return canvas, draw


def screenshot_slide(
    index: int,
    section: str,
    title: str,
    subtitle: str,
    capture_name: str,
    caption: str,
) -> Path:
    canvas, draw = base_slide(section, title, subtitle)
    frame = (78, 283, 1764, 700)
    draw.rounded_rectangle(frame, radius=16, fill="#EEF1ED", outline=BORDER, width=2)
    image, position = fit_image(CAPTURES / capture_name, (90, 295, 1740, 676))
    draw.rounded_rectangle(
        (position[0] - 2, position[1] - 2, position[0] + image.width + 1, position[1] + image.height + 1),
        radius=4,
        outline="#BDC8C1",
        width=2,
    )
    canvas.paste(image, position)
    draw.text((78, 1002), caption, font=font(15), fill=MUTED)
    draw.text((1760, 1002), f"{index:02d}", font=font(15, True), fill=MINT)
    path = SLIDES / f"slide-{index:02d}.png"
    canvas.save(path)
    return path


def cover_slide() -> Path:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#101916")
    draw = ImageDraw.Draw(canvas)
    for x in range(0, WIDTH, 38):
        draw.line((x, 0, x, HEIGHT), fill="#15221E", width=1)
    for y in range(0, HEIGHT, 38):
        draw.line((0, y, WIDTH, y), fill="#15221E", width=1)
    for radius in (230, 310, 390):
        draw.ellipse(
            (WIDTH - radius - 40, -radius + 80, WIDTH + radius - 40, radius + 80),
            outline="#19332B",
            width=2,
        )
    draw.rounded_rectangle((96, 82, 146, 132), radius=10, fill=MINT_BRIGHT)
    draw.text((108, 91), "N", font=font(29, True), fill="#0A1A15")
    draw.text((166, 84), "NEXA", font=font(31, True), fill="#F4FBF8")
    draw.text((167, 123), "AGENT WORKSPACE", font=font(13), fill="#73827D")
    draw.text((96, 330), "传智杯 AI Web 网页开发挑战赛", font=font(22), fill="#8FA09A")
    draw.text((94, 377), "NEXA Agent Workspace", font=font(72, True), fill="#F5FCF9")
    draw.text((96, 464), "AI Agent 智能助手与自动化工作流平台", font=font(34), fill="#D2DDD8")
    draw.line((96, 534, 270, 534), fill=MINT_BRIGHT, width=3)
    draw.text((96, 570), "自主规划 · 工具调用 · 多轮对话 · 工作流编排", font=font(23), fill="#7E918A")
    draw.rounded_rectangle((96, 820, 1820, 940), radius=14, fill="#15231F", outline="#24362F", width=2)
    labels = [
        ("参赛团队", "NEXA Team"),
        ("项目形态", "Web + Node.js Agent Gateway"),
        ("运行模式", "真实模型 / 本地演示双模式"),
        ("文档版本", "V1.0"),
    ]
    for idx, (label, value) in enumerate(labels):
        x = 128 + (idx % 2) * 835
        y = 844 + (idx // 2) * 50
        draw.text((x, y), label, font=font(13), fill="#657873")
        draw.text((x, y + 21), value, font=font(20), fill="#E2ECE8")
    path = SLIDES / "slide-01.png"
    canvas.save(path)
    return path


def tech_slide(index: int) -> Path:
    canvas, draw = base_slide(
        "AI TECHNOLOGY",
        "真实大模型驱动的 Agent 执行链",
        "模型负责理解与生成，Gateway 负责工具选择、执行、轨迹和降级。",
    )
    boxes = [
        ("01", "接收任务", "多轮消息与企业上下文", BLUE_SOFT, BLUE, 110),
        ("02", "模型推理", "生成文本或 tool_calls", VIOLET_SOFT, VIOLET, 520),
        ("03", "工具执行", "白名单工具与结果校验", MINT_SOFT, MINT, 930),
        ("04", "结果交付", "回答、来源与执行轨迹", CORAL_SOFT, CORAL, 1340),
    ]
    for number, title, subtitle, background, accent, x in boxes:
        draw.rounded_rectangle((x, 360, x + 350, 565), radius=16, fill=background, outline="#D7DED8", width=2)
        draw.text((x + 28, 385), number, font=font(17, True), fill=accent)
        draw.text((x + 28, 425), title, font=font(31, True), fill=INK)
        draw_wrapped(draw, subtitle, (x + 28, 475), 290, font(19), MUTED, 6)
        if x < 1340:
            draw.line((x + 370, 462, x + 395, 462), fill="#AEBAB3", width=3)
            draw.polygon([(x + 395, 462), (x + 384, 456), (x + 384, 468)], fill="#AEBAB3")

    draw.rounded_rectangle((110, 635, 1810, 875), radius=16, fill="#14221E")
    code_lines = [
        "POST /api/agent/run",
        "messages + system prompt  ->  Chat Completions API",
        "tool_calls?  ->  execute whitelist tool  ->  append tool result",
        "final response + plan + toolTrace + sources",
    ]
    for line_index, line in enumerate(code_lines):
        draw.text((155, 682 + line_index * 43), line, font=font(20), fill="#BDE9D9" if line_index == 0 else "#DCE9E4")
    draw.text((110, 925), "最多四轮工具调用 · 35 秒超时 · 密钥仅存服务端 · 模型异常自动降级", font=font(21), fill=MUTED)
    path = SLIDES / f"slide-{index:02d}.png"
    canvas.save(path)
    return path


def innovation_slide(index: int) -> Path:
    canvas, draw = base_slide(
        "INNOVATION",
        "技术创新与应用创新",
        "让 AI 不仅能生成内容，还能完成可审核、可追溯的工作。",
    )
    cards = [
        ("过程可视化", "计划、工具、来源、状态和耗时全部可见", MINT_SOFT, MINT),
        ("对话 + 工作流", "探索任务与稳定复用形成一体化闭环", BLUE_SOFT, BLUE),
        ("运行可观测", "Token、耗时、失败节点与重试入口", VIOLET_SOFT, VIOLET),
        ("安全可控", "写操作确认、最小权限与人工审核", CORAL_SOFT, CORAL),
    ]
    positions = [(100, 345), (980, 345), (100, 610), (980, 610)]
    for (title, body, background, accent), (x, y) in zip(cards, positions):
        draw.rounded_rectangle((x, y, x + 820, y + 215), radius=18, fill=background, outline="#D7DED8", width=2)
        draw.line((x, y + 25, x, y + 190), fill=accent, width=5)
        draw.text((x + 34, y + 30), title, font=font(31, True), fill=INK)
        draw_wrapped(draw, body, (x + 34, y + 91), 730, font(21), MUTED, 8)
    draw.rounded_rectangle((100, 875, 1800, 970), radius=14, fill="#14221E")
    draw.text(
        (134, 910),
        "从目标输入到结果交付：可规划、可执行、可审核、可追溯",
        font=font(27, True),
        fill="#E7F4EF",
    )
    path = SLIDES / f"slide-{index:02d}.png"
    canvas.save(path)
    return path


def mobile_conclusion_slide(index: int) -> Path:
    canvas, draw = base_slide(
        "CONCLUSION",
        "面向真实工作的 AI Agent 工作台",
        "桌面端完整协作，移动端随时查看任务、运行状态与审核结果。",
    )
    image, position = fit_image(CAPTURES / "mobile.png", (120, 300, 410, 655))
    draw.rounded_rectangle(
        (position[0] - 6, position[1] - 6, position[0] + image.width + 5, position[1] + image.height + 5),
        radius=12,
        outline="#AEBDB5",
        width=3,
    )
    canvas.paste(image, position)

    items = [
        ("完整产品闭环", "工作台、对话、任务、工作流、知识库、工具与运行记录"),
        ("真实 Agent 能力", "OpenAI 兼容模型、原生 Tool Calling、多轮上下文"),
        ("比赛现场稳定", "无 Key 或无网络时自动进入本地演示模式"),
    ]
    y = 350
    for idx, (title, body) in enumerate(items):
        draw.rounded_rectangle((620, y, 1790, y + 170), radius=16, fill=SURFACE_SOFT, outline=BORDER, width=2)
        draw.text((660, y + 30), f"0{idx + 1}", font=font(18, True), fill=MINT)
        draw.text((710, y + 25), title, font=font(30, True), fill=INK)
        draw_wrapped(draw, body, (710, y + 83), 1010, font(20), MUTED, 6)
        y += 195
    draw.text((620, 960), "NEXA Team · 谢谢观看", font=font(21, True), fill=INK_SOFT)
    path = SLIDES / f"slide-{index:02d}.png"
    canvas.save(path)
    return path


SEGMENTS_DATA = [
    {
        "section": "INTRODUCTION",
        "title": "NEXA Agent Workspace",
        "subtitle": "基于大模型构建的 AI Agent 智能助手与自动化工作流平台。",
        "capture": "dashboard.png",
        "caption": "项目介绍 · 面向真实知识工作的 Agent 工作台",
        "narration": (
            "大家好，欢迎观看 NEXA Agent Workspace 项目演示。NEXA 是一个面向知识工作者的 AI Agent 工作台。"
            "用户只需要描述目标，Agent 就会完成任务理解、自主规划、企业知识检索、工具调用和结果交付。"
            "项目面向传智杯 AI Web 网页开发挑战赛，重点展示大模型、智能体规划、工具调用、多轮对话和自动化工作流能力。"
        ),
    },
    {
        "section": "WORKSPACE",
        "title": "把目标交给 Agent 团队",
        "subtitle": "从任务输入、实时执行到效率指标，一个界面掌握 Agent 工作状态。",
        "capture": "dashboard.png",
        "caption": "Agent 工作台 · 统一任务入口、执行状态与效率指标",
        "narration": (
            "首先是 Agent 工作台。顶部是任务入口，用户可以输入自然语言目标，也可以直接选择运营周报、竞品扫描、会议行动项等快捷任务。"
            "下方展示活跃 Agent、自动化任务、执行成功率和节省时间。智能体团队区域可以看到每个 Agent 的职责、运行次数和准确率。"
            "右侧实时执行面板展示当前任务进度，自动化工坊则把稳定的业务流程沉淀为可复用工作流。"
        ),
    },
    {
        "section": "AGENT CHAT",
        "title": "可观测的多轮智能对话",
        "subtitle": "执行计划、工具调用和知识来源完整呈现，结果可以被验证。",
        "capture": "chat.png",
        "caption": "智能对话 · 执行计划、工具轨迹、知识来源与结果操作",
        "narration": (
            "现在演示智能对话。我们点击生成运营周报，Agent 会先展示执行计划，然后调用项目指标工具读取活跃团队、激活率和留存数据，"
            "并检索增长运营手册和客户反馈知识。最终结果包含关键指标、业务洞察、下周建议和后续任务。"
            "下方可以展开每个工具的调用记录，也能查看参考来源。用户还可以继续追问，例如调整建议优先级，Agent 会保留上下文完成第二轮回答。"
        ),
    },
    {
        "section": "WORKFLOW",
        "title": "可视化自动化工作流",
        "subtitle": "从对话探索到稳定复用，节点、配置、运行和执行日志一体呈现。",
        "capture": "workflow.png",
        "caption": "工作流编排 · 六节点执行、节点配置与运行日志",
        "narration": (
            "一次性任务可以通过对话完成，稳定流程则进入工作流。这条运营周报自动化包含六个节点：手动触发、任务规划、知识检索、质量校验、生成交付物和发送飞书。"
            "节点支持拖拽、缩放和配置，右侧可以设置模型、超时、失败重试和人工审核。点击运行后，每个节点按顺序推进，颜色和状态实时变化，"
            "执行日志同步记录节点名称、结果和耗时。"
        ),
    },
    {
        "section": "TASK CENTER",
        "title": "任务闭环与人工审核",
        "subtitle": "Agent 负责执行，人负责判断关键动作，过程可控。",
        "capture": "tasks.png",
        "caption": "任务中心 · 待处理、进行中、等待审核和已完成",
        "narration": (
            "任务中心将 Agent 工作拆分为待处理、进行中、等待审核和已完成四个阶段。每张任务卡展示负责 Agent、负责人、截止时间和执行进度。"
            "涉及发送通知等关键动作时，任务会自动进入等待审核，人工确认后才继续。这样既保留自动化效率，也避免 AI 在未经确认时执行高风险写操作。"
        ),
    },
    {
        "section": "KNOWLEDGE & TOOLS",
        "title": "企业知识与工具连接",
        "subtitle": "让 Agent 基于可信知识工作，并把规划转化为真实动作。",
        "capture": "knowledge.png",
        "caption": "企业知识库 · 分类检索、引用统计与知识详情",
        "narration": (
            "企业知识库为 Agent 提供可信事实。文档可以分类、检索、上传和解析，每条回答都能显示引用来源。"
            "在工具连接页面，可以管理飞书、企业微信、Notion、GitHub、Webhook 和自定义 REST API 的授权与启停。"
            "工具连接配置调用上限、写操作确认和返回内容记录，保证 Agent 的能力边界清晰可管理。"
        ),
    },
    {
        "section": "OBSERVABILITY",
        "title": "运行记录与过程可追溯",
        "subtitle": "成功、耗时、Token、失败节点和恢复入口全部可见。",
        "capture": "runs.png",
        "caption": "运行可观测性 · 执行轨迹、用量、异常与重试",
        "narration": (
            "运行记录展示总运行次数、成功率、平均耗时和异常数量。展开一次运行，可以看到完整的执行轨迹，每一步都有状态和耗时。"
            "如果工具调用失败，界面会直接定位失败阶段，并提供重新运行入口。这样 AI 的执行结果不再是黑盒，而是可以审计和持续优化的工程过程。"
        ),
    },
    {
        "section": "AI TECHNOLOGY",
        "title": "真实大模型驱动的 Agent 执行链",
        "subtitle": "模型负责理解与生成，Gateway 负责工具选择、执行、轨迹和降级。",
        "slide_type": "tech",
        "caption": "AI 技术方案 · OpenAI 兼容模型与原生 Tool Calling",
        "narration": (
            "技术方案方面，NEXA 使用 OpenAI 兼容的 Chat Completions 接口作为模型抽象层，可以接入 DeepSeek、OpenAI 或企业私有模型。"
            "用户消息和系统提示词进入模型，当模型返回 tool_calls 时，Node 服务端会执行白名单工具，再把结构化结果写回上下文。"
            "系统最多执行四轮工具调用，并设置超时、输入长度限制和错误降级。提示词要求涉及企业事实时必须调用工具，写操作必须由用户明确要求。"
        ),
    },
    {
        "section": "INNOVATION",
        "title": "技术创新与应用创新",
        "subtitle": "将过程透明度、工作流复用和企业安全共同纳入产品设计。",
        "slide_type": "innovation",
        "caption": "项目创新 · 过程可视化、对话与工作流统一、运行可观测",
        "narration": (
            "NEXA 的创新点体现在三个方面。第一是 Agent 过程可视化，计划、工具、来源、状态和耗时都可以查看。"
            "第二是对话与工作流一体化，对话适合探索一次性任务，工作流适合稳定复用，任务中心负责人工审核。"
            "第三是真实模型与本地演示双模式，既保留大模型工具调用能力，也保证比赛现场在网络或模型异常时仍然可以完整展示。"
        ),
    },
    {
        "section": "CONCLUSION",
        "title": "从回答问题到完成工作",
        "subtitle": "NEXA 将大模型能力转化为可规划、可执行、可审核、可追溯的智能体工作台。",
        "slide_type": "conclusion",
        "caption": "总结 · 完整产品闭环、真实 Agent 能力与稳定演示",
        "narration": (
            "最后总结，NEXA 不只回答一个问题，而是把目标转化为可规划、可执行、可审核、可追溯的工作结果。"
            "项目具备完整 Web 产品、真实模型接入、工具调用循环、工作流编排和自动化测试，同时适配桌面端和移动端。"
            "感谢各位评审观看，NEXA Team 期待在传智杯 AI Web 网页开发挑战赛中展示更多可能。"
        ),
    },
]


def synth_wav(text: str, path: Path) -> float:
    text_path = path.with_suffix(".txt")
    text_path.write_text(text, encoding="utf-8")
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        raise RuntimeError("PowerShell is required for Windows speech synthesis")
    script = ROOT / "tools" / "tts_windows.ps1"
    subprocess.run(
        [
            shell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
            "-TextFile",
            str(text_path),
            "-OutputFile",
            str(path),
        ],
        check=True,
        capture_output=True,
    )
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def format_srt_time(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def split_caption(text: str, max_chars: int = 26) -> list[str]:
    clean = " ".join(text.replace("\n", "").split())
    parts: list[str] = []
    current = ""
    for char in clean:
        current += char
        if len(current) >= max_chars and char in "。，；！？":
            parts.append(current)
            current = ""
    if current:
        parts.append(current)
    if not parts:
        parts = [clean]
    return parts


def encode_segment(
    slide: Path,
    audio: Path | None,
    output: Path,
    duration: float,
) -> None:
    total_duration = duration + 0.7
    visual_filter = (
        "scale=1920:1080,format=yuv420p,"
        "fade=t=in:st=0:d=0.25,"
        f"fade=t=out:st={max(0, total_duration - 0.3):.3f}:d=0.3"
    )
    command = [
        str(FFMPEG),
        "-y",
        "-loop",
        "1",
        "-i",
        str(slide),
    ]
    if audio is None:
        command.extend(
            [
                "-f",
                "lavfi",
                "-i",
                "anullsrc=channel_layout=stereo:sample_rate=44100",
            ]
        )
    else:
        command.extend(["-i", str(audio)])
    command.extend(
        [
        "-t",
        f"{total_duration:.3f}",
        "-r",
        "30",
        "-vf",
        visual_filter,
        "-af",
        "adelay=250|250,apad=pad_dur=0.45",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-movflags",
        "+faststart",
        "-shortest",
        str(output),
        ]
    )
    subprocess.run(command, check=True, capture_output=True)


def main() -> None:
    if not CAPTURES.exists():
        raise SystemExit("Missing video captures. Run tools/capture_video_assets.py first.")

    for path in SEGMENTS.glob("*.mp4"):
        path.unlink()
    for path in AUDIO.glob("*.wav"):
        path.unlink()
    for path in SLIDES.glob("*.png"):
        path.unlink()

    tts_enabled = "--with-tts" in sys.argv
    srt_entries: list[str] = []
    voiceover_lines: list[str] = []
    concat_lines: list[str] = []
    timeline = 0.0

    for index, item in enumerate(SEGMENTS_DATA, start=1):
        slide_type = item.get("slide_type")
        if slide_type == "tech":
            slide = tech_slide(index)
        elif slide_type == "innovation":
            slide = innovation_slide(index)
        elif slide_type == "conclusion":
            slide = mobile_conclusion_slide(index)
        elif index == 1:
            slide = cover_slide()
        else:
            slide = screenshot_slide(
                index,
                item["section"],
                item["title"],
                item["subtitle"],
                item["capture"],
                item["caption"],
            )

        audio: Path | None = None
        if tts_enabled:
            audio = AUDIO / f"segment-{index:02d}.wav"
            try:
                duration = synth_wav(item["narration"], audio)
            except Exception as error:
                print(f"TTS unavailable for segment {index}: {error}")
                audio = None
                duration = max(28, min(55, len(item["narration"]) / 4.0 + 4))
        else:
            duration = max(28, min(55, len(item["narration"]) / 4.0 + 4))
        segment = SEGMENTS / f"segment-{index:02d}.mp4"
        encode_segment(slide, audio, segment, duration)
        concat_lines.append(f"file '{segment.as_posix()}'")
        voiceover_lines.append(
            f"[{format_srt_time(timeline)} - {format_srt_time(timeline + duration)}] "
            f"{item['title']}\n{item['narration']}\n"
        )

        captions = split_caption(item["narration"])
        char_total = sum(len(caption) for caption in captions) or 1
        cursor = timeline
        for caption_index, caption in enumerate(captions):
            share = duration * len(caption) / char_total
            srt_entries.append(
                f"{len(srt_entries) + 1}\n"
                f"{format_srt_time(cursor)} --> {format_srt_time(cursor + share)}\n"
                f"{caption}\n"
            )
            cursor += share
        timeline += duration + 0.7

    concat_file = WORK / "segments.txt"
    concat_file.write_text("\n".join(concat_lines), encoding="utf-8")
    suffix = "" if tts_enabled else "-字幕版"
    final_video = OUTPUT_DIR / f"NEXA-Agent-Workspace-演示视频{suffix}.mp4"
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(final_video),
        ],
        check=True,
        capture_output=True,
    )

    srt_path = OUTPUT_DIR / "NEXA-Agent-Workspace-演示字幕.srt"
    srt_path.write_text("\n".join(srt_entries), encoding="utf-8")
    voiceover_path = OUTPUT_DIR / "NEXA-Agent-Workspace-配音稿.txt"
    voiceover_path.write_text("\n".join(voiceover_lines), encoding="utf-8")
    print(f"VIDEO={final_video}")
    print(f"SRT={srt_path}")
    print(f"VOICEOVER={voiceover_path}")
    print(f"DURATION={timeline:.1f}s")


if __name__ == "__main__":
    main()
