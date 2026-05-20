# Release Checklist

发布前逐项确认：

- `python3 -m unittest discover -s tests -p "test_*.py"` 通过。
- `bash examples/quickstart.sh` 能输出合法 JSON。
- `python3 tools/ziwei_offline.py --help` 与 README 示例一致。
- `README.md`、`SKILL.md`、`prompts.md` 不包含私有路径、悬空符号或仓库外依赖说明。
- `SKILL.md` frontmatter 只包含 `name` 与 `description`，且 `description` 只描述触发条件。
- `LICENSE`、`.gitignore`、`.github/workflows/ci.yml` 已存在。
- `report-template.html` 仍保留免责声明与 K 线完整性校验逻辑。
- 默认 `hybrid`、纯离线 `offline`、手工坐标三条使用路径都在 README 中可见。
