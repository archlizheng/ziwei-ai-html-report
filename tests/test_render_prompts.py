import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import render_prompts as rp  # noqa: E402
import ziwei_offline as zw  # noqa: E402


class RenderPromptsTests(unittest.TestCase):
    def setUp(self):
        self.chart = zw.generate_chart(
            1996, 1, 6, 11, "female", 2026, minute=30, use_true_solar_time=False
        )
        self.payload = zw.build_payload(self.chart, 2026)

    def test_render_creates_prompt_files_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp)
            manifest = rp.render_all_prompts(self.payload, out, work_root=out)
            prompts_dir = out / "prompts"
            for name in (
                "natal.system.md",
                "natal.user.md",
                "yearly.system.md",
                "yearly.user.md",
                "kline.system.md",
                "kline.user.md",
            ):
                self.assertTrue((prompts_dir / name).exists(), msg=name)
            self.assertTrue((out / "prompt-manifest.json").exists())
            self.assertEqual(len(manifest["promptHashes"]), 6)
            self.assertEqual(manifest["version"], "2")
            self.assertTrue(manifest["payloadSummary"]["hasKlineData"])

    def test_kline_prompt_forbids_model_ohlc(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp)
            manifest = rp.render_all_prompts(self.payload, out, work_root=out)
            user = (out / "prompts" / "kline.user.md").read_text(encoding="utf-8")
            system = (out / "prompts" / "kline.system.md").read_text(encoding="utf-8")
            outputs = manifest["agentContract"]["requiredOutputs"]
            kline = next(o for o in outputs if o["id"] == "klineBrief")

            self.assertIn("不得返回或改写 open、close、high、low", user)
            self.assertIn("不得由模型自由生成或改写", system)
            self.assertTrue(kline["path"].endswith("kline-brief.json"))
            self.assertIn("不得返回或改写 open/high/low/close", kline["note"])

    def test_manifest_assemble_uses_payload_kline_data_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp)
            manifest = rp.render_all_prompts(self.payload, out, work_root=out)
            command = manifest["assemble"]["command"]

            self.assertIn("--kline-brief-json", command)
            self.assertNotIn("--kline-json", command)

    def test_cli_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            payload_path = tmp_path / "payload.json"
            payload_path.write_text(
                json.dumps(self.payload, ensure_ascii=False), encoding="utf-8"
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "render_prompts.py"),
                    "--payload-json",
                    str(payload_path),
                    "--out-dir",
                    str(tmp_path / "work"),
                    "--work-root",
                    str(tmp_path / "work"),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            out = json.loads(proc.stdout.strip())
            self.assertTrue(pathlib.Path(out["manifest"]).exists())


class ReadmeConsistencyTests(unittest.TestCase):
    def test_readme_documents_render_and_generate_commands(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("render_prompts.py", readme)
        self.assertIn("generate_report.py", readme)
        self.assertIn("prompt-manifest.json", readme)
        self.assertIn("klineData", readme)


if __name__ == "__main__":
    unittest.main()
