import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { existsSync, readFileSync } from "node:fs";
import { extname, join, normalize, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL(".", import.meta.url));

function loadDotEnv() {
  const envPath = join(ROOT, ".env");
  if (!existsSync(envPath)) return;

  const text = requireText(envPath);
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const separator = line.indexOf("=");
    if (separator < 1) continue;
    const key = line.slice(0, separator).trim();
    let value = line.slice(separator + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (!(key in process.env)) process.env[key] = value;
  }
}

function requireText(path) {
  try {
    return readFileSync(path, "utf8");
  } catch {
    return "";
  }
}

loadDotEnv();

const PORT = Number(process.env.PORT || 4173);
// Model access stays server-side so API keys are never exposed to the browser.
const CONFIG = {
  apiKey: process.env.LLM_API_KEY || "",
  baseUrl: (process.env.LLM_BASE_URL || "https://api.openai.com/v1").replace(/\/+$/, ""),
  model: process.env.LLM_MODEL || "gpt-4.1-mini"
};

const KNOWLEDGE = [
  {
    id: "kb-growth-playbook",
    title: "2026 Q4 增长运营手册",
    type: "策略文档",
    updated: "2026-11-12",
    content:
      "Q4 北极星指标为周活跃团队数。核心抓手是新用户首日激活、模板复用率和团队邀请率。运营周报需要同时展示漏斗转化、渠道质量与流失原因，并对异常指标给出归因假设。"
  },
  {
    id: "kb-product-release",
    title: "Agent Studio 2.4 发布说明",
    type: "产品文档",
    updated: "2026-11-10",
    content:
      "Agent Studio 2.4 新增工作流版本管理、人工审批节点和运行回放。支持接入飞书、企业微信、Notion 与自定义 REST API。运行数据保留 90 天。"
  },
  {
    id: "kb-competitor",
    title: "AI Agent 产品竞品追踪",
    type: "市场情报",
    updated: "2026-11-13",
    content:
      "近期竞品重点集中在多 Agent 协作、可视化编排和企业级权限审计。客户最关注可观测性、数据隔离和 SaaS 工具连接数量。差异机会在于低门槛中文工作流与过程可解释性。"
  },
  {
    id: "kb-customer-voice",
    title: "客户反馈主题聚类（11 月）",
    type: "客户洞察",
    updated: "2026-11-11",
    content:
      "本月反馈中出现频率最高的问题依次是：工作流节点配置学习成本、飞书通知格式不灵活、运行失败原因不透明。正面反馈集中在知识库回答准确率和任务自动拆分能力。"
  },
  {
    id: "kb-security",
    title: "企业数据安全与权限规范",
    type: "制度规范",
    updated: "2026-10-28",
    content:
      "知识库检索遵循最小权限原则。敏感文档不得发送至外部模型上下文；对外工具调用需记录发起人、Agent、参数摘要和返回状态。生产工作流发布前必须完成人工审批。"
  }
];

const METRICS = {
  product: {
    activeTeams: 1286,
    activeTeamsChange: 12.4,
    activationRate: 61.8,
    activationChange: 3.2,
    weeklyRetention: 74.6,
    retentionChange: -1.1,
    topChannel: "产品内邀请",
    topChannelShare: 38.2
  },
  growth: {
    newUsers: 4820,
    newUsersChange: 8.7,
    activationRate: 58.3,
    activationChange: 2.6,
    inviteRate: 22.4,
    inviteChange: 4.1
  }
};

