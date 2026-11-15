(function () {
  "use strict";

  const icon = window.lucideIcon;
  const appMain = document.getElementById("appMain");
  const pageBreadcrumb = document.getElementById("pageBreadcrumb");
  const sidebar = document.getElementById("sidebar");
  const mobileScrim = document.getElementById("mobileScrim");
  const toastRegion = document.getElementById("toastRegion");
  const commandOverlay = document.getElementById("commandOverlay");
  const commandInput = document.getElementById("commandInput");
  const commandResults = document.getElementById("commandResults");
  const notificationPopover = document.getElementById("notificationPopover");

  const VIEW_META = {
    dashboard: { title: "工作台", eyebrow: "Workspace overview" },
    chat: { title: "智能对话", eyebrow: "Agent conversation" },
    tasks: { title: "任务中心", eyebrow: "Task orchestration" },
    workflow: { title: "工作流", eyebrow: "Automation builder" },
    knowledge: { title: "知识库", eyebrow: "Enterprise knowledge" },
    tools: { title: "工具连接", eyebrow: "Connected tools" },
    runs: { title: "运行记录", eyebrow: "Execution observability" }
  };

  const NAV_ITEMS = [
    { view: "dashboard", label: "工作台", icon: "layout-dashboard", keywords: "首页 总览 overview" },
    { view: "chat", label: "智能对话", icon: "message-square", keywords: "agent 对话 chat" },
    { view: "tasks", label: "任务中心", icon: "list-checks", keywords: "任务 task 进度" },
    { view: "workflow", label: "工作流", icon: "workflow", keywords: "自动化 编排 automation" },
    { view: "knowledge", label: "知识库", icon: "book-open", keywords: "文档 知识 rag" },
    { view: "tools", label: "工具连接", icon: "plug", keywords: "飞书 微信 api 集成" },
    { view: "runs", label: "运行记录", icon: "activity", keywords: "日志 执行 trace" }
  ];

  const AGENTS = [
    {
      id: "ops",
      name: "运营周报官",
      description: "汇总指标、提炼洞察并生成周报",
      icon: "chart-column",
      tone: "mint",
      status: "ready",
      runs: 46,
      accuracy: "98.2%"
    },
    {
      id: "radar",
      name: "竞品雷达",
      description: "追踪市场动态并生成竞争情报",
      icon: "target",
      tone: "coral",
      status: "running",
      runs: 28,
      accuracy: "96.8%"
    },
    {
      id: "meeting",
      name: "会议行动助手",
      description: "提炼纪要、识别决策并跟进任务",
      icon: "users",
      tone: "blue",
      status: "ready",
      runs: 34,
      accuracy: "99.1%"
    },
    {
      id: "support",
      name: "客户洞察官",
      description: "聚类反馈、识别风险与产品机会",
      icon: "brain",
      tone: "violet",
      status: "ready",
      runs: 18,
      accuracy: "97.4%"
    }
  ];

  const INITIAL_CONVERSATIONS = [
    {
      id: "conv-weekly",
      title: "本周产品运营周报",
      agent: "运营周报官",
      time: "10:42",
      messages: []
    },
    {
      id: "conv-competitor",
      title: "AI Agent 竞品动向分析",
      agent: "竞品雷达",
      time: "昨天",
      messages: []
    },
    {
      id: "conv-meeting",
      title: "产品评审会行动项",
      agent: "会议行动助手",
      time: "周三",
      messages: []
    }
  ];

  const INITIAL_DOCS = [
    {
      id: "kb-growth-playbook",
      title: "2026 Q4 增长运营手册",
      type: "策略文档",
      typeKey: "strategy",
      updated: "11 月 12 日",
      owner: "林默",
      chunks: 42,
      references: 186,
      summary: "Q4 北极星指标、增长抓手、渠道质量评估与周报规范。"
    },
    {
      id: "kb-product-release",
      title: "Agent Studio 2.4 发布说明",
      type: "产品文档",
      typeKey: "product",
      updated: "11 月 10 日",
      owner: "陈曦",
      chunks: 28,
      references: 94,
      summary: "工作流版本管理、人工审批、运行回放与新增工具连接。"
    },
    {
      id: "kb-competitor",
      title: "AI Agent 产品竞品追踪",
      type: "市场情报",
      typeKey: "market",
      updated: "11 月 13 日",
      owner: "周青",
      chunks: 56,
      references: 231,
      summary: "多 Agent 协作、可视化编排、权限审计与工具生态追踪。"
    },
    {
      id: "kb-customer-voice",
      title: "客户反馈主题聚类（11 月）",
      type: "客户洞察",
      typeKey: "insight",
      updated: "11 月 11 日",
      owner: "林默",
      chunks: 36,
      references: 172,
      summary: "高频反馈、情绪趋势、客户原声与产品机会主题聚类。"
    },
    {
      id: "kb-security",
      title: "企业数据安全与权限规范",
      type: "制度规范",
      typeKey: "policy",
      updated: "10 月 28 日",
      owner: "安全中心",
      chunks: 19,
      references: 61,
      summary: "知识库权限、敏感数据边界、工具调用审计与发布审批。"
    }
  ];

  const TOOL_CONNECTIONS = [
    {
      id: "feishu",
      name: "飞书",
      description: "消息通知、文档读写、审批与日历",
      icon: "message-square",
      tone: "blue",
      category: "协作",
      connected: true,
      enabled: true,
      account: "星云科技 · 飞书"
    },
    {
      id: "wecom",
      name: "企业微信",
      description: "群机器人通知与内部应用消息",
      icon: "users",
      tone: "mint",
      category: "协作",
      connected: true,
      enabled: true,
      account: "星云科技 · 企微"
    },
    {
      id: "notion",
      name: "Notion",
      description: "知识页面同步与数据库条目写入",
      icon: "file-text",
      tone: "ink",
      category: "知识",
      connected: true,
      enabled: false,
      account: "产品知识空间"
    },
    {
      id: "github",
      name: "GitHub",
      description: "读取 Issue、PR 与发布记录",
      icon: "git-branch",
      tone: "violet",
      category: "研发",
      connected: true,
      enabled: true,
      account: "nexa-product"
    },
    {
      id: "webhook",
      name: "Webhook",
      description: "通过 HTTP 回调连接内部系统",
      icon: "webhook",
      tone: "coral",
      category: "开放接口",
      connected: true,
      enabled: true,
      account: "3 个端点运行中"
    },
    {
      id: "rest",
      name: "自定义 REST API",
      description: "为 Agent 封装企业私有能力",
      icon: "code",
      tone: "sand",
      category: "开放接口",
      connected: false,
      enabled: false,
      account: "尚未配置"
    }
  ];

  const INITIAL_RUNS = [
    {
      id: "RUN-2F91A",
      name: "生成产品运营周报",
      agent: "运营周报官",
      trigger: "手动触发",
      status: "success",
      duration: "38.2s",
      tokens: "12.4k",
      time: "今天 10:42",
      steps: [
        ["读取项目指标", "已完成 · 1.2s"],
        ["检索企业知识", "已完成 · 2.8s"],
        ["生成结构化周报", "已完成 · 31.4s"],
        ["创建后续任务", "已完成 · 2.8s"]
      ]
    },
    {
      id: "RUN-8C31D",
      name: "竞品动态每日扫描",
      agent: "竞品雷达",
      trigger: "定时任务",
      status: "running",
      duration: "21.7s",
      tokens: "8.1k",
      time: "今天 10:30",
      steps: [
        ["抓取市场信息", "已完成 · 8.4s"],
        ["筛选高相关信号", "进行中 · 13.3s"],
        ["生成情报摘要", "等待中"]
      ]
    },
    {
      id: "RUN-4A72E",
      name: "客户反馈周度聚类",
      agent: "客户洞察官",
      trigger: "Webhook",
      status: "success",
      duration: "52.6s",
      tokens: "18.7k",
      time: "今天 09:16",
      steps: [
        ["同步客户反馈", "已完成 · 10.2s"],
        ["主题聚类", "已完成 · 28.9s"],
        ["识别风险信号", "已完成 · 8.3s"],
        ["写入知识库", "已完成 · 5.2s"]
      ]
    },
    {
      id: "RUN-7D10B",
      name: "产品评审会纪要分发",
      agent: "会议行动助手",
      trigger: "日历事件",
      status: "review",
      duration: "43.9s",
      tokens: "9.6k",
      time: "昨天 17:28",
      steps: [
        ["读取会议转写", "已完成 · 7.1s"],
        ["提炼决策与行动项", "已完成 · 30.2s"],
        ["发送至项目群", "等待人工确认"]
      ]
    },
    {
      id: "RUN-3B84F",
      name: "新用户激活分析",
      agent: "运营周报官",
      trigger: "手动触发",
      status: "failed",
      duration: "12.3s",
      tokens: "4.2k",
      time: "昨天 15:04",
      steps: [
        ["读取项目指标", "已完成 · 1.1s"],
        ["调用数据仓库", "失败 · 权限已过期"],
        ["生成分析结论", "已终止"]
      ]
    }
  ];

  const TASKS = [
    {
      id: "TASK-2841",
      title: "完成本周产品运营周报",
      description: "汇总活跃、激活、留存与渠道数据，生成管理层周报。",
      agent: "运营周报官",
      owner: "林默",
      due: "今天 16:00",
      column: "doing",
      progress: 72,
      tone: "mint",
      icon: "chart-column"
    },
    {
      id: "TASK-2838",
      title: "竞品动态每日扫描",
      description: "追踪 8 个重点竞品的产品更新与市场动作。",
      agent: "竞品雷达",
      owner: "周青",
      due: "今天 18:00",
      column: "doing",
      progress: 46,
      tone: "coral",
      icon: "target"
    },
    {
      id: "TASK-2836",
      title: "产品评审会纪要分发",
      description: "行动项已整理，等待确认后发送至项目群。",
      agent: "会议行动助手",
      owner: "陈曦",
      due: "今天 14:30",
      column: "review",
      progress: 88,
      tone: "blue",
      icon: "users"
    },
    {
      id: "TASK-2832",
      title: "客户反馈主题聚类",
      description: "对 286 条反馈进行主题聚类与风险识别。",
      agent: "客户洞察官",
      owner: "林默",
      due: "今天 20:00",
      column: "backlog",
      progress: 0,
      tone: "violet",
      icon: "brain"
    },
    {
      id: "TASK-2829",
      title: "整理 Agent Studio 2.4 发布 Q&A",
      description: "根据发布说明与客户问题生成内部答疑文档。",
      agent: "客户洞察官",
      owner: "陈曦",
      due: "明天 12:00",
      column: "backlog",
      progress: 0,
      tone: "violet",
      icon: "file-text"
    },
    {
      id: "TASK-2814",
      title: "11 月增长渠道复盘",
      description: "已生成渠道质量对比与预算调整建议。",
      agent: "运营周报官",
      owner: "周青",
      due: "已完成",
      column: "done",
      progress: 100,
      tone: "mint",
      icon: "chart-column"
    }
  ];

  const WORKFLOW_NODES = [
    {
      id: "trigger",
      type: "trigger",
      index: "01",
      title: "手动触发",
      description: "接收任务目标",
      icon: "play",
      x: 32,
      y: 208,
      status: "idle"
    },
    {
      id: "planner",
      type: "agent",
      index: "02",
      title: "任务规划",
      description: "拆解目标与交付标准",
      icon: "brain",
      x: 240,
      y: 208,
      status: "idle"
    },
    {
      id: "knowledge",
      type: "tool",
      index: "03",
      title: "知识检索",
      description: "读取指标与内部文档",
      icon: "database",
      x: 448,
      y: 208,
      status: "idle"
    },
    {
      id: "review",
      type: "condition",
      index: "04",
      title: "质量校验",
      description: "事实、格式与敏感信息",
      icon: "shield-check",
      x: 656,
      y: 208,
      status: "idle"
    },
    {
      id: "writer",
      type: "agent",
      index: "05",
      title: "生成交付物",
      description: "输出结构化周报",
      icon: "file-text",
      x: 864,
      y: 208,
      status: "idle"
    },
    {
      id: "notify",
      type: "tool",
      index: "06",
      title: "发送至飞书",
      description: "同步负责人并归档",
      icon: "send",
      x: 1072,
      y: 208,
      status: "idle"
    }
  ];

  const state = {
    view: "dashboard",
    mode: "demo",
    conversations: INITIAL_CONVERSATIONS.map((item) => ({ ...item, messages: [] })),
    activeConversationId: "conv-weekly",
    chatInput: "",
    generating: false,
    generationToken: 0,
    docs: INITIAL_DOCS.map((item) => ({ ...item })),
    docQuery: "",
    docType: "全部",
    selectedDocId: "kb-growth-playbook",
    tools: TOOL_CONNECTIONS.map((item) => ({ ...item })),
    toolQuery: "",
    toolCategory: "全部",
    runs: INITIAL_RUNS.map((run) => ({ ...run, steps: run.steps.map((step) => [...step]) })),
    runFilter: "all",
    expandedRunId: null,
    tasks: TASKS.map((item) => ({ ...item })),
    taskFilter: "all",
    workflow: {
      name: "运营周报自动化",
      version: "v2.4",
      nodes: WORKFLOW_NODES.map((node) => ({ ...node })),
      selectedNodeId: "planner",
      zoom: 1,
      running: false,
      runIndex: -1,
      logs: []
    },
    paletteIndex: 0,
    paletteItems: []
  };

  // Render text through a small safe subset instead of injecting model HTML.
  function escapeHTML(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function inlineMarkdown(value) {
    return escapeHTML(value)
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/`(.+?)`/g, "<code>$1</code>");
  }

  function formatMessage(text) {
    const lines = String(text || "").split(/\r?\n/);
    const output = [];
    let listType = "";

    const closeList = () => {
      if (listType) {
        output.push(`</${listType}>`);
        listType = "";
      }
    };

    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line) {
        closeList();
        continue;
      }

      if (line.startsWith("### ")) {
        closeList();
        output.push(`<h4>${inlineMarkdown(line.slice(4))}</h4>`);
        continue;
      }
      if (line.startsWith("## ")) {
        closeList();
        output.push(`<h3>${inlineMarkdown(line.slice(3))}</h3>`);
        continue;
      }
      if (/^[-•]\s+/.test(line)) {
        if (listType !== "ul") {
          closeList();
          output.push("<ul>");
          listType = "ul";
        }
        output.push(`<li>${inlineMarkdown(line.replace(/^[-•]\s+/, ""))}</li>`);
        continue;
      }
      if (/^\d+\.\s+/.test(line)) {
        if (listType !== "ol") {
          closeList();
          output.push("<ol>");
          listType = "ol";
        }
        output.push(`<li>${inlineMarkdown(line.replace(/^\d+\.\s+/, ""))}</li>`);
        continue;
      }

      closeList();
      output.push(`<p>${inlineMarkdown(line)}</p>`);
    }

    closeList();
    return output.join("");
  }

  function hydrateIcons(root) {
    (root || document).querySelectorAll("[data-icon]").forEach((element) => {
      element.innerHTML = icon(element.dataset.icon, 18);
    });
  }

  function setView(view, options) {
    if (!VIEW_META[view]) return;
    state.view = view;
    pageBreadcrumb.textContent = VIEW_META[view].title;
    document.querySelectorAll(".nav-item[data-view]").forEach((button) => {
      button.classList.toggle("active", button.dataset.view === view);
    });
    renderView();
    appMain.scrollTop = 0;
    closeSidebar();
    closePopovers();

    if (!options?.silent) {
      history.replaceState(null, "", `#${view}`);
    }
  }

  function renderView() {
    const renderers = {
      dashboard: renderDashboard,
      chat: renderChat,
      tasks: renderTasks,
      workflow: renderWorkflow,
      knowledge: renderKnowledge,
      tools: renderTools,
      runs: renderRuns
    };
    appMain.innerHTML = renderers[state.view]();
    hydrateIcons(appMain);

    if (state.view === "chat") {
      requestAnimationFrame(() => {
        scrollChatToBottom(false);
        const input = document.getElementById("chatComposerInput");
        if (input && window.innerWidth > 720) input.focus({ preventScroll: true });
      });
    }

    if (state.view === "workflow") {
      requestAnimationFrame(drawWorkflowEdges);
    }
  }

  function pageHeading({ eyebrow, title, subtitle, actions, compact }) {
    return `
      <div class="page-heading ${compact ? "is-compact" : ""}">
        <div>
          ${eyebrow ? `<span class="page-eyebrow">${escapeHTML(eyebrow)}</span>` : ""}
          <h1>${title}</h1>
          ${subtitle ? `<p>${subtitle}</p>` : ""}
        </div>
        ${actions ? `<div class="heading-actions">${actions}</div>` : ""}
      </div>
    `;
  }

  function statusDot(label, tone) {
    return `<span class="status-pill ${tone || ""}"><i></i>${escapeHTML(label)}</span>`;
  }

  function renderDashboard() {
    const stats = [
      {
        label: "活跃 Agent",
        value: "4",
        change: "+1",
        note: "本周新增",
        icon: "bot",
        tone: "mint",
        chart: "M2 24 C8 22, 9 14, 16 17 S27 7, 34 11 S43 2, 54 5"
      },
      {
        label: "本周自动化任务",
        value: "126",
        change: "+24%",
        note: "较上周",
        icon: "zap",
        tone: "coral",
        chart: "M2 25 C10 25, 10 22, 16 22 S23 13, 29 16 S35 10, 40 12 S48 4, 54 7"
      },
      {
        label: "执行成功率",
        value: "98.7%",
        change: "+1.2%",
        note: "近 7 天",
        icon: "gauge",
        tone: "blue",
        chart: "M2 22 C9 21, 11 17, 17 18 S25 15, 31 16 S40 11, 47 12 S51 7, 54 8"
      },
      {
        label: "本月节省时间",
        value: "18.6h",
        change: "+3.4h",
        note: "较上月",
        icon: "clock",
        tone: "violet",
        chart: "M2 26 C7 24, 11 25, 15 21 S22 22, 27 16 S35 18, 40 11 S49 10, 54 4"
      }
    ];

    return `
      <div class="view dashboard-view">
        ${pageHeading({
          eyebrow: "FRIDAY, 14 NOV · LIVE WORKSPACE",
          title: "上午好，林默",
          subtitle: "你的 Agent 团队正在处理 <strong>3 项任务</strong>，本周已为你节省 <strong>18.6 小时</strong>。",
          actions: `
            <button class="secondary-button" type="button" data-view="runs"><span data-icon="activity"></span>查看运行报告</button>
            <button class="primary-button" type="button" data-action="create-agent"><span data-icon="plus"></span>创建 Agent</button>
          `
        })}

        <section class="command-deck" aria-label="Agent 任务输入">
          <div class="command-grid-pattern"></div>
          <div class="command-deck-head">
            <div class="command-agent">
              <span class="command-avatar">${icon("sparkles", 22)}</span>
              <div>
                <span class="command-overline"><i></i> NEXA Agent 已就绪</span>
                <h2>今天，交给 Agent 做什么？</h2>
              </div>
            </div>
            <div class="command-capabilities">
              <span><i>01</i> 自主规划</span>
              <span><i>02</i> 工具调用</span>
              <span><i>03</i> 结果交付</span>
            </div>
          </div>
          <form class="command-form" data-form="dashboard-command">
            <span class="command-input-icon" data-icon="sparkles"></span>
            <input
              id="dashboardCommandInput"
              name="prompt"
              autocomplete="off"
              placeholder="描述目标，Agent 会自动拆解任务、调用工具并交付结果..."
              aria-label="任务描述"
            />
            <button class="voice-button" type="button" aria-label="语音输入" data-action="voice">
              <span data-icon="mic"></span>
            </button>
            <button class="command-submit" type="submit" aria-label="开始执行">
              <span data-icon="arrow-up"></span>
            </button>
          </form>
          <div class="prompt-suggestions">
            <span class="suggestion-label">试试</span>
            <button type="button" data-prompt="生成本周产品运营周报，汇总活跃、激活、留存和渠道表现">生成运营周报</button>
            <button type="button" data-prompt="分析最近一周 AI Agent 竞品动态，提炼市场机会和风险">扫描竞品动态</button>
            <button type="button" data-prompt="整理产品评审会的决策和行动项，并分配给负责人">整理会议行动项</button>
            <button type="button" data-prompt="分析 11 月客户反馈，提炼高频问题和产品机会">聚类客户反馈</button>
          </div>
        </section>

        <div class="stats-grid">
          ${stats
            .map(
              (stat) => `
                <article class="stat-card">
                  <div class="stat-top">
                    <span class="stat-icon ${stat.tone}" data-icon="${stat.icon}"></span>
                    <svg class="stat-spark" viewBox="0 0 56 30" aria-hidden="true">
                      <path d="${stat.chart}" />
                    </svg>
                  </div>
                  <div class="stat-value">${stat.value}</div>
                  <div class="stat-meta">
                    <span>${stat.label}</span>
                    <strong>${stat.change}</strong>
                    <small>${stat.note}</small>
                  </div>
                </article>
              `
            )
            .join("")}
        </div>

        <div class="dashboard-columns">
          <section class="panel agent-team-panel">
            <div class="panel-heading">
              <div>
                <span class="section-kicker">AGENT TEAM</span>
                <h2>智能体团队</h2>
              </div>
              <button class="text-button" type="button" data-action="manage-agents">管理全部 <span data-icon="arrow-right"></span></button>
            </div>
            <div class="agent-cards">
              ${AGENTS.map(
                (agent) => `
                  <button class="agent-card" type="button" data-action="open-agent" data-agent-id="${agent.id}">
                    <span class="agent-icon ${agent.tone}" data-icon="${agent.icon}"></span>
                    <span class="agent-main">
                      <span class="agent-name-row">
                        <strong>${agent.name}</strong>
                        ${agent.status === "running" ? statusDot("运行中", "running") : statusDot("已就绪", "ready")}
                      </span>
                      <span class="agent-description">${agent.description}</span>
                      <span class="agent-metrics">
                        <span><b>${agent.runs}</b> 本月运行</span>
                        <span><b>${agent.accuracy}</b> 准确率</span>
                      </span>
                    </span>
                    <span class="agent-arrow" data-icon="arrow-right"></span>
                  </button>
                `
              ).join("")}
            </div>
          </section>

          <aside class="panel live-run-panel">
            <div class="panel-heading">
              <div>
                <span class="section-kicker">LIVE EXECUTION</span>
                <h2>实时执行</h2>
              </div>
              ${statusDot("LIVE", "live")}
            </div>
            <div class="live-run-agent">
              <span class="agent-icon coral" data-icon="target"></span>
              <div>
                <strong>竞品动态每日扫描</strong>
                <span>竞品雷达 · 已运行 21.7 秒</span>
              </div>
              <button class="icon-button small" type="button" data-view="workflow" aria-label="打开工作流">
                <span data-icon="maximize"></span>
              </button>
            </div>
            <div class="live-timeline">
              <div class="live-step done">
                <span class="timeline-marker" data-icon="check"></span>
                <div><strong>抓取市场信息</strong><small>读取 18 个信息源</small></div>
                <span>8.4s</span>
              </div>
              <div class="live-step active">
                <span class="timeline-marker" data-icon="loader-circle"></span>
                <div><strong>筛选高相关信号</strong><small>正在评估信息可信度</small></div>
                <span>13.3s</span>
              </div>
              <div class="live-step pending">
                <span class="timeline-marker" data-icon="sparkles"></span>
                <div><strong>生成情报摘要</strong><small>等待上一步完成</small></div>
                <span>—</span>
              </div>
            </div>
            <div class="live-progress">
              <div><span>当前进度</span><strong>46%</strong></div>
              <div class="progress-track"><span style="width: 46%"></span></div>
            </div>
          </aside>
        </div>

        <div class="dashboard-columns lower">
          <section class="panel workflow-preview-panel">
            <div class="panel-heading">
              <div>
                <span class="section-kicker">AUTOMATION</span>
                <h2>运营周报自动化</h2>
              </div>
              <div class="heading-inline">
                ${statusDot("已发布 · v2.4", "ready")}
                <button class="icon-button small" type="button" data-view="workflow" aria-label="打开工作流编辑器">
                  <span data-icon="arrow-up-right"></span>
                </button>
              </div>
            </div>
            <div class="workflow-mini">
              <div class="mini-node mint"><span data-icon="play"></span><div><strong>手动触发</strong><small>接收目标</small></div></div>
              <span class="mini-connector"></span>
              <div class="mini-node violet"><span data-icon="brain"></span><div><strong>任务规划</strong><small>拆解步骤</small></div></div>
              <span class="mini-connector"></span>
              <div class="mini-node blue"><span data-icon="database"></span><div><strong>知识检索</strong><small>读取数据</small></div></div>
              <span class="mini-connector"></span>
              <div class="mini-node coral"><span data-icon="send"></span><div><strong>发送周报</strong><small>飞书通知</small></div></div>
            </div>
            <div class="workflow-meta">
              <span><span data-icon="clock"></span> 每周五 10:00 自动运行</span>
              <span><span data-icon="zap"></span> 平均 38 秒完成</span>
              <span><span data-icon="circle-check"></span> 本周成功 3 / 3 次</span>
            </div>
          </section>

          <section class="panel recent-activity-panel">
            <div class="panel-heading">
              <div>
                <span class="section-kicker">RECENT ACTIVITY</span>
                <h2>最近动态</h2>
              </div>
              <button class="text-button" type="button" data-view="runs">全部记录 <span data-icon="arrow-right"></span></button>
            </div>
            <div class="activity-list">
              <button class="activity-row" type="button" data-view="runs">
                <span class="activity-icon success" data-icon="file-text"></span>
                <span><strong>产品运营周报已交付</strong><small>运营周报官 · 2 分钟前</small></span>
                <span class="activity-tag">已完成</span>
              </button>
              <button class="activity-row" type="button" data-view="knowledge">
                <span class="activity-icon info" data-icon="book-open"></span>
                <span><strong>新增 3 篇知识文档</strong><small>林默 · 18 分钟前</small></span>
                <span class="activity-tag neutral">知识库</span>
              </button>
              <button class="activity-row" type="button" data-view="tasks">
                <span class="activity-icon review" data-icon="clock"></span>
                <span><strong>会议纪要等待人工确认</strong><small>会议行动助手 · 36 分钟前</small></span>
                <span class="activity-tag warning">待审核</span>
              </button>
            </div>
          </section>
        </div>
      </div>
    `;
  }

  function getActiveConversation() {
    return (
      state.conversations.find((conversation) => conversation.id === state.activeConversationId) ||
      state.conversations[0]
    );
  }

  function renderChatConversationList() {
    return state.conversations
      .map(
        (conversation) => `
          <button
            class="conversation-item ${conversation.id === state.activeConversationId ? "active" : ""}"
            type="button"
            data-action="select-conversation"
            data-conversation-id="${conversation.id}"
          >
            <span class="conversation-icon" data-icon="message-square"></span>
            <span class="conversation-copy">
              <strong>${escapeHTML(conversation.title)}</strong>
              <small>${escapeHTML(conversation.agent)} · ${escapeHTML(conversation.time)}</small>
            </span>
            <span class="icon-button tiny conversation-more" role="button" aria-label="更多">
              <span data-icon="more-horizontal"></span>
            </span>
          </button>
        `
      )
      .join("");
  }

  function renderChatWelcome() {
    return `
      <div class="chat-welcome">
        <div class="welcome-agent-mark">
          <span class="agent-orbit orbit-one"></span>
          <span class="agent-orbit orbit-two"></span>
          ${icon("sparkles", 26)}
        </div>
        <span class="page-eyebrow">NEXA INTELLIGENT AGENT</span>
        <h2>今天想推进什么？</h2>
        <p>描述一个目标，我会自主规划、调用企业工具，并把结果交付给你。</p>
        <div class="welcome-capabilities">
          <span>${icon("brain", 16)} 任务规划</span>
          <span>${icon("plug", 16)} 工具调用</span>
          <span>${icon("book-open", 16)} 企业知识</span>
          <span>${icon("shield-check", 16)} 过程可追溯</span>
        </div>
        <div class="welcome-prompt-grid">
          <button type="button" data-prompt="生成本周产品运营周报，汇总活跃、激活、留存和渠道表现">
            <span class="prompt-card-icon mint" data-icon="chart-column"></span>
            <span><strong>生成运营周报</strong><small>汇总本周指标、洞察与建议</small></span>
            <span data-icon="arrow-up-right"></span>
          </button>
          <button type="button" data-prompt="分析最近一周 AI Agent 竞品动态，提炼市场机会和风险">
            <span class="prompt-card-icon coral" data-icon="target"></span>
            <span><strong>扫描竞品动态</strong><small>追踪市场变化与竞争信号</small></span>
            <span data-icon="arrow-up-right"></span>
          </button>
          <button type="button" data-prompt="整理产品评审会的决策和行动项，并分配给负责人">
            <span class="prompt-card-icon blue" data-icon="users"></span>
            <span><strong>整理会议行动项</strong><small>提炼决策并自动创建任务</small></span>
            <span data-icon="arrow-up-right"></span>
          </button>
          <button type="button" data-prompt="分析 11 月客户反馈，提炼高频问题和产品机会">
            <span class="prompt-card-icon violet" data-icon="brain"></span>
            <span><strong>聚类客户反馈</strong><small>识别高频问题与产品机会</small></span>
            <span data-icon="arrow-up-right"></span>
          </button>
        </div>
      </div>
    `;
  }

  function renderToolTrace(message) {
    if (!message.toolTrace?.length) return "";
    return `
      <details class="tool-trace" open>
        <summary>
          <span><span data-icon="terminal"></span> 工具调用记录</span>
          <span class="trace-count">${message.toolTrace.length} 个工具</span>
          <span data-icon="chevron-down"></span>
        </summary>
        <div class="trace-list">
          ${message.toolTrace
            .map(
              (tool) => `
                <div class="trace-row ${tool.status === "error" ? "error" : ""}">
                  <span class="trace-icon" data-icon="${tool.status === "error" ? "triangle-alert" : "check"}"></span>
                  <span><strong>${escapeHTML(tool.label)}</strong><small>${escapeHTML(tool.detail)}</small></span>
                  <span class="trace-status">${tool.status === "error" ? "失败" : "完成"}</span>
                </div>
              `
            )
            .join("")}
        </div>
      </details>
    `;
  }

  function renderMessage(message) {
    if (message.role === "user") {
      return `
        <div class="message-row user-message">
          <div class="message-body">
            <div class="message-meta"><span>你</span><span>${escapeHTML(message.time || "刚刚")}</span></div>
            <div class="user-bubble">${formatMessage(message.content)}</div>
          </div>
          <span class="avatar avatar-lin">林</span>
        </div>
      `;
    }

    if (message.pending) {
      return `
        <div class="message-row assistant-message pending-message" data-message-id="${message.id}">
          <span class="agent-avatar">${icon("sparkles", 19)}</span>
          <div class="message-body wide">
            <div class="message-meta">
              <span><strong>NEXA Agent</strong> <i class="live-dot"></i> 正在执行</span>
              <span>${escapeHTML(message.time || "刚刚")}</span>
            </div>
            <div class="pending-card">
              <div class="pending-head">
                <span class="pending-loader"></span>
                <div><strong id="pendingStageTitle">${escapeHTML(message.stage || "正在理解任务目标")}</strong><small>Agent 正在自主规划执行路径</small></div>
              </div>
              <div class="pending-steps">
                <span class="active"><i>1</i> 理解目标 <b></b></span>
                <span><i>2</i> 规划步骤 <b></b></span>
                <span><i>3</i> 调用工具 <b></b></span>
                <span><i>4</i> 生成结果 <b></b></span>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    return `
      <div class="message-row assistant-message" data-message-id="${message.id}">
        <span class="agent-avatar">${icon("sparkles", 19)}</span>
        <div class="message-body wide">
          <div class="message-meta">
            <span><strong>NEXA Agent</strong> <span class="agent-mode">${state.mode === "llm" ? "LLM" : "DEMO"}</span></span>
            <span>${escapeHTML(message.time || "刚刚")}</span>
          </div>
          ${
            message.plan?.length
              ? `
                <div class="plan-strip">
                  <span class="plan-title">${icon("brain", 15)} 执行计划</span>
                  ${message.plan
                    .map((step, index) => `<span class="plan-step"><i>${String(index + 1).padStart(2, "0")}</i>${escapeHTML(step)}</span>`)
                    .join('<span class="plan-arrow">→</span>')}
                </div>
              `
              : ""
          }
          <div class="agent-message-content">${formatMessage(message.content)}</div>
          ${renderToolTrace(message)}
          ${
            message.sources?.length
              ? `
                <div class="message-sources">
                  <span>${icon("book-open", 15)} 参考来源</span>
                  ${message.sources
                    .map((source) => `<button type="button" data-action="open-source" data-source-id="${source.id}">${escapeHTML(source.title)}</button>`)
                    .join("")}
                </div>
              `
              : ""
          }
          <div class="message-actions">
            <button class="icon-button tiny" type="button" data-action="copy-answer" title="复制回答"><span data-icon="copy"></span></button>
            <button class="icon-button tiny" type="button" data-action="regenerate" title="重新生成"><span data-icon="refresh-cw"></span></button>
            <span class="message-action-divider"></span>
            <button class="text-button small" type="button" data-action="create-task-from-message"><span data-icon="plus"></span>转为任务</button>
          </div>
        </div>
      </div>
    `;
  }

  function renderChat() {
    const conversation = getActiveConversation();
    return `
      <div class="view chat-view">
        <div class="chat-layout">
          <aside class="chat-list-panel">
            <div class="chat-list-head">
              <div><span class="section-kicker">CONVERSATIONS</span><h2>对话</h2></div>
              <button class="icon-button soft" type="button" data-action="new-conversation" aria-label="新建对话"><span data-icon="plus"></span></button>
            </div>
            <div class="conversation-search">
              <span data-icon="search"></span>
              <input type="search" placeholder="搜索对话" aria-label="搜索对话" />
            </div>
            <div class="conversation-group-label">最近对话</div>
            <div class="conversation-list">${renderChatConversationList()}</div>
            <div class="chat-list-footer">
              <span class="agent-avatar tiny">${icon("sparkles", 15)}</span>
              <span><strong>3 个 Agent 在线</strong><small>服务运行正常</small></span>
              <i class="online-dot"></i>
            </div>
          </aside>

          <section class="conversation-panel">
            <div class="conversation-topbar">
              <button class="agent-selector" type="button" data-action="agent-picker">
                <span class="agent-avatar small">${icon("sparkles", 16)}</span>
                <span><strong>NEXA 通用助理</strong><small>自主规划 · 工具调用 · 多轮对话</small></span>
                <span data-icon="chevron-down"></span>
              </button>
              <div class="conversation-tools">
                <button class="icon-button" type="button" data-action="chat-options" aria-label="对话设置"><span data-icon="sliders-horizontal"></span></button>
                <button class="icon-button" type="button" data-action="chat-share" aria-label="分享对话"><span data-icon="external-link"></span></button>
              </div>
            </div>

            <div class="chat-scroll" id="chatScroll">
              <div class="chat-thread">
                ${
                  conversation?.messages.length
                    ? conversation.messages.map(renderMessage).join("")
                    : renderChatWelcome()
                }
              </div>
            </div>

            <div class="chat-composer-wrap">
              <form class="chat-composer" data-form="chat">
                <div class="composer-context">
                  <button type="button" class="context-chip" data-action="context-knowledge"><span data-icon="book-open"></span>企业知识库</button>
                  <button type="button" class="context-chip" data-action="context-tools"><span data-icon="plug"></span>4 个工具可用</button>
                  <span class="composer-mode">${state.mode === "llm" ? "LLM 已连接" : "本地演示模式"}</span>
                </div>
                <textarea
                  id="chatComposerInput"
                  name="prompt"
                  rows="1"
                  placeholder="输入任务，或继续追问..."
                  aria-label="发送消息"
                >${escapeHTML(state.chatInput || "")}</textarea>
                <div class="composer-actions">
                  <div>
                    <button class="icon-button" type="button" data-action="attach" aria-label="添加附件"><span data-icon="paperclip"></span></button>
                    <button class="icon-button" type="button" data-action="voice" aria-label="语音输入"><span data-icon="mic"></span></button>
                    <button class="icon-button" type="button" data-action="prompt-library" aria-label="提示词库"><span data-icon="wand-sparkles"></span></button>
                  </div>
                  <div class="composer-submit-group">
                    ${
                      state.generating
                        ? `<button class="stop-button" type="button" data-action="stop-generation"><span data-icon="circle-stop"></span>停止</button>`
                        : ""
                    }
                    <button class="send-button" type="submit" aria-label="发送消息" ${state.generating ? "disabled" : ""}>
                      <span data-icon="arrow-up"></span>
                    </button>
                  </div>
                </div>
              </form>
              <p class="composer-footnote">Agent 可能会犯错，请核对关键数据。工具调用过程可在回答中查看。</p>
            </div>
          </section>

          <aside class="chat-context-panel">
            <div class="context-head">
              <span class="section-kicker">AGENT CONTEXT</span>
              <h2>运行上下文</h2>
            </div>
            <div class="context-agent-card">
              <span class="agent-avatar">${icon("sparkles", 21)}</span>
              <div><strong>NEXA 通用助理</strong><span>${statusDot("在线", "ready")}</span></div>
              <button class="icon-button tiny" type="button" data-action="agent-settings" aria-label="Agent 设置"><span data-icon="sliders-horizontal"></span></button>
            </div>
            <div class="context-block">
              <div class="context-block-head"><span>可用能力</span><strong>4</strong></div>
              <div class="capability-list">
                <span><i class="mint" data-icon="brain"></i><span><strong>任务规划</strong><small>自动拆解复杂目标</small></span><b data-icon="check"></b></span>
                <span><i class="blue" data-icon="database"></i><span><strong>知识检索</strong><small>5 个知识空间</small></span><b data-icon="check"></b></span>
                <span><i class="coral" data-icon="wrench"></i><span><strong>工具调用</strong><small>4 个已连接工具</small></span><b data-icon="check"></b></span>
                <span><i class="violet" data-icon="shield-check"></i><span><strong>质量校验</strong><small>敏感信息与事实检查</small></span><b data-icon="check"></b></span>
              </div>
            </div>
            <div class="context-block">
              <div class="context-block-head"><span>本次会话</span><button class="text-button" type="button" data-action="clear-context">重置</button></div>
              <div class="session-stats">
                <span><small>消息轮次</small><strong>${conversation?.messages.length || 0}</strong></span>
                <span><small>工具调用</small><strong>${conversation?.messages.reduce((sum, item) => sum + (item.toolTrace?.length || 0), 0) || 0}</strong></span>
                <span><small>知识引用</small><strong>${conversation?.messages.reduce((sum, item) => sum + (item.sources?.length || 0), 0) || 0}</strong></span>
              </div>
            </div>
            <button class="context-help" type="button" data-action="help">
              <span data-icon="circle-help"></span>
              <span><strong>Agent 如何工作？</strong><small>查看规划与工具调用机制</small></span>
              <span data-icon="arrow-up-right"></span>
            </button>
          </aside>
        </div>
      </div>
    `;
  }

  function scrollChatToBottom(smooth) {
    const scroll = document.getElementById("chatScroll");
    if (!scroll) return;
    scroll.scrollTo({ top: scroll.scrollHeight, behavior: smooth ? "smooth" : "auto" });
  }

  function startNewConversation() {
    const now = new Date();
    const conversation = {
      id: `conv-${Date.now()}`,
      title: "新的对话",
      agent: "NEXA 通用助理",
      time: now.toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" }),
      messages: []
    };
    state.conversations.unshift(conversation);
    state.activeConversationId = conversation.id;
    state.chatInput = "";
    setView("chat");
  }

  function localFallbackReply(prompt) {
    const weekly = /周报|运营|数据|复盘/.test(prompt);
    if (weekly) {
      return {
        mode: "demo",
        content:
          "### 本周产品运营周报已完成\n\n我汇总了项目指标、增长策略与客户反馈，核心结论如下：\n\n**整体表现**\n- 活跃团队 **1,286**，环比增长 **12.4%**。\n- 新用户激活率 **61.8%**，环比提升 **3.2 个百分点**。\n- 周留存率 **74.6%**，环比下降 **1.1 个百分点**。\n\n**关键判断**\n产品内邀请渠道仍是主要增长来源，但新团队第二周的模板使用深度需要关注。\n\n**下一步建议**\n1. 上线新团队 3 步模板引导。\n2. 对留存下降团队做分渠道回访。\n3. 将高频工作流设为首周推荐模板。",
        plan: ["理解目标与交付标准", "读取项目指标", "企业知识检索", "校验结果并生成交付物"],
        toolTrace: [
          { label: "读取项目指标", detail: "获取活跃、激活与留存数据", status: "done" },
          { label: "企业知识检索", detail: "命中 2 篇增长与反馈文档", status: "done" }
        ],
        sources: [
          { id: "kb-growth-playbook", title: "2026 Q4 增长运营手册", type: "策略文档" },
          { id: "kb-customer-voice", title: "客户反馈主题聚类（11 月）", type: "客户洞察" }
        ]
      };
    }
    return {
      mode: "demo",
      content:
        "### 任务已拆解\n\n我已理解你的目标，并完成了第一轮信息整理。\n\n**建议执行路径**\n1. 明确交付物格式与截止时间。\n2. 调用项目指标、知识库和协作工具补齐事实。\n3. 生成初稿并执行完整性与一致性校验。\n4. 经你确认后发送到指定渠道。\n\n你可以继续补充目标受众、截止时间或输出格式，我会据此细化执行方案。",
      plan: ["理解目标与交付标准", "企业知识检索", "校验结果并生成交付物"],
      toolTrace: [{ label: "企业知识检索", detail: "检索相关企业内部知识", status: "done" }],
      sources: [{ id: "kb-product-release", title: "Agent Studio 2.4 发布说明", type: "产品文档" }]
    };
  }

  // A generation token prevents stopped or superseded responses from overwriting newer state.
  async function submitChatPrompt(prompt) {
    const cleanPrompt = String(prompt || "").trim();
    if (!cleanPrompt || state.generating) return;

    let conversation = getActiveConversation();
    if (!conversation) {
      startNewConversation();
      conversation = getActiveConversation();
    }
    if (!conversation) return;

    if (conversation.messages.length === 0) {
      conversation.title = cleanPrompt.slice(0, 24) + (cleanPrompt.length > 24 ? "…" : "");
    }

    const now = new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
    conversation.messages.push({ id: `user-${Date.now()}`, role: "user", content: cleanPrompt, time: now });
    const pendingId = `assistant-${Date.now()}`;
    conversation.messages.push({
      id: pendingId,
      role: "assistant",
      pending: true,
      stage: "正在理解任务目标",
      time: now
    });
    state.chatInput = "";
    state.generating = true;
    const token = ++state.generationToken;
    renderView();
    scrollChatToBottom(true);

    const stageTitles = ["正在规划执行步骤", "正在调用企业工具", "正在校验并生成结果"];
    stageTitles.forEach((title, index) => {
      window.setTimeout(() => {
        if (token !== state.generationToken) return;
        const titleElement = document.getElementById("pendingStageTitle");
        if (titleElement) titleElement.textContent = title;
        const steps = document.querySelectorAll(".pending-steps span");
        steps.forEach((step, stepIndex) => {
          step.classList.toggle("active", stepIndex === index + 1);
          step.classList.toggle("complete", stepIndex <= index);
        });
      }, 650 + index * 700);
    });

    const history = conversation.messages
      .filter((message) => !message.pending)
      .slice(-10)
      .map((message) => ({ role: message.role, content: message.content }));

    let reply;
    try {
      const response = await fetch("/api/agent/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history })
      });
      if (!response.ok) throw new Error(`Agent API ${response.status}`);
      const data = await response.json();
      if (!data.ok) throw new Error(data.error || "Agent API 返回异常");
      reply = data;
    } catch {
      reply = localFallbackReply(cleanPrompt);
    }

    if (token !== state.generationToken) return;
    const index = conversation.messages.findIndex((message) => message.id === pendingId);
    if (index >= 0) {
      conversation.messages[index] = {
        id: pendingId,
        role: "assistant",
        content: reply.content,
        plan: reply.plan,
        toolTrace: reply.toolTrace,
        sources: reply.sources,
        mode: reply.mode,
        time: new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })
      };
    }
    state.mode = reply.mode === "llm" ? "llm" : "demo";
    state.generating = false;
    renderView();
    scrollChatToBottom(true);
  }

  function stopGeneration() {
    if (!state.generating) return;
    state.generationToken += 1;
    state.generating = false;
    const conversation = getActiveConversation();
    if (conversation) {
      const pendingIndex = conversation.messages.findIndex((message) => message.pending);
      if (pendingIndex >= 0) {
        conversation.messages[pendingIndex] = {
          id: conversation.messages[pendingIndex].id,
          role: "assistant",
          content: "已停止本次执行。你可以调整目标或补充信息后重新发起。",
          time: "刚刚"
        };
      }
    }
    renderView();
    showToast("已停止执行", "本轮 Agent 任务已安全终止", "neutral");
  }

  function renderTaskCard(task) {
    const columnMeta = {
      backlog: { label: "待处理", action: "开始执行", icon: "play" },
      doing: { label: "进行中", action: "查看进度", icon: "activity" },
      review: { label: "待审核", action: "审核结果", icon: "eye" },
      done: { label: "已完成", action: "查看结果", icon: "file-text" }
    }[task.column];

    return `
      <article class="task-card" data-task-id="${task.id}">
        <div class="task-card-top">
          <span class="task-agent-icon ${task.tone}" data-icon="${task.icon}"></span>
          <span class="task-code">${task.id}</span>
          <button class="icon-button tiny" type="button" data-action="task-menu" aria-label="任务菜单"><span data-icon="more-horizontal"></span></button>
        </div>
        <h3>${escapeHTML(task.title)}</h3>
        <p>${escapeHTML(task.description)}</p>
        <div class="task-agent-row">
          <span class="mini-avatar">${escapeHTML(task.agent.slice(0, 1))}</span>
          <span>${escapeHTML(task.agent)}</span>
          <span class="task-owner">${escapeHTML(task.owner)}</span>
        </div>
        ${
          task.progress > 0
            ? `
              <div class="task-progress">
                <div><span>${task.progress}%</span><small>${columnMeta.label}</small></div>
                <div class="progress-track ${task.tone}"><span style="width:${task.progress}%"></span></div>
              </div>
            `
            : ""
        }
        <div class="task-card-footer">
          <span class="due-label"><span data-icon="clock"></span>${escapeHTML(task.due)}</span>
          <button class="task-action ${task.column === "review" ? "emphasis" : ""}" type="button" data-action="run-task" data-task-id="${task.id}">
            <span data-icon="${columnMeta.icon}"></span>${columnMeta.action}
          </button>
        </div>
      </article>
    `;
  }

  function renderTasks() {
    const columns = [
      { key: "backlog", title: "待处理", dot: "neutral", count: state.tasks.filter((task) => task.column === "backlog").length },
      { key: "doing", title: "进行中", dot: "mint", count: state.tasks.filter((task) => task.column === "doing").length },
      { key: "review", title: "等待审核", dot: "amber", count: state.tasks.filter((task) => task.column === "review").length },
      { key: "done", title: "已完成", dot: "blue", count: state.tasks.filter((task) => task.column === "done").length }
    ];
    const visibleColumns =
      state.taskFilter === "all" ? columns : columns.filter((column) => column.key === state.taskFilter);

    return `
      <div class="view tasks-view">
        ${pageHeading({
          eyebrow: "TASK ORCHESTRATION",
          title: "任务中心",
          subtitle: "让 Agent 负责执行，你只需要定义目标并审核关键结果。",
          actions: `
            <button class="secondary-button" type="button" data-action="task-view"><span data-icon="layout-dashboard"></span>看板视图</button>
            <button class="primary-button" type="button" data-action="new-task"><span data-icon="plus"></span>新建任务</button>
          `
        })}

        <div class="task-summary-strip">
          <div class="task-summary-main">
            <span class="summary-icon" data-icon="zap"></span>
            <div><strong>今日自动化效率 92%</strong><span>4 个 Agent 正在协作，预计节省 6.4 小时</span></div>
          </div>
          <div class="task-summary-metrics">
            <span><small>进行中</small><strong>2</strong></span>
            <span><small>待审核</small><strong>1</strong></span>
            <span><small>今日完成</small><strong>7</strong></span>
            <span><small>按时交付</small><strong>98%</strong></span>
          </div>
        </div>

        <div class="task-toolbar">
          <div class="segmented-filter">
            ${[
              ["all", "全部任务"],
              ["backlog", "待处理"],
              ["doing", "进行中"],
              ["review", "待审核"],
              ["done", "已完成"]
            ]
              .map(
                ([key, label]) => `
                  <button type="button" class="${state.taskFilter === key ? "active" : ""}" data-action="filter-tasks" data-filter="${key}">
                    ${label}
                  </button>
                `
              )
              .join("")}
          </div>
          <div class="task-toolbar-actions">
            <button class="filter-button" type="button" data-action="filter-menu"><span data-icon="list-filter"></span>筛选</button>
            <button class="filter-button" type="button" data-action="assignee-menu"><span data-icon="users"></span>负责人</button>
          </div>
        </div>

        <div class="kanban-board ${visibleColumns.length === 1 ? "single-column" : ""}">
          ${visibleColumns
            .map(
              (column) => `
                <section class="kanban-column">
                  <div class="kanban-head">
                    <div><i class="${column.dot}"></i><strong>${column.title}</strong><span>${column.count}</span></div>
                    <button class="icon-button tiny" type="button" data-action="column-menu" aria-label="${column.title}菜单"><span data-icon="more-horizontal"></span></button>
                  </div>
                  <div class="kanban-cards">
                    ${state.tasks
                      .filter((task) => task.column === column.key)
                      .map(renderTaskCard)
                      .join("")}
                    ${
                      column.key === "backlog"
                        ? `<button class="add-task-card" type="button" data-action="new-task"><span data-icon="plus"></span>添加任务</button>`
                        : ""
                    }
                  </div>
                </section>
              `
            )
            .join("")}
        </div>
      </div>
    `;
  }

  function workflowEdgesMarkup(nodes) {
    let markup = "";
    for (let index = 0; index < nodes.length - 1; index += 1) {
      const source = nodes[index];
      const target = nodes[index + 1];
      const startX = source.x + 168;
      const startY = source.y + 52;
      const endX = target.x;
      const endY = target.y + 52;
      const middle = (startX + endX) / 2;
      const active = source.status === "done" || source.status === "running";
      markup += `<path class="${active ? "active" : ""}" d="M ${startX} ${startY} C ${middle} ${startY}, ${middle} ${endY}, ${endX} ${endY}" />`;
    }
    return markup;
  }

  function renderWorkflowNodes() {
    return state.workflow.nodes
      .map(
        (node) => `
          <div
            class="flow-node type-${node.type} status-${node.status} ${state.workflow.selectedNodeId === node.id ? "selected" : ""}"
            style="left:${node.x}px; top:${node.y}px"
            data-node-id="${node.id}"
          >
            <span class="node-port input"></span>
            <button class="flow-node-main" type="button" data-action="select-node" data-node-id="${node.id}">
              <span class="node-head">
                <span class="node-icon" data-icon="${node.icon}"></span>
                <span class="node-index">${node.index}</span>
                <span class="node-status">
                  ${
                    node.status === "running"
                      ? `<span class="spinner"></span>`
                      : node.status === "done"
                        ? `<span data-icon="check"></span>`
                        : `<span data-icon="more-horizontal"></span>`
                  }
                </span>
              </span>
              <strong>${escapeHTML(node.title)}</strong>
              <small>${escapeHTML(node.description)}</small>
            </button>
            <span class="node-port output"></span>
          </div>
        `
      )
      .join("");
  }

  function renderWorkflowInspector() {
    const node =
      state.workflow.nodes.find((item) => item.id === state.workflow.selectedNodeId) ||
      state.workflow.nodes[0];
    if (!node) return "";

    const typeLabels = {
      trigger: "触发器",
      agent: "Agent 节点",
      tool: "工具节点",
      condition: "条件节点"
    };

    return `
      <div class="inspector-head">
        <div>
          <span class="section-kicker">NODE INSPECTOR</span>
          <h2>节点设置</h2>
        </div>
        <button class="icon-button tiny" type="button" data-action="close-inspector" aria-label="关闭设置"><span data-icon="x"></span></button>
      </div>
      <div class="inspector-node-type">
        <span class="node-icon ${node.type}" data-icon="${node.icon}"></span>
        <div><strong>${typeLabels[node.type]}</strong><small>${node.index} · ${escapeHTML(node.id)}</small></div>
        ${statusDot(node.status === "running" ? "运行中" : node.status === "done" ? "已完成" : "已配置", node.status === "running" ? "running" : "ready")}
      </div>
      <div class="inspector-form">
        <label>
          <span>节点名称</span>
          <input type="text" value="${escapeHTML(node.title)}" data-node-field="title" data-node-id="${node.id}" />
        </label>
        <label>
          <span>配置说明</span>
          <textarea rows="3" data-node-field="description" data-node-id="${node.id}">${escapeHTML(node.description)}</textarea>
        </label>
        <div class="inspector-row">
          <label><span>执行模型</span><select><option>NEXA Auto</option><option>DeepSeek Chat</option><option>GPT-4.1 mini</option></select></label>
          <label><span>超时时间</span><select><option>60 秒</option><option>120 秒</option><option>300 秒</option></select></label>
        </div>
        <div class="setting-toggle-row">
          <div><strong>失败时重试</strong><small>最多自动重试 2 次</small></div>
          <button class="switch on" type="button" role="switch" aria-checked="true" data-action="toggle-node-retry"><span></span></button>
        </div>
        <div class="setting-toggle-row">
          <div><strong>需要人工审核</strong><small>执行后暂停等待确认</small></div>
          <button class="switch" type="button" role="switch" aria-checked="false" data-action="toggle-node-review"><span></span></button>
        </div>
      </div>
      <div class="inspector-log">
        <div class="inspector-log-head"><span>最近运行</span><button class="text-button" type="button" data-view="runs">查看记录</button></div>
        ${
          state.workflow.logs.length
            ? state.workflow.logs
                .slice(-4)
                .reverse()
                .map(
                  (log) => `
                    <div class="inspector-log-row">
                      <span class="log-dot ${log.type || "success"}"></span>
                      <div><strong>${escapeHTML(log.title)}</strong><small>${escapeHTML(log.detail)}</small></div>
                      <span>${escapeHTML(log.time)}</span>
                    </div>
                  `
                )
                .join("")
            : `
              <div class="inspector-empty">
                ${icon("terminal", 20)}
                <span>运行工作流后可查看节点执行日志</span>
              </div>
            `
        }
      </div>
      <div class="inspector-actions">
        <button class="icon-button" type="button" data-action="duplicate-node" aria-label="复制节点"><span data-icon="copy"></span></button>
        <button class="icon-button danger" type="button" data-action="delete-node" aria-label="删除节点"><span data-icon="trash"></span></button>
        <button class="primary-button" type="button" data-action="save-node"><span data-icon="check"></span>应用设置</button>
      </div>
    `;
  }

  function renderWorkflow() {
    const nodes = state.workflow.nodes;
    const selected = nodes.find((node) => node.id === state.workflow.selectedNodeId);
    return `
      <div class="view workflow-view">
        <div class="workflow-view-head">
          <div class="workflow-title-block">
            <button class="icon-button" type="button" data-view="dashboard" aria-label="返回工作台"><span data-icon="arrow-left"></span></button>
            <div>
              <div class="workflow-title-row">
                <h1>${escapeHTML(state.workflow.name)}</h1>
                <span class="version-badge">${state.workflow.version}</span>
              </div>
              <p><span class="save-indicator"><i></i> 所有更改已保存</span> · 上次发布 2 小时前</p>
            </div>
          </div>
          <div class="workflow-head-actions">
            <button class="icon-button" type="button" data-action="workflow-undo" aria-label="撤销"><span data-icon="rotate-ccw"></span></button>
            <button class="secondary-button" type="button" data-action="workflow-test"><span data-icon="flask"></span>测试运行</button>
            <button class="primary-button run-button" type="button" data-action="run-workflow" ${state.workflow.running ? "disabled" : ""}>
              <span data-icon="${state.workflow.running ? "loader-circle" : "play"}"></span>${state.workflow.running ? "正在运行" : "运行工作流"}
            </button>
            <button class="icon-button" type="button" data-action="workflow-more" aria-label="更多操作"><span data-icon="more-horizontal"></span></button>
          </div>
        </div>

        <div class="workflow-shell">
          <div class="workflow-subtoolbar">
            <div class="workflow-tabs">
              <button class="active" type="button">编排画布</button>
              <button type="button" data-action="workflow-runs">运行历史 <span>${state.runs.length}</span></button>
              <button type="button" data-action="workflow-settings">工作流设置</button>
            </div>
            <div class="canvas-tools">
              <button class="filter-button" type="button" data-action="add-node"><span data-icon="plus"></span>添加节点</button>
              <button class="icon-button" type="button" data-action="workflow-guide" aria-label="使用指南"><span data-icon="circle-help"></span></button>
            </div>
          </div>

          <div class="workflow-workspace ${selected ? "" : "inspector-hidden"}">
            <div class="canvas-wrap">
              <div class="canvas-info">
                <span><span class="canvas-dot"></span> Agent Flow</span>
                <span>${nodes.length} 个节点 · ${nodes.length > 1 ? nodes.length - 1 : 0} 条连接</span>
              </div>
              <div class="canvas-scroll" id="canvasScroll">
                <div class="canvas-stage" id="canvasStage" style="transform: scale(${state.workflow.zoom})">
                  <svg class="canvas-edges" id="canvasEdges" viewBox="0 0 1280 520" preserveAspectRatio="none"></svg>
                  <div class="canvas-lane-label top">INPUT</div>
                  <div class="canvas-lane-label bottom">OUTPUT</div>
                  ${renderWorkflowNodes()}
                  <div class="canvas-note">
                    <span data-icon="sparkles"></span>
                    <span>Agent 会根据任务复杂度自动选择工具与执行路径</span>
                  </div>
                </div>
              </div>
              <div class="canvas-zoom">
                <button type="button" data-action="zoom-out" aria-label="缩小"><span data-icon="minus"></span></button>
                <span>${Math.round(state.workflow.zoom * 100)}%</span>
                <button type="button" data-action="zoom-in" aria-label="放大"><span data-icon="plus"></span></button>
                <button type="button" data-action="zoom-reset" aria-label="重置缩放"><span data-icon="maximize"></span></button>
              </div>
              <div class="canvas-minimap">
                <div class="minimap-stage">
                  ${nodes.map((node) => `<i style="left:${(node.x / 1280) * 100}%; top:${(node.y / 520) * 100}%"></i>`).join("")}
                  <span class="minimap-viewport"></span>
                </div>
              </div>
            </div>
            <aside class="node-inspector">${renderWorkflowInspector()}</aside>
          </div>
        </div>
      </div>
    `;
  }

  function drawWorkflowEdges() {
    const svg = document.getElementById("canvasEdges");
    if (!svg) return;
    svg.innerHTML = workflowEdgesMarkup(state.workflow.nodes);
  }

  // Workflow execution is simulated node-by-node to make state changes observable.
  function runWorkflow() {
    if (state.workflow.running) return;
    state.workflow.running = true;
    state.workflow.runIndex = -1;
    state.workflow.nodes.forEach((node) => {
      node.status = "idle";
    });
    state.workflow.logs = [
      { title: "工作流已启动", detail: "手动触发 · 林默", time: "刚刚", type: "info" }
    ];
    renderView();
    showToast("工作流已启动", `${state.workflow.nodes.length} 个节点开始执行`, "success");

    state.workflow.nodes.forEach((node, index) => {
      window.setTimeout(() => {
        if (!state.workflow.running) return;
        state.workflow.runIndex = index;
        state.workflow.nodes.forEach((item, itemIndex) => {
          if (itemIndex < index) item.status = "done";
          if (itemIndex === index) item.status = "running";
        });
        state.workflow.logs.push({
          title: node.title,
          detail: index === 0 ? "接收任务目标" : "节点执行成功",
          time: `${((index + 1) * 0.7).toFixed(1)}s`,
          type: "success"
        });
        if (state.view === "workflow") renderView();
      }, 550 + index * 760);
    });

    window.setTimeout(
      () => {
        if (!state.workflow.running) return;
        state.workflow.running = false;
        state.workflow.nodes.forEach((node) => {
          node.status = "done";
        });
        state.workflow.logs.push({
          title: "运行完成",
          detail: "结果已发送至飞书 · 总耗时 5.2 秒",
          time: "5.2s",
          type: "success"
        });
        const run = {
          id: `RUN-${Math.random().toString(16).slice(2, 7).toUpperCase()}`,
          name: state.workflow.name,
          agent: "NEXA Auto",
          trigger: "手动触发",
          status: "success",
          duration: "5.2s",
          tokens: "6.8k",
          time: "刚刚",
          steps: state.workflow.nodes.map((node) => [node.title, "已完成"])
        };
        state.runs.unshift(run);
        if (state.view === "workflow") renderView();
        showToast("工作流执行成功", "6 个节点全部完成，结果已发送至飞书", "success");
      },
      550 + state.workflow.nodes.length * 760 + 300
    );
  }

  function docTypeClass(typeKey) {
    return `doc-type-${typeKey || "strategy"}`;
  }

  function renderKnowledge() {
    const query = state.docQuery.trim().toLowerCase();
    const types = ["全部", "策略文档", "产品文档", "市场情报", "客户洞察", "制度规范"];
    const visibleDocs = state.docs.filter((doc) => {
      const matchesQuery =
        !query ||
        `${doc.title} ${doc.summary} ${doc.owner} ${doc.type}`.toLowerCase().includes(query);
      const matchesType = state.docType === "全部" || doc.type === state.docType;
      return matchesQuery && matchesType;
    });
    const selectedDoc =
      visibleDocs.find((doc) => doc.id === state.selectedDocId) ||
      visibleDocs[0] ||
      state.docs[0];

    return `
      <div class="view knowledge-view">
        ${pageHeading({
          eyebrow: "ENTERPRISE KNOWLEDGE",
          title: "知识库",
          subtitle: "让 Agent 基于可信企业知识工作，每次引用都可追溯到原文。",
          actions: `
            <button class="secondary-button" type="button" data-action="knowledge-settings"><span data-icon="sliders-horizontal"></span>检索设置</button>
            <button class="primary-button" type="button" data-action="upload-knowledge"><span data-icon="upload"></span>上传文档</button>
            <input id="knowledgeFile" type="file" hidden multiple accept=".pdf,.doc,.docx,.txt,.md,.csv" />
          `
        })}

        <div class="knowledge-stats">
          <div><span class="knowledge-stat-icon mint" data-icon="book-open"></span><span><small>知识文档</small><strong>${state.docs.length + 1}</strong></span><em>+3 本周</em></div>
          <div><span class="knowledge-stat-icon blue" data-icon="layers"></span><span><small>知识分块</small><strong>${state.docs.reduce((sum, doc) => sum + doc.chunks, 0) + 18}</strong></span><em>已向量化</em></div>
          <div><span class="knowledge-stat-icon coral" data-icon="link-2"></span><span><small>本月引用</small><strong>${state.docs.reduce((sum, doc) => sum + doc.references, 0)}</strong></span><em>+18.4%</em></div>
          <div><span class="knowledge-stat-icon violet" data-icon="target"></span><span><small>检索命中率</small><strong>94.2%</strong></span><em>近 7 天</em></div>
        </div>

        <div class="knowledge-layout">
          <section class="panel knowledge-list-panel">
            <div class="knowledge-toolbar">
              <div class="knowledge-search">
                <span data-icon="search"></span>
                <input id="docSearchInput" type="search" placeholder="搜索知识文档、内容或负责人" value="${escapeHTML(state.docQuery)}" />
                <kbd>⌘ F</kbd>
              </div>
              <button class="icon-button" type="button" data-action="doc-sort" aria-label="排序"><span data-icon="list-filter"></span></button>
            </div>
            <div class="doc-type-tabs">
              ${types
                .map(
                  (type) => `
                    <button type="button" class="${state.docType === type ? "active" : ""}" data-action="filter-docs" data-doc-type="${type}">
                      ${type}
                    </button>
                  `
                )
                .join("")}
            </div>
            <div class="doc-list">
              ${visibleDocs
                .map(
                  (doc) => `
                    <button
                      class="doc-row ${selectedDoc?.id === doc.id ? "active" : ""}"
                      type="button"
                      data-action="select-doc"
                      data-doc-id="${doc.id}"
                    >
                      <span class="doc-type-icon ${docTypeClass(doc.typeKey)}" data-icon="${doc.typeKey === "market" ? "globe" : doc.typeKey === "insight" ? "users" : doc.typeKey === "policy" ? "shield-check" : "file-text"}"></span>
                      <span class="doc-copy">
                        <span class="doc-name-row"><strong>${escapeHTML(doc.title)}</strong><i>${escapeHTML(doc.type)}</i></span>
                        <small>${escapeHTML(doc.summary)}</small>
                        <span class="doc-meta"><span>${escapeHTML(doc.owner)}</span><span>${escapeHTML(doc.updated)}</span><span>${doc.references} 次引用</span></span>
                      </span>
                      <span class="doc-arrow" data-icon="chevron-right"></span>
                    </button>
                  `
                )
                .join("")}
              ${
                visibleDocs.length
                  ? ""
                  : `
                    <div class="empty-state">
                      <span data-icon="search"></span>
                      <strong>没有找到匹配文档</strong>
                      <p>尝试更换关键词或文档类型。</p>
                    </div>
                  `
              }
            </div>
            <div class="doc-list-footer">
              <span>显示 ${visibleDocs.length} / ${state.docs.length + 1} 篇文档</span>
              <button class="text-button" type="button" data-action="sync-knowledge"><span data-icon="refresh-cw"></span>同步数据源</button>
            </div>
          </section>

          <aside class="panel doc-detail-panel">
            ${
              selectedDoc
                ? `
                  <div class="doc-detail-head">
                    <div class="doc-breadcrumb"><span>知识库</span><span data-icon="chevron-right"></span><span>${escapeHTML(selectedDoc.type)}</span></div>
                    <button class="icon-button" type="button" data-action="doc-more" aria-label="更多"><span data-icon="more-horizontal"></span></button>
                  </div>
                  <div class="doc-detail-title">
                    <span class="doc-detail-icon ${docTypeClass(selectedDoc.typeKey)}" data-icon="${selectedDoc.typeKey === "market" ? "globe" : selectedDoc.typeKey === "insight" ? "users" : selectedDoc.typeKey === "policy" ? "shield-check" : "file-text"}"></span>
                    <h2>${escapeHTML(selectedDoc.title)}</h2>
                    <p>${escapeHTML(selectedDoc.summary)}</p>
                  </div>
                  <div class="doc-detail-meta">
                    <span><small>负责人</small><strong>${escapeHTML(selectedDoc.owner)}</strong></span>
                    <span><small>更新时间</small><strong>${escapeHTML(selectedDoc.updated)}</strong></span>
                    <span><small>知识分块</small><strong>${selectedDoc.chunks}</strong></span>
                    <span><small>被 Agent 引用</small><strong>${selectedDoc.references} 次</strong></span>
                  </div>
                  <div class="doc-preview">
                    <div class="doc-preview-head">
                      <span>内容预览</span>
                      <span class="vector-badge"><i></i> 已完成向量化</span>
                    </div>
                    <div class="doc-preview-body">
                      <p>${escapeHTML(selectedDoc.summary)}</p>
                      <div class="preview-snippet">
                        <span class="snippet-number">CHUNK 01</span>
                        <p>
                          Agent 在执行相关任务时，将优先检索本文档中的结构化知识与关键指标。
                          检索结果包含来源标题、文档类型与段落位置，便于用户核验事实。
                        </p>
                      </div>
                      <div class="preview-highlight">
                        ${icon("sparkles", 17)}
                        <span><strong>Agent 使用建议</strong><small>适合用于运营周报、市场分析和内部知识问答。</small></span>
                      </div>
                    </div>
                  </div>
                  <div class="doc-detail-actions">
                    <button class="secondary-button" type="button" data-action="preview-doc"><span data-icon="eye"></span>查看原文</button>
                    <button class="primary-button" type="button" data-action="use-doc-in-chat"><span data-icon="message-square"></span>用于对话</button>
                  </div>
                `
                : `
                  <div class="empty-state tall">
                    <span data-icon="file-text"></span>
                    <strong>选择一篇知识文档</strong>
                    <p>查看文档摘要、引用情况和检索效果。</p>
                  </div>
                `
            }
          </aside>
        </div>
      </div>
    `;
  }

  function renderTools() {
    const query = state.toolQuery.trim().toLowerCase();
    const tools = state.tools.filter(
      (tool) =>
        (state.toolCategory === "全部" || tool.category === state.toolCategory) &&
        `${tool.name} ${tool.description} ${tool.category}`.toLowerCase().includes(query)
    );
    const connectedCount = state.tools.filter((tool) => tool.connected).length;
    const enabledCount = state.tools.filter((tool) => tool.enabled).length;

    return `
      <div class="view tools-view">
        ${pageHeading({
          eyebrow: "CONNECTED TOOLS",
          title: "工具连接",
          subtitle: "为 Agent 连接企业系统，让规划真正转化为可执行的动作。",
          actions: `
            <button class="secondary-button" type="button" data-action="tool-docs"><span data-icon="book-open"></span>开发文档</button>
            <button class="primary-button" type="button" data-action="request-tool"><span data-icon="plus"></span>添加自定义工具</button>
          `
        })}

        <div class="security-banner">
          <span class="security-icon" data-icon="shield-check"></span>
          <div><strong>企业级安全连接</strong><span>凭据使用 AES-256 加密存储；所有工具调用均记录发起人、Agent、参数摘要和返回状态。</span></div>
          <button class="text-button" type="button" data-action="security-details">安全策略 <span data-icon="arrow-right"></span></button>
        </div>

        <div class="tools-overview">
          <div class="tool-overview-main">
            <span class="tool-orbit-icon">${icon("plug", 22)}</span>
            <div><strong>${connectedCount} 个工具已连接</strong><span>Agent 当前可调用 ${enabledCount} 个企业工具</span></div>
          </div>
          <div class="tool-health">
            <span><i class="success"></i>连接正常 <strong>${enabledCount}</strong></span>
            <span><i class="neutral"></i>已暂停 <strong>${connectedCount - enabledCount}</strong></span>
            <span><i class="warning"></i>需关注 <strong>0</strong></span>
          </div>
          <div class="tools-search">
            <span data-icon="search"></span>
            <input id="toolSearchInput" type="search" placeholder="搜索工具" value="${escapeHTML(state.toolQuery)}" />
          </div>
        </div>

        <div class="tool-category-nav">
          ${["全部", "协作", "知识", "研发", "开放接口"]
            .map(
              (category, index) => `
                <button type="button" class="${state.toolCategory === category ? "active" : ""}" data-action="filter-tools" data-category="${category}">
                  ${category}${index < 4 ? `<span>${state.tools.filter((tool) => tool.category === category).length}</span>` : ""}
                </button>
              `
            )
            .join("")}
        </div>

        <div class="tools-grid">
          ${tools
            .map(
              (tool) => `
                <article class="tool-card ${tool.connected ? "connected" : ""}">
                  <div class="tool-card-head">
                    <span class="tool-logo ${tool.tone}" data-icon="${tool.icon}"></span>
                    <span class="tool-category">${escapeHTML(tool.category)}</span>
                    ${
                      tool.connected
                        ? `<button class="switch ${tool.enabled ? "on" : ""}" type="button" role="switch" aria-checked="${tool.enabled}" data-action="toggle-tool" data-tool-id="${tool.id}" aria-label="${tool.enabled ? "停用" : "启用"}${tool.name}"><span></span></button>`
                        : `<span class="connection-status">未连接</span>`
                    }
                  </div>
                  <h3>${escapeHTML(tool.name)}</h3>
                  <p>${escapeHTML(tool.description)}</p>
                  <div class="tool-account">
                    ${
                      tool.connected
                        ? `<span class="connected-indicator"><i></i>${escapeHTML(tool.account)}</span><span data-icon="circle-check"></span>`
                        : `<span>连接后即可授权 Agent 调用</span>`
                    }
                  </div>
                  <div class="tool-card-actions">
                    ${
                      tool.connected
                        ? `
                          <button class="secondary-button compact" type="button" data-action="configure-tool" data-tool-id="${tool.id}"><span data-icon="sliders-horizontal"></span>配置</button>
                          <button class="icon-button tiny" type="button" data-action="tool-disconnect" data-tool-id="${tool.id}" aria-label="断开连接"><span data-icon="more-horizontal"></span></button>
                        `
                        : `<button class="primary-button compact" type="button" data-action="connect-tool" data-tool-id="${tool.id}"><span data-icon="plus"></span>连接工具</button>`
                    }
                  </div>
                </article>
              `
            )
            .join("")}
        </div>

        <div class="developer-tool-banner">
          <div class="developer-banner-icon">${icon("code", 24)}</div>
          <div><strong>构建你自己的企业工具</strong><span>使用 OpenAPI Schema 或自定义函数，将内部能力暴露给 Agent。</span></div>
          <div class="developer-code"><code>POST /api/tools</code><span>application/json</span></div>
          <button class="secondary-button compact" type="button" data-action="tool-docs"><span data-icon="external-link"></span>查看接入指南</button>
        </div>
      </div>
    `;
  }

  function runStatusMeta(status) {
    return {
      success: { label: "成功", className: "success", icon: "circle-check" },
      running: { label: "运行中", className: "running", icon: "loader-circle" },
      review: { label: "待审核", className: "review", icon: "clock" },
      failed: { label: "失败", className: "failed", icon: "triangle-alert" }
    }[status];
  }

  function renderRunRow(run) {
    const status = runStatusMeta(run.status);
    const expanded = state.expandedRunId === run.id;
    return `
      <div class="run-record ${expanded ? "expanded" : ""}">
        <button class="run-table-row" type="button" data-action="toggle-run" data-run-id="${run.id}" aria-expanded="${expanded}">
          <span class="run-identity">
            <span class="run-status-icon ${status.className}" data-icon="${status.icon}"></span>
            <span><strong>${escapeHTML(run.name)}</strong><small>${run.id} · ${escapeHTML(run.agent)}</small></span>
          </span>
          <span class="run-trigger"><span data-icon="${run.trigger === "手动触发" ? "play" : run.trigger === "Webhook" ? "webhook" : "clock"}"></span>${escapeHTML(run.trigger)}</span>
          <span class="run-duration">${escapeHTML(run.duration)}</span>
          <span class="run-tokens">${escapeHTML(run.tokens)} tokens</span>
          <span class="run-time">${escapeHTML(run.time)}</span>
          <span class="run-status ${status.className}"><i></i>${status.label}</span>
          <span class="run-expand" data-icon="${expanded ? "chevron-up" : "chevron-down"}"></span>
        </button>
        ${
          expanded
            ? `
              <div class="run-detail">
                <div class="run-trace">
                  <div class="run-detail-title"><span>执行轨迹</span><small>每一步均可追溯</small></div>
                  ${run.steps
                    .map(
                      (step, index) => `
                        <div class="run-trace-step ${index === run.steps.length - 1 ? "last" : ""}">
                          <span class="trace-number">${String(index + 1).padStart(2, "0")}</span>
                          <div><strong>${escapeHTML(step[0])}</strong><small>${escapeHTML(step[1])}</small></div>
                        </div>
                      `
                    )
                    .join("")}
                </div>
                <div class="run-output">
                  <div class="run-detail-title"><span>运行摘要</span><button class="text-button" type="button" data-action="download-run"><span data-icon="download"></span>导出</button></div>
                  <div class="run-output-card">
                    <span class="output-icon" data-icon="${status.icon}"></span>
                    <div>
                      <strong>${run.status === "success" ? "任务已成功交付" : run.status === "running" ? "Agent 正在继续执行" : run.status === "review" ? "已暂停，等待人工确认" : "执行中断，需要检查配置"}</strong>
                      <p>${run.status === "success" ? "输出结果已写入任务中心，并按规则发送协作通知。" : run.status === "running" ? "可以离开当前页面，后续结果会通过通知中心发送。" : run.status === "review" ? "审核通过后将自动执行发送动作。" : "数据仓库连接凭据已过期，更新后可重新运行。"}</p>
                    </div>
                  </div>
                  <div class="run-actions">
                    ${run.status === "failed" ? `<button class="primary-button compact" type="button" data-action="retry-run"><span data-icon="refresh-cw"></span>重新运行</button>` : `<button class="secondary-button compact" type="button" data-action="view-run-output"><span data-icon="eye"></span>查看输出</button>`}
                    <button class="icon-button" type="button" data-action="run-more" aria-label="更多"><span data-icon="more-horizontal"></span></button>
                  </div>
                </div>
              </div>
            `
            : ""
        }
      </div>
    `;
  }

  function renderRuns() {
    const filters = [
      ["all", "全部"],
      ["success", "成功"],
      ["running", "运行中"],
      ["review", "待审核"],
      ["failed", "失败"]
    ];
    const runs = state.runs.filter((run) => state.runFilter === "all" || run.status === state.runFilter);
    const successCount = state.runs.filter((run) => run.status === "success").length;
    const failedCount = state.runs.filter((run) => run.status === "failed").length;

    return `
      <div class="view runs-view">
        ${pageHeading({
          eyebrow: "EXECUTION OBSERVABILITY",
          title: "运行记录",
          subtitle: "查看 Agent 的每一次规划、工具调用和结果交付，让自动化过程透明可控。",
          actions: `
            <button class="secondary-button" type="button" data-action="run-date-filter"><span data-icon="calendar"></span>近 7 天</button>
            <button class="primary-button" type="button" data-action="export-runs"><span data-icon="download"></span>导出记录</button>
          `
        })}

        <div class="run-kpi-grid">
          <article class="run-kpi">
            <span class="run-kpi-icon mint" data-icon="activity"></span>
            <div><small>总运行次数</small><strong>${state.runs.length}</strong><em>+18.4% 本周</em></div>
            <svg viewBox="0 0 80 34" aria-hidden="true"><path d="M2 29 C12 27, 14 21, 23 23 S34 11, 43 15 S55 7, 64 9 S72 2, 78 4"/></svg>
          </article>
          <article class="run-kpi">
            <span class="run-kpi-icon blue" data-icon="circle-check"></span>
            <div><small>成功率</small><strong>98.7%</strong><em>目标 ≥ 98%</em></div>
            <svg viewBox="0 0 80 34" aria-hidden="true"><path d="M2 27 C10 26, 16 21, 24 22 S34 17, 42 16 S54 13, 61 10 S70 10, 78 5"/></svg>
          </article>
          <article class="run-kpi">
            <span class="run-kpi-icon coral" data-icon="clock"></span>
            <div><small>平均耗时</small><strong>26.4s</strong><em>-4.2s 较上周</em></div>
            <svg viewBox="0 0 80 34" aria-hidden="true"><path d="M2 17 C12 13, 16 23, 24 18 S35 22, 43 15 S54 18, 62 9 S72 13, 78 6"/></svg>
          </article>
          <article class="run-kpi">
            <span class="run-kpi-icon violet" data-icon="triangle-alert"></span>
            <div><small>异常运行</small><strong>${failedCount}</strong><em>1 项需要处理</em></div>
            <svg viewBox="0 0 80 34" aria-hidden="true"><path d="M2 26 C10 26, 16 24, 23 27 S35 18, 43 24 S54 7, 62 18 S71 24, 78 25"/></svg>
          </article>
        </div>

        <section class="panel runs-panel">
          <div class="runs-toolbar">
            <div class="run-filter-tabs">
              ${filters
                .map(
                  ([key, label]) => `
                    <button type="button" class="${state.runFilter === key ? "active" : ""}" data-action="filter-runs" data-filter="${key}">
                      ${label}
                      ${key !== "all" ? `<span>${state.runs.filter((run) => run.status === key).length}</span>` : ""}
                    </button>
                  `
                )
                .join("")}
            </div>
            <div class="runs-toolbar-right">
              <div class="runs-search">
                <span data-icon="search"></span>
                <input type="search" placeholder="搜索运行记录" aria-label="搜索运行记录" />
              </div>
              <button class="icon-button" type="button" data-action="run-refresh" aria-label="刷新"><span data-icon="refresh-cw"></span></button>
            </div>
          </div>
          <div class="run-table">
            <div class="run-table-head">
              <span>运行 / Agent</span>
              <span>触发方式</span>
              <span>耗时</span>
              <span>用量</span>
              <span>时间</span>
              <span>状态</span>
              <span></span>
            </div>
            <div class="run-table-body">
              ${runs.map(renderRunRow).join("")}
              ${
                runs.length
                  ? ""
                  : `<div class="empty-state"><span data-icon="activity"></span><strong>没有匹配的运行记录</strong><p>调整筛选条件后再试。</p></div>`
              }
            </div>
          </div>
          <div class="run-table-footer">
            <span>共 ${runs.length} 条记录 · 数据保留 90 天</span>
            <div class="pagination"><button disabled>上一页</button><button class="active">1</button><button disabled>下一页</button></div>
          </div>
        </section>
      </div>
    `;
  }

  let suppressFlowClickUntil = 0;
  let nodeDrag = null;

  function showToast(title, detail, tone) {
    const toast = document.createElement("div");
    toast.className = `toast ${tone || "success"}`;
    toast.innerHTML = `
      <span class="toast-icon" data-icon="${tone === "neutral" ? "circle-dot" : tone === "warning" ? "triangle-alert" : "circle-check"}"></span>
      <span><strong>${escapeHTML(title)}</strong>${detail ? `<small>${escapeHTML(detail)}</small>` : ""}</span>
      <button type="button" aria-label="关闭通知"><span data-icon="x"></span></button>
    `;
    hydrateIcons(toast);
    toastRegion.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add("visible"));
    const remove = () => {
      toast.classList.remove("visible");
      window.setTimeout(() => toast.remove(), 220);
    };
    toast.querySelector("button").addEventListener("click", remove);
    window.setTimeout(remove, 4200);
  }

  function openSidebar() {
    sidebar.classList.add("open");
    mobileScrim.classList.add("visible");
    document.body.classList.add("nav-open");
  }

  function closeSidebar() {
    sidebar.classList.remove("open");
    mobileScrim.classList.remove("visible");
    document.body.classList.remove("nav-open");
  }

  function closePopovers() {
    notificationPopover.hidden = true;
    document.getElementById("notificationTrigger")?.classList.remove("active");
  }

  function openNotificationPopover() {
    const willOpen = notificationPopover.hidden;
    closePopovers();
    notificationPopover.hidden = !willOpen;
    document.getElementById("notificationTrigger")?.classList.toggle("active", willOpen);
  }

  function commandItems(query) {
    const q = query.trim().toLowerCase();
    const navItems = NAV_ITEMS.map((item) => ({
      type: "view",
      label: item.label,
      detail: `前往${item.label}`,
      icon: item.icon,
      value: item.view,
      keywords: `${item.label} ${item.keywords}`
    }));
    const prompts = [
      ["生成运营周报", "汇总本周指标、洞察与建议", "chart-column", "生成本周产品运营周报，汇总活跃、激活、留存和渠道表现"],
      ["扫描竞品动态", "追踪市场变化与竞争信号", "target", "分析最近一周 AI Agent 竞品动态，提炼市场机会和风险"],
      ["整理会议行动项", "提炼决策并创建任务", "users", "整理产品评审会的决策和行动项，并分配给负责人"],
      ["聚类客户反馈", "识别高频问题与产品机会", "brain", "分析 11 月客户反馈，提炼高频问题和产品机会"]
    ].map(([label, detail, iconName, prompt]) => ({
      type: "prompt",
      label,
      detail,
      icon: iconName,
      value: prompt,
      keywords: `${label} ${detail} 提示词 任务`
    }));
    const actions = [
      {
        type: "action",
        label: "创建 Agent",
        detail: "配置角色、模型与可用工具",
        icon: "plus",
        value: "create-agent",
        keywords: "新建 agent 智能体"
      },
      {
        type: "action",
        label: "上传知识文档",
        detail: "向企业知识库添加内容",
        icon: "upload",
        value: "upload-knowledge",
        keywords: "知识 文档 上传 rag"
      },
      {
        type: "action",
        label: "运行工作流",
        detail: "打开运营周报自动化",
        icon: "play",
        value: "run-workflow-current",
        keywords: "workflow 自动化 运行"
      }
    ];

    return [...navItems, ...prompts, ...actions].filter((item) =>
      !q || `${item.label} ${item.detail} ${item.keywords}`.toLowerCase().includes(q)
    );
  }

  function renderCommandResults(query) {
    state.paletteItems = commandItems(query);
    if (state.paletteIndex >= state.paletteItems.length) state.paletteIndex = 0;

    if (!state.paletteItems.length) {
      commandResults.innerHTML = `
        <div class="palette-empty">
          <span data-icon="search"></span>
          <strong>没有找到结果</strong>
          <p>试试搜索页面、Agent 或输入一个任务目标。</p>
        </div>
      `;
      hydrateIcons(commandResults);
      return;
    }

    let lastType = "";
    commandResults.innerHTML = state.paletteItems
      .map((item, index) => {
        const groupLabel =
          item.type === "view" ? "前往页面" : item.type === "prompt" ? "快捷任务" : "快捷操作";
        const showGroup = groupLabel !== lastType;
        lastType = groupLabel;
        return `
          ${showGroup ? `<div class="palette-group-label">${groupLabel}</div>` : ""}
          <button class="palette-item ${index === state.paletteIndex ? "active" : ""}" type="button" data-command-index="${index}">
            <span class="palette-item-icon" data-icon="${item.icon}"></span>
            <span><strong>${escapeHTML(item.label)}</strong><small>${escapeHTML(item.detail)}</small></span>
            <span class="palette-enter">↵</span>
          </button>
        `;
      })
      .join("");
    hydrateIcons(commandResults);
  }

  function openCommandPalette() {
    closePopovers();
    closeModal();
    commandOverlay.hidden = false;
    state.paletteIndex = 0;
    commandInput.value = "";
    renderCommandResults("");
    window.setTimeout(() => commandInput.focus(), 30);
  }

  function closeCommandPalette() {
    commandOverlay.hidden = true;
    commandInput.value = "";
  }

  function executeCommandItem(index) {
    const item = state.paletteItems[index];
    if (!item) return;
    closeCommandPalette();
    if (item.type === "view") {
      setView(item.value);
      return;
    }
    if (item.type === "prompt") {
      setView("chat");
      startNewConversation();
      window.setTimeout(() => submitChatPrompt(item.value), 40);
      return;
    }
    if (item.type === "action") {
      handleAction(item.value, {});
    }
  }

  function openModal({ eyebrow, title, description, body, footer, size, iconName }) {
    closeModal();
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.id = "modalOverlay";
    overlay.innerHTML = `
      <div class="modal-card ${size || ""}" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
        <div class="modal-head">
          <div class="modal-title-group">
            ${iconName ? `<span class="modal-icon" data-icon="${iconName}"></span>` : ""}
            <div>
              ${eyebrow ? `<span class="section-kicker">${escapeHTML(eyebrow)}</span>` : ""}
              <h2 id="modalTitle">${escapeHTML(title)}</h2>
              ${description ? `<p>${escapeHTML(description)}</p>` : ""}
            </div>
          </div>
          <button class="icon-button" type="button" data-action="close-modal" aria-label="关闭"><span data-icon="x"></span></button>
        </div>
        <div class="modal-body">${body}</div>
        ${footer ? `<div class="modal-footer">${footer}</div>` : ""}
      </div>
    `;
    document.body.appendChild(overlay);
    hydrateIcons(overlay);
    requestAnimationFrame(() => overlay.classList.add("visible"));
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) closeModal();
    });
    window.setTimeout(() => overlay.querySelector("input, textarea, select")?.focus(), 80);
  }

  function closeModal() {
    const overlay = document.getElementById("modalOverlay");
    if (!overlay) return;
    overlay.classList.remove("visible");
    window.setTimeout(() => overlay.remove(), 180);
  }

  function openCreateAgentModal() {
    openModal({
      eyebrow: "AGENT BUILDER",
      title: "创建专属 Agent",
      description: "定义角色与能力边界，NEXA 会为它配置规划策略和可用工具。",
      iconName: "sparkles",
      size: "medium",
      body: `
        <form class="modal-form" id="createAgentForm" data-form="create-agent">
          <label><span>Agent 名称</span><input name="agentName" required placeholder="例如：销售策略顾问" /></label>
          <label>
            <span>职责描述</span>
            <textarea name="agentRole" rows="3" required placeholder="描述它负责解决的问题、工作方式和交付标准"></textarea>
          </label>
          <div class="modal-form-grid">
            <label><span>执行模型</span><select name="model"><option>NEXA Auto</option><option>DeepSeek Chat</option><option>GPT-4.1 mini</option></select></label>
            <label><span>知识空间</span><select name="knowledge"><option>企业全部知识</option><option>产品与市场</option><option>客户洞察</option></select></label>
          </div>
          <div class="modal-choice">
            <span>默认工具</span>
            <div>
              <label><input type="checkbox" checked /> 企业知识库</label>
              <label><input type="checkbox" checked /> 项目指标</label>
              <label><input type="checkbox" /> 飞书通知</label>
            </div>
          </div>
        </form>
      `,
      footer: `
        <button class="secondary-button" type="button" data-action="close-modal">取消</button>
        <button class="primary-button" type="submit" form="createAgentForm"><span data-icon="sparkles"></span>创建 Agent</button>
      `
    });
  }

  function openNodePicker() {
    const types = [
      ["agent", "Agent 节点", "调用大模型执行理解、推理或生成任务", "brain"],
      ["tool", "工具节点", "调用已连接的企业系统与开放接口", "plug"],
      ["condition", "条件节点", "根据变量或模型判断进入不同分支", "git-branch"],
      ["trigger", "触发器", "接收手动、定时、Webhook 或日历事件", "play"]
    ];
    openModal({
      eyebrow: "ADD NODE",
      title: "添加工作流节点",
      description: "选择节点类型并添加到当前编排画布。",
      iconName: "plus",
      body: `
        <div class="node-picker-grid">
          ${types
            .map(
              ([type, title, description, iconName]) => `
                <button type="button" data-action="choose-node-type" data-node-type="${type}" data-node-icon="${iconName}">
                  <span class="node-picker-icon ${type}" data-icon="${iconName}"></span>
                  <span><strong>${title}</strong><small>${description}</small></span>
                  <span data-icon="plus"></span>
                </button>
              `
            )
            .join("")}
        </div>
      `
    });
  }

  function openHelpModal() {
    openModal({
      eyebrow: "QUICK GUIDE",
      title: "Agent 如何工作？",
      description: "NEXA 将复杂目标转换为可观测、可控制、可复用的执行过程。",
      iconName: "circle-help",
      size: "medium",
      body: `
        <div class="help-flow">
          <div><span>01</span><strong>理解目标</strong><p>识别交付物、约束、受众与截止时间。</p></div>
          <div><span>02</span><strong>自主规划</strong><p>拆解步骤，判断是否需要知识与工具。</p></div>
          <div><span>03</span><strong>调用工具</strong><p>执行检索、数据读取、任务创建与通知。</p></div>
          <div><span>04</span><strong>校验交付</strong><p>检查事实与格式，记录完整执行轨迹。</p></div>
        </div>
        <div class="help-shortcuts">
          <div><span>打开全局命令</span><kbd>Ctrl K</kbd></div>
          <div><span>发起新任务</span><kbd>N</kbd></div>
          <div><span>关闭当前浮层</span><kbd>Esc</kbd></div>
        </div>
      `,
      footer: `<button class="primary-button" type="button" data-action="close-modal">知道了</button>`
    });
  }

  function openRequestToolModal() {
    openModal({
      eyebrow: "CUSTOM TOOL",
      title: "接入自定义工具",
      description: "通过 OpenAPI Schema 将企业内部能力安全地开放给 Agent。",
      iconName: "code",
      size: "medium",
      body: `
        <form class="modal-form" id="requestToolForm" data-form="request-tool">
          <label><span>工具名称</span><input name="toolName" required placeholder="例如：CRM 客户查询" /></label>
          <label><span>OpenAPI 地址</span><input name="toolUrl" type="url" required placeholder="https://api.example.com/openapi.json" /></label>
          <label><span>用途说明</span><textarea name="toolPurpose" rows="3" placeholder="告诉 Agent 什么时候应该调用这个工具"></textarea></label>
          <div class="modal-form-note"><span data-icon="shield-check"></span><span>连接前会校验域名、鉴权方式与 Schema 安全性。</span></div>
        </form>
      `,
      footer: `
        <button class="secondary-button" type="button" data-action="close-modal">取消</button>
        <button class="primary-button" type="submit" form="requestToolForm"><span data-icon="plug"></span>开始连接</button>
      `
    });
  }

  function addKnowledgeFiles(files) {
    if (!files?.length) return;
    const typeByExtension = {
      pdf: ["产品文档", "product"],
      doc: ["策略文档", "strategy"],
      docx: ["策略文档", "strategy"],
      md: ["策略文档", "strategy"],
      txt: ["客户洞察", "insight"],
      csv: ["客户洞察", "insight"]
    };
    Array.from(files).forEach((file, index) => {
      const extension = file.name.split(".").pop()?.toLowerCase() || "txt";
      const [type, typeKey] = typeByExtension[extension] || ["策略文档", "strategy"];
      state.docs.unshift({
        id: `kb-upload-${Date.now()}-${index}`,
        title: file.name.replace(/\.[^.]+$/, ""),
        type,
        typeKey,
        updated: "刚刚",
        owner: "林默",
        chunks: Math.max(1, Math.ceil(file.size / 2400)),
        references: 0,
        summary: `从本地文件上传，正在进行解析与向量化（${(file.size / 1024).toFixed(1)} KB）。`
      });
    });
    state.selectedDocId = state.docs[0].id;
    state.docType = "全部";
    state.docQuery = "";
    renderView();
    showToast("文档已加入知识库", `${files.length} 份文档正在解析与向量化`, "success");
  }

  function handleAction(action, element) {
    switch (action) {
      case "workspace-menu":
        showToast("星云科技", "当前为唯一可访问的企业工作空间", "neutral");
        break;
      case "new-task":
      case "new-conversation":
        startNewConversation();
        break;
      case "help":
        openHelpModal();
        break;
      case "profile":
        showToast("账户中心", "林默 · 星云科技管理员", "neutral");
        break;
      case "create-agent":
      case "manage-agents":
        openCreateAgentModal();
        break;
      case "close-modal":
        closeModal();
        break;
      case "open-agent": {
        const agent = AGENTS.find((item) => item.id === element.dataset.agentId);
        const conversation = getActiveConversation();
        if (conversation) conversation.agent = agent?.name || "NEXA 通用助理";
        setView("chat");
        showToast("Agent 已载入对话", agent?.name || "NEXA 通用助理", "success");
        break;
      }
      case "voice":
        showToast("语音输入", "麦克风已就绪，请开始描述任务", "neutral");
        break;
      case "attach":
        showToast("添加附件", "支持 PDF、Office、图片与音频文件", "neutral");
        break;
      case "prompt-library":
        openCommandPalette();
        break;
      case "stop-generation":
        stopGeneration();
        break;
      case "select-conversation": {
        state.activeConversationId = element.dataset.conversationId;
        renderView();
        break;
      }
      case "agent-picker":
      case "agent-settings":
        showToast("NEXA 通用助理", "当前使用 NEXA Auto 路由策略", "neutral");
        break;
      case "clear-context": {
        const conversation = getActiveConversation();
        if (conversation) conversation.messages = [];
        renderView();
        showToast("会话上下文已重置", "知识引用与工具记录已清空", "neutral");
        break;
      }
      case "context-knowledge":
        setView("knowledge");
        break;
      case "context-tools":
        setView("tools");
        break;
      case "chat-options":
        showToast("对话设置", "模型温度 0.35 · 自动调用工具已开启", "neutral");
        break;
      case "chat-share":
        showToast("分享链接已复制", "拥有工作空间权限的成员可以查看", "success");
        break;
      case "copy-answer": {
        const content = element.closest(".message-row")?.querySelector(".agent-message-content")?.textContent || "";
        copyText(content);
        break;
      }
      case "regenerate": {
        const conversation = getActiveConversation();
        const lastUser = [...(conversation?.messages || [])].reverse().find((message) => message.role === "user");
        if (lastUser) submitChatPrompt(lastUser.content);
        break;
      }
      case "create-task-from-message": {
        state.tasks.unshift({
          id: `TASK-${Math.floor(2850 + Math.random() * 100)}`,
          title: "跟进 Agent 交付结果",
          description: "根据对话结果推进后续动作，并通知相关负责人。",
          agent: "NEXA 通用助理",
          owner: "林默",
          due: "今天 18:00",
          column: "doing",
          progress: 20,
          tone: "mint",
          icon: "list-checks"
        });
        showToast("已转为任务", "可在任务中心继续跟踪执行进度", "success");
        break;
      }
      case "open-source":
        state.selectedDocId = element.dataset.sourceId;
        setView("knowledge");
        break;
      case "filter-tasks":
        state.taskFilter = element.dataset.filter;
        renderView();
        break;
      case "run-task": {
        const task = state.tasks.find((item) => item.id === element.dataset.taskId);
        if (!task) break;
        if (task.column === "review") {
          task.column = "done";
          task.progress = 100;
          task.due = "刚刚完成";
          showToast("审核已通过", "Agent 已继续完成后续交付", "success");
        } else if (task.column === "backlog") {
          task.column = "doing";
          task.progress = 15;
          showToast("任务已启动", `${task.agent} 正在规划执行路径`, "success");
        } else if (task.column === "doing") {
          setView("workflow");
          showToast("已打开执行画布", "可以查看当前 Agent 的节点状态", "neutral");
          return;
        }
        renderView();
        break;
      }
      case "task-menu":
      case "column-menu":
      case "filter-menu":
      case "assignee-menu":
      case "task-view":
        showToast("任务视图", "当前展示所有 Agent 的实时协作看板", "neutral");
        break;
      case "select-node":
        if (Date.now() < suppressFlowClickUntil) break;
        state.workflow.selectedNodeId = element.dataset.nodeId;
        renderView();
        break;
      case "close-inspector":
        state.workflow.selectedNodeId = null;
        renderView();
        break;
      case "duplicate-node": {
        const sourceIndex = state.workflow.nodes.findIndex((node) => node.id === state.workflow.selectedNodeId);
        if (sourceIndex < 0) break;
        const source = state.workflow.nodes[sourceIndex];
        const duplicate = {
          ...source,
          id: `${source.id}-copy-${Date.now().toString().slice(-4)}`,
          index: String(state.workflow.nodes.length + 1).padStart(2, "0"),
          title: `${source.title} 副本`,
          x: Math.min(source.x + 28, 1080),
          y: Math.min(source.y + 130, 390),
          status: "idle"
        };
        state.workflow.nodes.splice(sourceIndex + 1, 0, duplicate);
        state.workflow.selectedNodeId = duplicate.id;
        renderView();
        showToast("节点已复制", "可以继续修改副本配置", "success");
        break;
      }
      case "delete-node": {
        if (state.workflow.nodes.length <= 1) {
          showToast("无法删除", "工作流至少需要保留一个节点", "warning");
          break;
        }
        const index = state.workflow.nodes.findIndex((node) => node.id === state.workflow.selectedNodeId);
        if (index >= 0) state.workflow.nodes.splice(index, 1);
        state.workflow.selectedNodeId = state.workflow.nodes[Math.max(0, index - 1)]?.id || null;
        renderView();
        showToast("节点已删除", "连接关系已自动更新", "neutral");
        break;
      }
      case "save-node":
        showToast("节点设置已保存", "工作流草稿已自动同步", "success");
        break;
      case "add-node":
        openNodePicker();
        break;
      case "choose-node-type": {
        const type = element.dataset.nodeType;
        const maxX = state.workflow.nodes.reduce((max, node) => Math.max(max, node.x), 0);
        const newNode = {
          id: `${type}-${Date.now().toString().slice(-4)}`,
          type,
          index: String(state.workflow.nodes.length + 1).padStart(2, "0"),
          title:
            type === "agent"
              ? "Agent 执行"
              : type === "tool"
                ? "工具调用"
                : type === "condition"
                  ? "条件判断"
                  : "触发器",
          description:
            type === "agent"
              ? "调用模型完成子任务"
              : type === "tool"
                ? "连接企业工具执行动作"
                : type === "condition"
                  ? "根据执行结果选择分支"
                  : "接收外部事件",
          icon: element.dataset.nodeIcon,
          x: Math.min(maxX + 208, 1112),
          y: 208,
          status: "idle"
        };
        state.workflow.nodes.push(newNode);
        state.workflow.selectedNodeId = newNode.id;
        closeModal();
        renderView();
        showToast("节点已添加", "可在右侧面板修改节点配置", "success");
        break;
      }
      case "run-workflow":
      case "workflow-test":
        runWorkflow();
        break;
      case "workflow-undo":
        showToast("撤销", "当前没有可撤销的更改", "neutral");
        break;
      case "workflow-more":
        showToast("工作流操作", "版本管理、复制与发布设置", "neutral");
        break;
      case "workflow-runs":
        setView("runs");
        break;
      case "workflow-settings":
      case "workflow-guide":
        showToast("工作流设置", "当前版本已开启失败重试与运行日志", "neutral");
        break;
      case "zoom-in":
        state.workflow.zoom = Math.min(1.2, state.workflow.zoom + 0.1);
        renderView();
        break;
      case "zoom-out":
        state.workflow.zoom = Math.max(0.7, state.workflow.zoom - 0.1);
        renderView();
        break;
      case "zoom-reset":
        state.workflow.zoom = 1;
        renderView();
        break;
      case "toggle-node-retry":
      case "toggle-node-review":
        element.classList.toggle("on");
        element.setAttribute("aria-checked", String(element.classList.contains("on")));
        break;
      case "filter-docs":
        state.docType = element.dataset.docType;
        renderView();
        break;
      case "select-doc":
        state.selectedDocId = element.dataset.docId;
        renderView();
        break;
      case "upload-knowledge":
        document.getElementById("knowledgeFile")?.click();
        break;
      case "knowledge-settings":
      case "doc-sort":
      case "doc-more":
        showToast("知识库设置", "当前使用混合检索：语义 70% + 关键词 30%", "neutral");
        break;
      case "sync-knowledge":
        showToast("正在同步数据源", "Notion 与飞书知识空间已开始增量同步", "success");
        break;
      case "preview-doc":
        showToast("文档预览", "原文阅读器已准备就绪", "neutral");
        break;
      case "use-doc-in-chat":
        setView("chat");
        showToast("知识范围已更新", "当前对话将优先引用所选文档", "success");
        break;
      case "tool-docs":
        showToast("开发者文档", "支持 OpenAPI 3.0 与自定义函数", "neutral");
        break;
      case "request-tool":
        openRequestToolModal();
        break;
      case "security-details":
        showToast("安全策略", "AES-256 凭据加密 · 全量调用审计 · 最小权限授权", "neutral");
        break;
      case "filter-tools":
        state.toolCategory = element.dataset.category;
        renderView();
        break;
      case "toggle-tool": {
        const tool = state.tools.find((item) => item.id === element.dataset.toolId);
        if (!tool) break;
        tool.enabled = !tool.enabled;
        renderView();
        showToast(tool.enabled ? `${tool.name} 已启用` : `${tool.name} 已暂停`, tool.enabled ? "Agent 现在可以调用该工具" : "已保留连接与授权凭据", tool.enabled ? "success" : "neutral");
        break;
      }
      case "connect-tool": {
        const tool = state.tools.find((item) => item.id === element.dataset.toolId);
        if (!tool) break;
        tool.connected = true;
        tool.enabled = true;
        tool.account = "刚刚完成授权";
        renderView();
        showToast(`${tool.name} 连接成功`, "Agent 已获得最小权限授权", "success");
        break;
      }
      case "configure-tool": {
        const tool = state.tools.find((item) => item.id === element.dataset.toolId);
        openModal({
          eyebrow: "TOOL CONFIGURATION",
          title: `${tool?.name || "工具"} 连接配置`,
          description: "管理授权范围、调用限额与数据访问策略。",
          iconName: tool?.icon || "plug",
          body: `
            <div class="tool-config-summary">
              <span class="tool-logo ${tool?.tone || "mint"}" data-icon="${tool?.icon || "plug"}"></span>
              <div><strong>${escapeHTML(tool?.account || "已连接")}</strong><small>最近调用：3 分钟前 · 状态正常</small></div>
              ${statusDot("连接正常", "ready")}
            </div>
            <div class="modal-form">
              <label><span>单次运行调用上限</span><select><option>10 次</option><option selected>20 次</option><option>50 次</option></select></label>
              <div class="setting-toggle-row"><div><strong>写入操作需确认</strong><small>发送消息、创建任务前暂停等待确认</small></div><button class="switch on" type="button" role="switch" aria-checked="true" data-action="toggle-inline-switch"><span></span></button></div>
              <div class="setting-toggle-row"><div><strong>记录工具返回内容</strong><small>用于调试与运行回放，保留 90 天</small></div><button class="switch on" type="button" role="switch" aria-checked="true" data-action="toggle-inline-switch"><span></span></button></div>
            </div>
          `,
          footer: `<button class="secondary-button" type="button" data-action="close-modal">取消</button><button class="primary-button" type="button" data-action="save-tool-config"><span data-icon="check"></span>保存配置</button>`
        });
        break;
      }
      case "tool-disconnect": {
        const tool = state.tools.find((item) => item.id === element.dataset.toolId);
        if (!tool) break;
        tool.connected = false;
        tool.enabled = false;
        tool.account = "尚未配置";
        renderView();
        showToast(`${tool.name} 已断开`, "相关工作流将无法继续调用该工具", "warning");
        break;
      }
      case "toggle-inline-switch":
        element.classList.toggle("on");
        element.setAttribute("aria-checked", String(element.classList.contains("on")));
        break;
      case "save-tool-config":
        closeModal();
        showToast("工具配置已保存", "新的权限策略将在下一次调用时生效", "success");
        break;
      case "filter-runs":
        state.runFilter = element.dataset.filter;
        renderView();
        break;
      case "toggle-run":
        state.expandedRunId = state.expandedRunId === element.dataset.runId ? null : element.dataset.runId;
        renderView();
        break;
      case "export-runs":
      case "download-run":
        showToast("正在导出运行数据", "CSV 文件将包含完整执行轨迹与用量", "success");
        break;
      case "run-refresh":
        showToast("运行记录已刷新", "所有数据均为最新状态", "success");
        break;
      case "retry-run":
        showToast("已重新发起运行", "Agent 将使用最新凭据执行任务", "success");
        break;
      case "view-run-output":
        showToast("打开运行输出", "结果已同步至任务中心", "neutral");
        break;
      case "run-date-filter":
      case "run-more":
        showToast("运行记录", "当前展示近 7 天的执行数据", "neutral");
        break;
      default:
        break;
    }
  }

  async function copyText(text) {
    try {
      await navigator.clipboard.writeText(text);
      showToast("已复制到剪贴板", "", "success");
    } catch {
      showToast("复制失败", "浏览器未授予剪贴板权限", "warning");
    }
  }

  function bindEvents() {
    document.addEventListener("click", (event) => {
      const viewTarget = event.target.closest("[data-view]");
      if (viewTarget) {
        event.preventDefault();
        setView(viewTarget.dataset.view);
        return;
      }

      const promptTarget = event.target.closest("[data-prompt]");
      if (promptTarget) {
        event.preventDefault();
        const prompt = promptTarget.dataset.prompt;
        if (state.view !== "chat") {
          setView("chat");
          startNewConversation();
        }
        window.setTimeout(() => submitChatPrompt(prompt), 40);
        return;
      }

      const actionTarget = event.target.closest("[data-action]");
      if (actionTarget && !actionTarget.closest(".conversation-more")) {
        event.preventDefault();
        handleAction(actionTarget.dataset.action, actionTarget);
      }
    });

    document.addEventListener("submit", (event) => {
      event.preventDefault();
      const form = event.target;

      if (form.dataset.form === "dashboard-command") {
        const prompt = form.querySelector("input[name='prompt']").value.trim();
        if (!prompt) {
          form.querySelector("input").focus();
          return;
        }
        setView("chat");
        startNewConversation();
        window.setTimeout(() => submitChatPrompt(prompt), 30);
        return;
      }

      if (form.dataset.form === "chat") {
        /*
        const input = form.querySelector("textarea[name='prompt']');
        */
        const promptValue = form.querySelector("textarea").value;
        submitChatPrompt(promptValue);
        return;
      }

      if (form.matches('[data-form="create-agent"]')) {
        const data = new FormData(form);
        const name = String(data.get("agentName") || "新 Agent");
        AGENTS.unshift({
          id: `agent-${Date.now()}`,
          name,
          description: String(data.get("agentRole") || "企业专属智能助手").slice(0, 48),
          icon: "sparkles",
          tone: "mint",
          status: "ready",
          runs: 0,
          accuracy: "—"
        });
        closeModal();
        showToast("Agent 创建成功", `${name} 已加入你的智能体团队`, "success");
        if (state.view === "dashboard") renderView();
        return;
      }

      if (form.matches('[data-form="request-tool"]')) {
        const data = new FormData(form);
        const name = String(data.get("toolName") || "自定义工具");
        state.tools.unshift({
          id: `custom-${Date.now()}`,
          name,
          description: String(data.get("toolPurpose") || "通过 OpenAPI Schema 接入的企业能力"),
          icon: "code",
          tone: "sand",
          category: "开放接口",
          connected: true,
          enabled: true,
          account: "Schema 已校验"
        });
        closeModal();
        if (state.view === "tools") renderView();
        showToast("自定义工具已接入", "Agent 现在可以根据用途说明调用该工具", "success");
      }
    });

    document.addEventListener("input", (event) => {
      if (event.target.matches("#chatComposerInput")) {
        state.chatInput = event.target.value;
        event.target.style.height = "auto";
        event.target.style.height = `${Math.min(event.target.scrollHeight, 160)}px`;
        return;
      }

      if (event.target.matches("#docSearchInput")) {
        state.docQuery = event.target.value;
        const cursor = event.target.selectionStart;
        renderView();
        requestAnimationFrame(() => {
          const input = document.getElementById("docSearchInput");
          if (input) {
            input.focus();
            input.setSelectionRange(cursor, cursor);
          }
        });
        return;
      }

      if (event.target.matches("#toolSearchInput")) {
        state.toolQuery = event.target.value;
        const cursor = event.target.selectionStart;
        renderView();
        requestAnimationFrame(() => {
          const input = document.getElementById("toolSearchInput");
          if (input) {
            input.focus();
            input.setSelectionRange(cursor, cursor);
          }
        });
        return;
      }

      if (event.target.matches("[data-node-field]")) {
        const node = state.workflow.nodes.find((item) => item.id === event.target.dataset.nodeId);
        if (node) node[event.target.dataset.nodeField] = event.target.value;
      }
    });

    document.addEventListener("change", (event) => {
      if (event.target.matches("#knowledgeFile")) {
        addKnowledgeFiles(event.target.files);
        event.target.value = "";
      }
    });

    document.addEventListener("keydown", (event) => {
      const modifier = event.ctrlKey || event.metaKey;
      if (modifier && event.key.toLowerCase() === "k") {
        event.preventDefault();
        openCommandPalette();
        return;
      }

      if (event.key === "Escape") {
        if (!commandOverlay.hidden) closeCommandPalette();
        else if (document.getElementById("modalOverlay")) closeModal();
        else if (!notificationPopover.hidden) closePopovers();
        else closeSidebar();
        return;
      }

      if (!commandOverlay.hidden) {
        if (event.key === "ArrowDown") {
          event.preventDefault();
          state.paletteIndex = Math.min(state.paletteItems.length - 1, state.paletteIndex + 1);
          renderCommandResults(commandInput.value);
          return;
        }
        if (event.key === "ArrowUp") {
          event.preventDefault();
          state.paletteIndex = Math.max(0, state.paletteIndex - 1);
          renderCommandResults(commandInput.value);
          return;
        }
        if (event.key === "Enter") {
          event.preventDefault();
          executeCommandItem(state.paletteIndex);
          return;
        }
      }

      const isTyping = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || "");
      if (!isTyping && event.key.toLowerCase() === "n") {
        event.preventDefault();
        startNewConversation();
      }
    });

    commandInput.addEventListener("input", () => {
      state.paletteIndex = 0;
      renderCommandResults(commandInput.value);
    });

    commandResults.addEventListener("click", (event) => {
      const item = event.target.closest("[data-command-index]");
      if (item) executeCommandItem(Number(item.dataset.commandIndex));
    });

    commandOverlay.addEventListener("click", (event) => {
      if (event.target === commandOverlay) closeCommandPalette();
    });

    document.getElementById("commandTrigger").addEventListener("click", openCommandPalette);
    document.getElementById("notificationTrigger").addEventListener("click", (event) => {
      event.stopPropagation();
      openNotificationPopover();
    });
    document.getElementById("mobileMenu").addEventListener("click", openSidebar);
    document.getElementById("sidebarClose").addEventListener("click", closeSidebar);
    mobileScrim.addEventListener("click", closeSidebar);

    notificationPopover.addEventListener("click", (event) => {
      if (event.target.closest('[data-action="mark-read"]')) {
        notificationPopover.querySelectorAll(".notification-item").forEach((item) => item.classList.remove("unread"));
        document.querySelector(".notification-dot")?.remove();
        showToast("通知已全部标为已读", "", "neutral");
      }
    });

    document.addEventListener("click", (event) => {
      if (
        !notificationPopover.hidden &&
        !notificationPopover.contains(event.target) &&
        !event.target.closest("#notificationTrigger")
      ) {
        closePopovers();
      }
    });

    document.addEventListener("pointerdown", (event) => {
      const nodeElement = event.target.closest(".flow-node");
      if (!nodeElement || event.target.closest(".canvas-zoom")) return;
      const node = state.workflow.nodes.find((item) => item.id === nodeElement.dataset.nodeId);
      if (!node) return;
      nodeDrag = {
        node,
        element: nodeElement,
        startX: event.clientX,
        startY: event.clientY,
        originalX: node.x,
        originalY: node.y,
        moved: false
      };
      nodeElement.classList.add("dragging");
    });

    document.addEventListener("pointermove", (event) => {
      if (!nodeDrag) return;
      const dx = (event.clientX - nodeDrag.startX) / state.workflow.zoom;
      const dy = (event.clientY - nodeDrag.startY) / state.workflow.zoom;
      if (Math.abs(dx) + Math.abs(dy) > 4) nodeDrag.moved = true;
      const nextX = Math.max(16, Math.min(1112, nodeDrag.originalX + dx));
      const nextY = Math.max(48, Math.min(396, nodeDrag.originalY + dy));
      nodeDrag.node.x = Math.round(nextX);
      nodeDrag.node.y = Math.round(nextY);
      nodeDrag.element.style.left = `${nodeDrag.node.x}px`;
      nodeDrag.element.style.top = `${nodeDrag.node.y}px`;
      drawWorkflowEdges();
    });

    document.addEventListener("pointerup", () => {
      if (!nodeDrag) return;
      const wasMoved = nodeDrag.moved;
      nodeDrag.element.classList.remove("dragging");
      nodeDrag = null;
      if (wasMoved) suppressFlowClickUntil = Date.now() + 180;
    });

    window.addEventListener("hashchange", () => {
      const view = location.hash.replace("#", "");
      if (VIEW_META[view] && view !== state.view) setView(view, { silent: true });
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 960) closeSidebar();
    });
  }

  async function loadHealth() {
    try {
      const response = await fetch("/api/health");
      if (!response.ok) throw new Error("Health check failed");
      const health = await response.json();
      state.mode = health.mode === "llm" ? "llm" : "demo";
      const status = document.querySelector(".system-status");
      if (status) {
        status.innerHTML = `<i></i> ${state.mode === "llm" ? "LLM 服务在线" : "演示环境在线"}`;
      }
    } catch {
      state.mode = "demo";
    }
  }

  function init() {
    hydrateIcons();
    bindEvents();
    const initialView = location.hash.replace("#", "");
    setView(VIEW_META[initialView] ? initialView : "dashboard", { silent: true });
    loadHealth();
  }

  init();
})();
