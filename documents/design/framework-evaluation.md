# 框架评估报告 / Framework Evaluation Report

**项目/Project**: 数字分身 (Digital Twin) — local OSS LLM digital twin
**日期/Date**: 2026-06-15
**作者/Author**: Sisyphus/Atlas (automated)

---

## 1. 框架概述 / Framework Overview

### 1.1 superpowers (OHMyOpenCode)

superpowers is a plugin-based framework for the OpenCode CLI environment. It provides a complete AI-agent-native development pipeline:

| Component | Role |
|---|---|
| **Prometheus** | Generates structured implementation plans from specifications. Decomposes work into verifiable, sequential tasks. |
| **Sisyphus** | Routes plan tasks to Atlas sub-agents for execution. Each agent completes one unit, verifies it, then signals readiness. |
| **Atlas** | Sub-agent orchestrator. Receives single tasks, executes them atomically, verifies results via LSP diagnostics and tests. |
| **Momus** | Code review agent. Evaluates output for correctness, quality, and security. Used at critical checkpoints. |
| **Brainstorming** | Pre-work skill that explores user intent, requirements, and design before implementation. |
| **TDD** | Test-driven development skill enforcing write-test → implement → verify flow. |

**Strengths**:
- AI-agent-native: Designed from the ground up for AI-driven development.
- Zero setup overhead in this environment (already configured).
- Integrated plan → execute → review pipeline with verification gates.
- Skills system extensible for project-specific workflows.

**Weaknesses**:
- Tightly coupled to OpenCode CLI; not portable to other agent platforms.
- Relatively new ecosystem; community and documentation still evolving.
- May feel structured/constrained for developers preferring ad-hoc workflows.

**Already configured**: Yes, operational in `/home/oldzhu/whoami/`.

---

### 1.2 BMAD Method

BMAD (Build-Measure-Analyze-Design) is a structured software development methodology emphasizing formal ceremonies, role definitions, and documentation.

| Phase | Purpose |
|---|---|
| **Discovery** | Stakeholder interviews, requirements gathering, feasibility analysis. |
| **Design** | Architecture decision records (ADRs), system design documents, interface specifications. |
| **Development** | Implementation with formal code review gates, multi-role verification (Architect, Developer, Tester). |
| **Deployment** | Staged rollout, acceptance testing, retrospective. |

**Roles**: Architect (design authority), Developer (implementation), Tester (quality assurance).

**Strengths**:
- Rigorous documentation ensures architectural decisions are traceable.
- Multi-role verification catches issues early.
- Strong stakeholder alignment through formal ceremonies.
- ADR format excellent for documenting design decisions.

**Weaknesses**:
- Heavy process overhead: ceremonies, role-switching, documentation-first.
- Not AI-agent-native: roles and ceremonies designed for human teams.
- Steep learning curve for teams unfamiliar with formal methodologies.
- Risk of "process for process's sake" on smaller projects.

---

### 1.3 Standard Agile with AI Agents

Using OpenCode agents in an ad-hoc, lightweight manner without formal methodology.

**Approach**: Issue tasks to agents as needed ("implement X", "fix Y"), review output, iterate. No prescribed plan structure, no formal review gates, no enforced methodology.

**Strengths**:
- Maximum flexibility: adapt workflow moment-to-moment.
- Low ceremony: no documentation overhead unless explicitly requested.
- Easy to start: zero learning curve beyond basic prompt engineering.
- Suitable for exploration, prototyping, and small tasks.

**Weaknesses**:
- No structure guarantee: quality depends entirely on prompt quality and agent capability.
- No built-in verification: must manually request tests, linting, reviews.
- Inconsistent output across sessions without standardized workflow.
- Difficult to reproduce success patterns or hand off between developers.
- No systematic planning: risk of architectural drift on complex projects.

---

## 2. 对比矩阵 / Comparison Matrix

| 维度 / Dimension | superpowers | BMAD Method | Agile Agents (Ad-hoc) |
|---|---|---|---|
| **规划严谨度 / Planning Rigor** | ★★★★★ Prometheus generates structured, verifiable plans with task decomposition and lifecycle tracking. | ★★★★ Formal Discovery → Design phases with stakeholder alignment. ADR format ensures traceability. | ★★★ Ad-hoc: plan quality depends on the prompts given. No enforced structure. |
| **执行自动化 / Execution Automation** | ★★★★★ Sisyphus/Atlas: automated task routing, execution, and verification. LSP diagnostics run automatically. | ★★★ Manual execution by human developers. Ceremonies require human coordination. | ★★★ Manual: must explicitly instruct agents for each step. No automatic orchestration. |
| **质量保证 / Quality Assurance** | ★★★★ Momus review agent + Oracle sub-agents for multi-perspective review. TDD skill enforces test-first. | ★★★★ Multi-role verification (Architect, Developer, Tester). Formal review gates per phase. | ★★★ Quality depends on whether user requests agent review. No systematic gates. |
| **学习曲线 / Learning Curve** | ★★★ Moderate: must understand skill system, Prometheus plans, and Sisyphus execution model. | ★★ Steep: formal ceremonies, role definitions, documentation requirements. Heavy methodology. | ★★★★★ Easy: prompt and iterate. Minimal learning beyond basic agent usage. |
| **AI代理适配 / AI Agent Fit** | ★★★★★ Native: designed specifically for AI agents. All components are skills/sub-agents. | ★★★ Needs adaptation: roles and ceremonies designed for humans. Would require translation. | ★★★★ Flexible: agents used directly, but no structured guidance for complex workflows. |
| **文档集成 / Documentation Integration** | ★★★★ Notepads for learnings, issues, decisions. Plan files as living documents. Built into workflow. | ★★★★★ Core feature: ADRs, design docs, retrospectives are mandatory artifacts. | ★★ Manual: documentation must be explicitly requested. Not integrated. |
| **可重复性 / Reproducibility** | ★★★★ Plan files + notepads create repeatable patterns. Skills enforce consistency. | ★★★★★ Formal process definition ensures repeatability across teams and projects. | ★★ Session-dependent: no guarantee of consistent approach across sessions. |
| **适用规模 / Suitable Scale** | ★★★★ Designed for solo-to-small-team AI-augmented development. Scales with agent parallelism. | ★★★★★ Designed for medium-to-large teams. Scales with formal role structure. | ★★★ Best for solo prototyping and small tasks. Degrades on complex projects. |

