<div align="center">
  <img width="800" src="./assets/header.svg" alt="terminal header" />
</div>

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gancheng-luo-andy/) [![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:andy8647lgc@gmail.com) [![Unsplash](https://img.shields.io/badge/Unsplash-7M_views-000000?style=flat-square&logo=unsplash&logoColor=white)](https://unsplash.com/@andy8647)

</div>

---

## About

```python
andy = {
    "is": "a full-stack engineer who builds agents — heaviest on the backend",
    "agent_layer": [
        "RAG — chunking, hybrid retrieval, reranking, citations",
        "prompt & context engineering — what goes in the window, and what doesn't",
        "MCP servers & tool calling — agents that change state, not just describe it",
        "evals — measure the pipeline instead of trusting the demo",
    ],
    "backend_under_it": [
        "FastAPI · SQLAlchemy · Alembic · Postgres · Redis",
        "Kafka for the async seams, Kubernetes and Docker to run it",
        "a model layer that swaps Anthropic/OpenAI/DeepSeek/Gemini",
    ],
    "also": "computer vision, trained and shipped on-device",
    "off_duty": "photography — 7M views / 57K downloads on Unsplash",
    "education": [
        "MIT (Artificial Intelligence) @ UNSW Sydney (2025–2026)",
        "BSc Computer Science @ University of Toronto",
    ],
    "before_agents": "4 years full-stack — commonsku, SnapPay",
    "based_in": "Shanghai · remote",
}
```

---

## What I'm Building

**Agent harness UI & tooling** — extensions for the [pi](https://pi.dev) coding agent, built because a long-running agent kept breaking. Sorted by npm downloads (last month).

[github.com/Andy8647/pi-toolbox](https://github.com/Andy8647/pi-toolbox): one consistent frame around every tool call — built-ins, MCP, subagents — with bash syntax highlighting. [![npm](https://img.shields.io/npm/dm/@andy8647/pi-toolbox?style=flat-square&label=%20&color=CB3837&logo=npm)](https://www.npmjs.com/package/@andy8647/pi-toolbox)

[github.com/Andy8647/pi-starline](https://github.com/Andy8647/pi-starline): **Starline** — a Starship-inspired statusline and Opencode-style TUI for pi. Pill footer with directory, git branch & status, runtime detection, context usage, token counts and cost at a glance; themeable colour palette with `$ref` expansion, fully custom `footerFormat` templates, `model`/`thinking` segments; bordered editor with accent rail, per-mode cursor styles and mouse selection. Forked from pi-zentui, since diverged well past upstream. [![stars](https://img.shields.io/github/stars/Andy8647/pi-starline?style=flat-square&label=%20&color=58a6ff&logo=github)](https://github.com/Andy8647/pi-starline)

[github.com/Andy8647/pi-balance](https://github.com/Andy8647/pi-balance): real-time API provider balance in the pi status bar — DeepSeek, Moonshot, OpenRouter, Codex and more.

[github.com/Andy8647/pi-ide-context](https://github.com/Andy8647/pi-ide-context): `/ide` for pi. Select text in Neovim or VS Code, switch to the agent — it already knows the file, cursor and selection. No copy-paste. [![npm](https://img.shields.io/npm/dm/pi-ide-context?style=flat-square&label=%20&color=CB3837&logo=npm)](https://www.npmjs.com/package/pi-ide-context)

[github.com/Andy8647/pi-agent-loop](https://github.com/Andy8647/pi-agent-loop): cross-provider rate-limit detection and auto-resume. Tells a soft quota limit apart from a hard 403, waits for the real reset, picks the task back up. [![npm](https://img.shields.io/npm/dm/@andy8647/pi-agent-loop?style=flat-square&label=%20&color=CB3837&logo=npm)](https://www.npmjs.com/package/@andy8647/pi-agent-loop)

```bash
pi install npm:@andy8647/pi-agent-loop
pi install npm:pi-ide-context
pi install npm:@andy8647/pi-toolbox
```

**Agent internals** — context engineering and the failure modes underneath

[github.com/Andy8647/superpowers](https://github.com/Andy8647/superpowers) (fork): plan generation kept dying on long runs — past ~119K tokens prompt cache dropped to zero, and a 3,000-line plan in one response got the stream killed. The fix was structural, not prompt-level: split plans into an index plus self-contained per-task files, so the controller reads only the index and each subagent reads only its own task. 9 files, +216/−108.

[github.com/Andy8647/pdf-injection-scanner](https://github.com/Andy8647/pdf-injection-scanner): finds prompt injection hidden inside PDFs before an agent reads them — white text, 0.1pt fonts, content positioned off-page. [![stars](https://img.shields.io/github/stars/Andy8647/pdf-injection-scanner?style=flat-square&label=%20&color=58a6ff&logo=github)](https://github.com/Andy8647/pdf-injection-scanner)

[github.com/Andy8647/agent-atlas](https://github.com/Andy8647/agent-atlas): interactive learning platform for the agent application layer — ReAct through harness engineering.

**Computer vision** — trained, converted, shipped to a device

[github.com/Andy8647/MahjongVis](https://github.com/Andy8647/MahjongVis): real-time mahjong tile recognition on iPhone. 3,713 self-annotated images across 42 classes, YOLOv8s trained 150 epochs, converted to CoreML with built-in NMS, running live through SwiftUI + AVCaptureSession.

---

## Tech

<div align="center">

**Agents & LLM** &nbsp;
![MCP](https://img.shields.io/badge/MCP-6E40C9?style=flat-square)
![RAG](https://img.shields.io/badge/RAG-FF6F00?style=flat-square)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-D97757?style=flat-square&logo=anthropic&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![DeepSeek](https://img.shields.io/badge/DeepSeek-4D6BFE?style=flat-square)

**Backend & Infra** &nbsp;
[![Skills](https://skillicons.dev/icons?i=python,fastapi,postgres,redis,kafka,docker,kubernetes,nginx&theme=dark)](https://skillicons.dev)

**Frontend** &nbsp;
[![Skills](https://skillicons.dev/icons?i=ts,react,nextjs,tailwind,vite&theme=dark)](https://skillicons.dev)

**Vision & On-device** &nbsp;
[![Skills](https://skillicons.dev/icons?i=pytorch,swift&theme=dark)](https://skillicons.dev)
![YOLOv8](https://img.shields.io/badge/YOLOv8-111111?style=flat-square&logo=yolo&logoColor=00FFFF)
![CoreML](https://img.shields.io/badge/CoreML-000000?style=flat-square&logo=apple&logoColor=white)

</div>

---

<div align="center">
  <img height="180" src="https://raw.githubusercontent.com/Andy8647/Andy8647/output/profile-summary-card-output/github_dark/2-most-commit-language.svg" />
</div>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Andy8647/Andy8647/output/github-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Andy8647/Andy8647/output/github-snake.svg" />
    <img alt="github-snake" src="https://raw.githubusercontent.com/Andy8647/Andy8647/output/github-snake-dark.svg" />
  </picture>
</div>

<div align="center">

![Profile Views](https://komarev.com/ghpvc/?username=Andy8647&color=58a6ff&style=flat-square&label=visitors)

</div>
