"""墨青测评风校验器回归测试。"""
import subprocess
import sys
import unittest
from pathlib import Path

from validate_gzh_html import THEME_ID, theme_checks, validate

WARNING_ID = "[darkmode-no-gradient]"
E1 = "color:#111827;font-weight:700;"


def fragment(style):
    return f'<section style="{style}"><span leaf="">测试文字</span></section>'


def long_paragraph(emph_style=None):
    text = "这是一个超过四十字的墨青主题正文段落，用来验证每个叙述型长段都必须具有已验证行内强调，不能回退为空白正文。"
    if emph_style:
        return (
            '<section><p style="margin:0 0 16px;font-size:14px;line-height:1.9;text-align:justify;">'
            f'<span leaf="">这是一个超过四十字的墨青主题正文段落，用来验证</span><span style="{emph_style}"><span leaf="">每个叙述型长段</span></span><span leaf="">都必须具有已验证行内强调，不能回退为空白正文。</span>'
            '</p></section>'
        )
    return (
        '<section><p style="margin:0 0 16px;font-size:14px;line-height:1.9;text-align:justify;">'
        f'<span leaf="">{text}</span></p></section>'
    )


class GradientBackgroundTests(unittest.TestCase):
    def test_background_styles(self):
        cases = [
            ("issue radial", fragment("background:radial-gradient(circle at 30% 0%,#FAFAFA,#FFFFFF)"), 1),
            ("linear", fragment("background:linear-gradient(180deg,transparent 60%,#E4E4E7 60%)"), 1),
            ("background image", fragment("background-image:linear-gradient(red,blue)"), 1),
            ("solid", fragment("background:#FAFAFA"), 0),
            ("comment", fragment("background:#fff;/* background:linear-gradient(red,blue) */"), 0),
            ("URL filename", fragment("background:url('linear-gradient(red,blue).png')"), 0),
        ]
        for name, source, expected in cases:
            with self.subTest(name=name):
                errors, warnings, leaf_count = validate(source)
                self.assertEqual(errors, [])
                self.assertEqual(leaf_count, 1)
                self.assertEqual(sum(WARNING_ID in w for w in warnings), expected)


class InkTealWhitelistTests(unittest.TestCase):
    def test_theme_is_fixed(self):
        self.assertEqual(THEME_ID, "ink-teal-tech")

    def test_long_paragraph_requires_whitelisted_emphasis(self):
        errors, warnings = theme_checks(long_paragraph())
        self.assertTrue(any("0 处行内强调" in error for error in errors))
        self.assertEqual(warnings, [])

    def test_e1_is_accepted(self):
        errors, warnings = theme_checks(long_paragraph(E1))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_unknown_emphasis_is_rejected(self):
        errors, _ = theme_checks(long_paragraph("color:#059669;font-weight:700;"))
        self.assertTrue(any("不属于 4.3 E1–E7" in error for error in errors))

    def test_master_font_exceptions_do_not_warn(self):
        source = (
            '<section style="font-family:Arial"><span leaf="">容器</span></section>'
            '<span style="font-family:Menlo;font-size:10px;font-weight:700"><span leaf="">STEP</span></span>'
            '<span style="font-family:Georgia;font-size:11px;font-style:italic"><span leaf="">/// END</span></span>'
        )
        _, warnings, _ = validate(source)
        self.assertFalse(any("font-family" in warning for warning in warnings))

    def test_cli_rejects_other_theme(self):
        script = Path(__file__).with_name("validate_gzh_html.py")
        result = subprocess.run(
            [sys.executable, str(script), "--theme", "moyu-green", "--stdin"],
            input=long_paragraph(E1),
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