### 得分汇总 / Score Summary

| Framework | Total Stars (out of 40) |
|---|---|
| superpowers | 33 |
| BMAD Method | 30 |
| Agile Agents (Ad-hoc) | 25 |

---

## 3. 推荐方案 / Recommendation

### 3.1 首选框架 / Primary Framework: **superpowers (OHMyOpenCode)**

**Rationale**:
- Already configured and operational in this project environment.
- Provides the complete plan → execute → review pipeline that 数字分身 requires.
- AI-agent-native design aligns with the project's AI-driven development approach.
- TDD and verification skills ensure code quality without manual oversight.
- Prometheus plans produce structured, traceable task decomposition suitable for a solo developer managing complexity.

### 3.2 补充方法 / Supplementary: **BMAD ADR Format**

Use BMAD's Architecture Decision Record (ADR) template for documenting design decisions. This adds structured traceability to the superpowers workflow without adopting the full BMAD methodology.

**ADR template location**: `documents/design/adr/` (create as needed, e.g., `adr-001-technology-stack.md`)

### 3.3 日常指导 / Guidance

| Activity | Tool/Method |
|---|---|
| Planning new features | Prometheus (skill) |
| Task execution | Sisyphus + Atlas (automatic via plan) |
| Code review at milestones | Momus (skill) |
| Design decision documentation | BMAD ADR format |
| Bug investigation | Systematic debugging skill |
| Ad-hoc small tasks | Direct agent prompts (Agile Agents style) |

### 3.4 不推荐 / NOT Recommended

- **Full BMAD adoption**: Excessive process overhead for a solo developer. Use ADR format only.
- **Paid frameworks**: Project constraint — local OSS tooling only. superpowers and OpenCode are OSS.
- **Pure ad-hoc (Agile Agents only)**: Insufficient structure for a complex, multi-component project like 数字分身. Risk of architectural drift.

---

## 4. 应用指南 / How to Apply

### 4.1 日常工作流 / Daily Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1.  brainstorm new feature requirements                     │
│      ↓                                                      │
│  2.  Prometheus: generate plan → .sisyphus/plans/           │
│      ↓                                                      │
│  3.  Sisyphus/Atlas: execute tasks one-by-one               │
│      ↓ (after each task)                                    │
│  4.  Verification: lsp_diagnostics, tests, build            │
│      ↓                                                      │
│  5.  Record learnings → .sisyphus/notepads/                 │
│      ↓                                                      │
│  6.  At milestones: Momus review + write ADR if needed       │
│      ↓                                                      │
│  7.  Commit & continue next task                            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 何时使用各方法元素 / When to Use Each Methodology Element

| 场景 / Scenario | 方法 / Method | 理由 / Reason |
|---|---|---|
| 新功能开发 / New feature | Prometheus → Sisyphus | Structured planning with automated execution. |
| 架构决策 / Architecture decision | BMAD ADR format | Traceable, dated, reasoned decisions in `documents/design/adr/`. |
| 重大变更审查 / Major change review | Momus skill | Multi-perspective AI code review. |
| 快速修复 / Quick fix | Agile Agents (ad-hoc) | Direct prompt for speed. No ceremony needed. |
| Bug 调试 / Bug debugging | Systematic debugging skill | Structured approach to root cause analysis. |
| 代码重构 / Refactoring | /refactor command | LSP + AST-grep driven refactoring with TDD verification. |
| 探索性编码 / Exploratory coding | Agile Agents (ad-hoc) | Prototype without formal structure. Switch to Prometheus if promising. |

### 4.3 关键原则 / Key Principles

1. **Plan before build**: Always run Prometheus for features spanning >1 file. Ad-hoc prompts for single-file, single-change work.
2. **Verify every unit**: Sisyphus enforces this automatically. Never skip verification.
3. **Document decisions**: When making a non-obvious design choice, write a brief ADR. Even 3-5 lines is valuable.
4. **Review at milestones**: After completing a plan phase, run Momus before moving on.
5. **Keep notepads updated**: Record patterns, issues, and decisions in `.sisyphus/notepads/` for future sessions.

---

## 附录 / Appendix

### A. 框架选择决策记录 / Framework Selection Decision

**Decision**: Use superpowers as primary methodology for 数字分身 project.

**Context**: The project is a solo-developer, AI-augmented, local OSS LLM digital twin. It requires structured planning, automated execution, and quality verification — all achievable with superpowers' Prometheus → Sisyphus → Momus pipeline. BMAD ADR format supplements for design documentation. Ad-hoc agent usage reserved for quick tasks.

**Consequences**:
- All multi-file features will have a Prometheus plan before implementation.
- All design decisions will be documented in ADR format at `documents/design/adr/`.
- Critical code changes will undergo Momus review.
- Ad-hoc agent prompts acceptable for single-file, single-change work only.

### B. 参考资料 / References

- superpowers GitHub: https://github.com/obra/superpowers
- BMAD Method: Architecture Decision Records (ADR) format
- OpenCode CLI: https://opencode.ai
