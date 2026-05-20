# ziwei-ai-html-report

离线紫微斗数报告工具包：输入出生信息或命盘上下文，输出可保存与分享的单文件 HTML 报告。

本目录为完整开源内容，复制本文件夹即可运行，不索引仓库其他目录。

## 你是哪类用户

- **普通用户（最快）**：看 `30 秒上手`，复制命令直接生成上下文。
- **Agent 用户（Codex/Claude/Minimax）**：看 `Agent 通用契约`，按统一输入/输出协议调用。
- **开发者（二次开发）**：看 `开发者入口`，了解算法口径、测试与扩展点。

## 30 秒上手

```bash
python3 tools/ziwei_offline.py \
  --solar 1996-01-06 \
  --time 11:30 \
  --gender female \
  --birthplace "广东省佛山市顺德区" \
  --target-year 2026 \
  --format json
```

运行后会输出：
- `chart`（结构化命盘）
- `natalContext`（综合批注输入）
- `yearlyContext`（流年输入）
- `klineContext`（K 线输入）

## GitHub 发布版保证

- 本目录可单独复制、克隆、运行，不依赖仓库其它目录。
- 核心排盘与上下文生成仅依赖 Python 标准库，不依赖 Node、npm、app 运行时或第三方排盘库。
- 在线地理编码只是增强能力，不是必需前提；坐标失败时会自动回退离线城市表或标准时。
- 对 Agent 的输入、输出与校验契约以 `SKILL.md`、`prompts.md`、`tools/ziwei_offline.py` 为准。

## 标准输入示例

展示层（给终端用户）：
- 阳历生日：1996年1月6日
- 农历生日：可不填（自动计算）
- 出生时间：11:30
- 性别：女
- 出生地：广东省佛山市顺德区

机器层（给脚本或 Agent）：
- `solar=1996-01-06`
- `time=11:30`（或 `hour=11`）
- `gender=female`
- `birthplace=广东省佛山市顺德区`
- `target-year=2026`（可选）

## Agent 通用契约

- **输入契约**：出生资料或已存在上下文（二选一）。
- **生成契约**：任意模型可用，但需遵守 `prompts.md` 的格式约束。
- **交付契约**：最终应产出单文件 HTML，且保留免责声明与 K 线校验规则。
- **失败契约**：输入越界、上下文不完整、K 线校验失败时必须停止断语或停止交付，不得脑补星曜事实。

### 对话式 Agent 兼容声明

本项目为 **agent-agnostic 协议**，支持在 Codex、Claude Code、Minimax 等对话式 Agent 中完成端到端报告生成。

- 可实现能力：通过对话生成 `natalContext/yearlyContext/klineContext`，并组装最终单文件 HTML 报告。
- 成功前提：目标 Agent 需严格遵守本目录的输入/输出契约与校验要求。
- 影响因素：具体成功率取决于 Agent 的指令遵循能力、上下文窗口与运行环境（如网络地理编码可用性）。
- 稳定性建议：优先使用本仓库提供的标准输入示例与 `examples/` 模板，降低格式偏差。

推荐阅读顺序：
1. `SKILL.md`
2. `prompts.md`
3. `report-template.html`

## 开发者入口

- 规则基线：`docs/rules-baseline.md`
- 规则映射：`RULE_MATRIX.md`
- 核心引擎：`tools/ziwei_offline.py`
- 语义数据：`tools/knowledge_semantics.json`
- 地理回退：`tools/cn_locations.json`
- 测试：`tests/test_ziwei_offline.py`
- 发布配套：`LICENSE`、`.github/workflows/ci.yml`、`RELEASE_CHECKLIST.md`

运行测试：

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## 真太阳时口径

- 固定 UTC+8，不回溯历史夏令时。
- 公式：`标准时 + (经度-120)*4 分钟 + 时间方程`。
- 地理编码模式：`hybrid`（在线优先，失败回退 `tools/cn_locations.json`）。
- 若无可用经纬度，会回退标准时并在输出中标注。

### 推荐运行模式

- 默认混合模式：`python3 tools/ziwei_offline.py --solar 1996-01-06 --time 11:30 --gender female --birthplace "广东省佛山市顺德区" --target-year 2026 --format json`
- 纯离线模式：在默认命令后追加 `--geocode-mode offline`
- 手工坐标模式：用 `--longitude 113.2932 --latitude 22.8054` 替代 `--birthplace`
- 禁用真太阳时：追加 `--disable-true-solar-time`

## 常见失败与排查

- `日期格式必须为 YYYY-MM-DD`：检查 `--solar` 是否是 ISO 日期。
- `time 格式必须为 HH:mm`：检查 `--time` 是否补零且范围合法。
- `必须提供 --time 或 --hour`：二者至少提供一个，`--time` 优先。
- 出生地无法解析：改用 `--geocode-mode offline`，或直接传 `--longitude/--latitude`。
- 日期超出 1900-01-31 至 2100-12-31：本发布版不会继续断语，需补充上下文或改用其它口径。

## 示例文件

- `examples/input.standard.json`：标准输入 JSON
- `examples/context.sample.md`：上下文输入样例
- `examples/quickstart.sh`：一键演示脚本
- `examples/output.sample.json`：输出结构样例
