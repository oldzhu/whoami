# Digital Twin — Notepad

## Learnings

### Session 2026-06-15
- **Atlas (orchestrator)**: Using DeepSeek v4-pro via OpenCode
- **CRITICAL: Sisyphus-Junior categories BROKEN** — `quick`, `writing`, `deep`, `unspecified-high` all fail:
  - `quick`/`writing`: Use unstable `MiniMax-M2.7` model that claims success but produces zero output
  - `deep`/`unspecified-high`: "Model not configured for category" errors
  - **WORKAROUND**: Use `subagent_type="general"` instead of `category` — this agent uses the working `deepseek-v4-pro` model
  - **Impact**: All tasks must use `subagent_type="general"` regardless of plan's recommended category
- **Subagent issue**: librarian/oracle/momus/metis agents use separate API configs — they timed out or got "invalid api key"
- **Hardware**: AMD AI 395 Max + RTX 3080 16GB laptop. Project uses llama.cpp for hardware flexibility
- **Constraint**: 100% local OSS LLM — no remote API calls for runtime inference

## Decisions
- Framework evaluation (Task 4) will recommend superpowers as primary execution framework + BMAD methodology for design rigor
- Bilingual docs: every .md file uses `## 中文 / English` section header pattern

## Issues
- Momus/Metis timing out — infrastructure issue, not project blocking
- **ALERT**: All Sisyphus-Junior category models broken — need to configure in opencode.json or oh-my-openagent.json. Using general agent as workaround.

### Task 4: Framework Evaluation Report
- Created `/home/oldzhu/whoami/documents/design/framework-evaluation.md` (208 lines)
- Bilingual format: every section uses ## 中文 / English headers
- Comparison matrix with 8 dimensions across 3 frameworks (superpowers, BMAD, Agile Agents)
- Recommendation: superpowers primary, BMAD ADR format supplementary, Agile Agents for quick tasks only
- Included daily workflow diagram and scenario-based guidance table