const TOOLS = [
  {
    type: "function",
    function: {
      name: "search_knowledge",
      description: "在企业知识库中检索制度、产品说明、市场情报和客户洞察。回答涉及内部事实时应优先调用。",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string", description: "检索关键词或问题" },
          limit: { type: "integer", description: "返回条数，1-5", minimum: 1, maximum: 5 }
        },
        required: ["query"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "get_project_metrics",
      description: "读取产品运营仪表盘中的实时指标，包括活跃团队、激活率、留存和渠道数据。",
      parameters: {
        type: "object",
        properties: {
          scope: {
            type: "string",
            enum: ["product", "growth"],
            description: "指标范围"
          }
        },
        required: ["scope"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "create_follow_up",
      description: "在任务中心创建一个可追踪的后续行动。仅当用户要求推进、安排或创建任务时调用。",
      parameters: {
        type: "object",
        properties: {
          title: { type: "string", description: "行动标题" },
          owner: { type: "string", description: "负责人" },
          due: { type: "string", description: "截止日期，ISO 格式" }
        },
        required: ["title", "owner", "due"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "send_notification",
      description: "将最终结果发送到指定协作渠道。执行前应确保用户明确要求发送。",
      parameters: {
        type: "object",
        properties: {
          channel: {
            type: "string",
            enum: ["feishu", "wecom", "email"],
            description: "发送渠道"
          },
          summary: { type: "string", description: "发送内容摘要" }
        },
        required: ["channel", "summary"]
      }
    }
  }
];

// The prompt defines execution boundaries, while tool schemas define callable capabilities.
const SYSTEM_PROMPT = `你是 NEXA Agent，一名服务企业知识工作者的智能执行助理。
你的目标不是只回答问题，而是自主完成用户交付的任务。工作原则：
1. 先理解目标、约束与期望交付物，再决定步骤。
2. 涉及企业内部事实、产品数据、市场情报时，必须调用提供的工具，不要编造。
3. 工具调用失败时说明影响，并给出可执行的替代方案。
4. 最终回答使用简洁中文。优先给出结论、关键数据、风险与下一步，不展示隐藏思维过程。
5. 只在用户明确要求推进或发送时调用写操作工具。
6. 不要声称执行了工具未返回的动作。`;

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2"
};

function sendJson(response, status, payload) {
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store"
  });
  response.end(JSON.stringify(payload));
}

async function readJson(request) {
  let body = "";
  for await (const chunk of request) {
    body += chunk;
    if (body.length > 1_000_000) throw new Error("请求体过大");
  }
  return body ? JSON.parse(body) : {};
}

function executeTool(name, args) {
  if (name === "search_knowledge") {
    const terms = String(args.query || "")
      .toLowerCase()
      .split(/[\s，,。？?]+/)
      .filter(Boolean);
    const limit = Math.min(Math.max(Number(args.limit) || 3, 1), 5);
    const scored = KNOWLEDGE.map((item) => {
      const haystack = `${item.title} ${item.content} ${item.type}`.toLowerCase();
      const score = terms.reduce((sum, term) => sum + (haystack.includes(term) ? 1 : 0), 0);
      return { ...item, score };
    })
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map(({ score, ...item }) => item);

    return {
      ok: true,
      query: args.query,
      results: scored.length ? scored : KNOWLEDGE.slice(0, Math.min(limit, 3)),
      count: scored.length,
      detail: `命中 ${scored.length || Math.min(limit, 3)} 篇企业知识`
    };
  }

  if (name === "get_project_metrics") {
    const scope = args.scope === "growth" ? "growth" : "product";
    return {
      ok: true,
      scope,
      period: "2026-11-08 至 2026-11-14",
      metrics: METRICS[scope],
      detail: "已读取最新运营指标"
    };
  }

  if (name === "create_follow_up") {
    return {
      ok: true,
      taskId: `TASK-${Math.floor(2000 + Math.random() * 7000)}`,
      title: args.title,
      owner: args.owner,
      due: args.due,
      status: "pending",
      detail: "已创建待办并通知负责人"
    };
  }

  if (name === "send_notification") {
    return {
      ok: true,
      channel: args.channel,
      messageId: `MSG-${Date.now().toString().slice(-6)}`,
      detail: `已发送至${channelLabel(args.channel)}`
    };
  }

  return { ok: false, error: `未知工具：${name}` };
}

function channelLabel(channel) {
  return { feishu: "飞书", wecom: "企业微信", email: "邮箱" }[channel] || channel;
}

function toolLabel(name) {
  return {
    search_knowledge: "企业知识检索",
    get_project_metrics: "读取项目指标",
    create_follow_up: "创建后续任务",
    send_notification: "发送协作通知"
  }[name] || name;
}

function toolDetail(name, result) {
  if (name === "search_knowledge") {
    return `检索 ${result.results?.length || 0} 篇知识文档`;
  }
  if (name === "get_project_metrics") {
    return "获取活跃、激活与留存数据";
  }
  return result.detail || "工具执行完成";
}

async function callModel(messages, tools) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 35_000);

  try {
    const response = await fetch(`${CONFIG.baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${CONFIG.apiKey}`
      },
      body: JSON.stringify({
        model: CONFIG.model,
        messages,
        tools,
        tool_choice: "auto",
        temperature: 0.35
      }),
      signal: controller.signal
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`模型接口返回 ${response.status}: ${errorText.slice(0, 240)}`);
    }
    return await response.json();
  } finally {
    clearTimeout(timeout);
  }
}

