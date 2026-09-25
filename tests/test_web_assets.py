from pathlib import Path
import unittest


class WebAssetTests(unittest.TestCase):
    def test_browser_entrypoint_contains_theme_and_controls(self):
        page = Path(__file__).parents[1] / "web" / "index.html"
        self.assertTrue(page.is_file())
        content = page.read_text(encoding="utf-8")
        for marker in ("峰岩 · 中秋快乐", "canvas", "requestAnimationFrame", "pointerdown"):
            self.assertIn(marker, content)
        self.assertNotIn("SPACE 暂停", content)


if __name__ == "__main__":
    unittest.main()