async function runAgent(payload) {
  const incomingMessages = Array.isArray(payload.messages) ? payload.messages : [];
  const sanitized = incomingMessages
    .filter((item) => item && ["user", "assistant"].includes(item.role))
    .slice(-12)
    .map((item) => ({
      role: item.role,
      content: String(item.content || "").slice(0, 12_000)
    }));

  if (!sanitized.length) throw new Error("消息不能为空");
  if (!CONFIG.apiKey) {
    return { ...createDemoResponse(sanitized.at(-1).content), mode: "demo" };
  }

  const messages = [{ role: "system", content: SYSTEM_PROMPT }, ...sanitized];
  const toolTrace = [];
  let sources = [];

  // A bounded tool loop prevents runaway calls while allowing multi-step work.
  for (let round = 0; round < 4; round += 1) {
    const completion = await callModel(messages, TOOLS);
    const message = completion?.choices?.[0]?.message;
    if (!message) throw new Error("模型返回为空");

    const toolCalls = Array.isArray(message.tool_calls) ? message.tool_calls : [];
    messages.push(message);

    if (!toolCalls.length) {
      return {
        mode: "llm",
        model: CONFIG.model,
        content: message.content || "任务已完成。",
        toolTrace,
        sources,
        plan: buildPlan(toolTrace)
      };
    }

    for (const call of toolCalls) {
      let args = {};
      try {
        args = JSON.parse(call.function?.arguments || "{}");
      } catch {
        args = {};
      }

      const name = call.function?.name || "unknown_tool";
      const result = executeTool(name, args);
      if (name === "search_knowledge" && result.results) {
        sources = result.results.map((item) => ({
          id: item.id,
          title: item.title,
          type: item.type
        }));
      }

      toolTrace.push({
        name,
        label: toolLabel(name),
        detail: toolDetail(name, result),
        status: result.ok ? "done" : "error"
      });

      messages.push({
        role: "tool",
        tool_call_id: call.id,
        content: JSON.stringify(result)
      });
    }
  }

  throw new Error("工具调用轮次超过上限");
}

function buildPlan(toolTrace) {
  const plan = ["理解目标与交付标准"];
  toolTrace.forEach((tool) => plan.push(tool.label));
  plan.push("校验结果并生成交付物");
  return plan;
}

function createDemoResponse(prompt) {
  const text = String(prompt || "");
  const isWeekly = /周报|运营|数据|复盘/.test(text);
  const isCompetitor = /竞品|市场|雷达|分析/.test(text);
  const isMeeting = /会议|纪要|行动项|安排/.test(text);

  if (isWeekly) {
    const trace = [
      {
        name: "get_project_metrics",
        label: "读取项目指标",
        detail: "获取活跃、激活与留存数据",
        status: "done"
      },
      {
        name: "search_knowledge",
        label: "企业知识检索",
        detail: "命中 2 篇增长与反馈文档",
        status: "done"
      },
      {
        name: "create_follow_up",
        label: "创建后续任务",
        detail: "已创建留存专项分析任务",
        status: "done"
      }
    ];
    return {
      content: `### 本周产品运营周报已完成

我汇总了 11 月 8 日至 14 日的项目指标、增长策略与客户反馈，核心结论如下：

**整体表现**
- 活跃团队达到 **1,286**，环比增长 **12.4%**，增速高于近四周均值。
- 新用户激活率为 **61.8%**，环比提升 **3.2 个百分点**，主要来自产品内邀请渠道。
- 周留存率为 **74.6%**，环比下降 **1.1 个百分点**，需要关注新团队第二周的模板使用深度。

**关键洞察**
客户反馈显示，工作流节点配置仍是主要学习门槛；同时，知识库回答准确率是当前最受认可的差异化能力。

**下周建议**
1. 针对未复用模板的新团队上线 3 步引导流程。
2. 对留存下降团队做分渠道回访，验证是否是激活质量波动。
3. 将高频工作流整理为首周推荐模板，提升团队邀请率。

已同步生成「新团队留存专项分析」待办，负责人：周青，截止：11 月 18 日。`,
      toolTrace: trace,
      sources: [
        { id: "kb-growth-playbook", title: "2026 Q4 增长运营手册", type: "策略文档" },
        { id: "kb-customer-voice", title: "客户反馈主题聚类（11 月）", type: "客户洞察" }
      ],
      plan: buildPlan(trace)
    };
  }

  if (isCompetitor) {
    const trace = [
      {
        name: "search_knowledge",
        label: "企业知识检索",
        detail: "命中 2 篇市场与产品情报",
        status: "done"
      }
    ];
    return {
      content: `### 竞品动态速览

本轮竞品变化集中在三个方向：

- **多 Agent 协作**：竞品正在强化角色分工与任务接力，但配置复杂度较高。
- **可视化编排**：版本管理、人工审批和运行回放成为企业采购的必选项。
- **连接生态**：飞书、企业微信、Notion 与 Webhook 是高频集成目标。

**机会判断**
NEXA 应继续放大“中文任务理解 + 低门槛工作流 + 全链路可观测”的组合优势。建议优先补齐失败原因解释和通知模板能力，这两项在客户反馈中的影响最直接。

**建议动作**
本周形成一页式竞品对比，重点标注权限审计、人工审批和工具连接数量。`,
      toolTrace: trace,
      sources: [
        { id: "kb-competitor", title: "AI Agent 产品竞品追踪", type: "市场情报" },
        { id: "kb-customer-voice", title: "客户反馈主题聚类（11 月）", type: "客户洞察" }
      ],
      plan: buildPlan(trace)
    };
  }

  if (isMeeting) {
    const trace = [
      {
        name: "search_knowledge",
        label: "企业知识检索",
        detail: "检索会议与项目上下文",
        status: "done"
      },
      {
        name: "create_follow_up",
        label: "创建后续任务",
        detail: "已生成 3 条会议行动项",
        status: "done"
      }
    ];
    return {
      content: `### 会议行动项已整理

**结论**
本次会议确认了 Agent Studio 2.4 的发布范围，并决定将“运行失败原因解释”纳入首发体验。

**行动项**
1. 产品：补充三类失败场景的说明文案，负责人陈曦，11 月 16 日前完成。
2. 研发：完善工作流运行回放，负责人周青，11 月 18 日前完成。
3. 运营：制作 5 分钟客户演示视频，负责人林默，11 月 19 日前完成。

**风险**
人工审批节点仍依赖权限配置，需要在灰度前完成一次全链路验证。`,
      toolTrace: trace,
      sources: [{ id: "kb-product-release", title: "Agent Studio 2.4 发布说明", type: "产品文档" }],
      plan: buildPlan(trace)
    };
  }

  const trace = [
    {
      name: "search_knowledge",
      label: "企业知识检索",
      detail: "检索相关企业内部知识",
      status: "done"
    }
  ];
  return {
    content: `### 任务已拆解

我已理解你的目标，并基于企业知识库完成了第一轮信息整理。

**建议执行路径**
1. 明确交付物格式与截止时间。
2. 调用项目指标、知识库和协作工具补齐事实。
3. 生成初稿后执行一次完整性与一致性校验。
4. 经你确认后发送到指定渠道。

当前处于本地演示模式。配置 \`LLM_API_KEY\` 后，Agent 会根据实际任务自主选择工具、执行多轮推理并返回结果。你也可以继续补充目标、受众或截止时间，我会据此细化方案。`,
    toolTrace: trace,
    sources: [{ id: "kb-product-release", title: "Agent Studio 2.4 发布说明", type: "产品文档" }],
    plan: buildPlan(trace)
  };
}

async function handleApi(request, response, pathname) {
  if (pathname === "/api/health" && request.method === "GET") {
    sendJson(response, 200, {
      ok: true,
      mode: CONFIG.apiKey ? "llm" : "demo",
      model: CONFIG.apiKey ? CONFIG.model : "local-demo",
      tools: TOOLS.map((tool) => tool.function.name),
      updatedAt: new Date().toISOString()
    });
    return true;
  }

  if (pathname === "/api/agent/run" && request.method === "POST") {
    try {
      const payload = await readJson(request);
      const result = await runAgent(payload);
      sendJson(response, 200, { ok: true, ...result });
    } catch (error) {
      console.error("[Agent]", error.message);
      if (CONFIG.apiKey) {
        const fallback = createDemoResponse("继续完成任务");
        sendJson(response, 200, {
          ok: true,
          ...fallback,
          mode: "demo-fallback",
          warning: error.message
        });
      } else {
        sendJson(response, 400, { ok: false, error: error.message });
      }
    }
    return true;
  }

  return false;
}

async function serveStatic(response, pathname) {
  const requested = pathname === "/" ? "/index.html" : decodeURIComponent(pathname);
  const normalized = normalize(requested).replace(/^([/\\])+/, "");
  const filePath = resolve(join(ROOT, normalized));

  if (!filePath.startsWith(resolve(ROOT))) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }

  try {
    const fileStat = await stat(filePath);
    if (!fileStat.isFile()) throw new Error("Not a file");
    const content = await readFile(filePath);
    response.writeHead(200, {
      "Content-Type": MIME_TYPES[extname(filePath).toLowerCase()] || "application/octet-stream",
      "Cache-Control": extname(filePath) === ".html" ? "no-cache" : "public, max-age=3600"
    });
    response.end(content);
  } catch {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("404 - 页面不存在");
  }
}

const server = createServer(async (request, response) => {
  const url = new URL(request.url || "/", `http://${request.headers.host || "localhost"}`);

  if (url.pathname.startsWith("/api/")) {
    const handled = await handleApi(request, response, url.pathname);
    if (!handled) sendJson(response, 404, { ok: false, error: "API 不存在" });
    return;
  }

  await serveStatic(response, url.pathname);
});

server.listen(PORT, () => {
  const mode = CONFIG.apiKey ? `LLM · ${CONFIG.model}` : "本地演示模式";
  console.log(`\n  NEXA Agent Workspace`);
  console.log(`  http://localhost:${PORT}`);
  console.log(`  Runtime: ${mode}`);
  console.log(`  Stop: Ctrl+C\n`);
});
