"""运行方式：py -B -m unittest discover -s code -p "test_*.py" -v"""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from word_count import count_words


class CountWordsTests(unittest.TestCase):
    def test_case_and_punctuation(self):
        self.assertEqual(count_words("Hello, hello! WORLD. world? Hello"),
                         {"hello": 3, "world": 2})

    def test_whitespace(self):
        self.assertEqual(count_words("apple\tbanana\napple"),
                         {"apple": 2, "banana": 1})

    def test_empty_and_non_words(self):
        for text in ("", " \n\t", "123 456 !? _"):
            with self.subTest(text=text):
                self.assertEqual(count_words(text), {})

    def test_chinese_units(self):
        self.assertEqual(count_words("数据 安全，数据！数据安全"),
                         {"数据": 2, "安全": 1, "数据安全": 1})


class CommandLineTests(unittest.TestCase):
    def run_program(self, path):
        script = Path(__file__).with_name("word_count.py")
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(script), str(path)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def test_file_output_and_sorting(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "含空格 sample.txt"
            path.write_text("Banana apple APPLE banana cherry apple", encoding="utf-8-sig")
            result = self.run_program(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "总词数：6", "不同词数：3", "词语\t次数",
            "apple\t3", "banana\t2", "cherry\t1",
        ])

    def test_tied_counts(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.txt"
            path.write_text("zebra apple", encoding="utf-8")
            result = self.run_program(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[-2:], ["apple\t1", "zebra\t1"])

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.txt"
            path.write_text("", encoding="utf-8")
            result = self.run_program(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(),
                         ["总词数：0", "不同词数：0", "未找到可统计的词语。"])

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_program(Path(folder) / "missing.txt")
        self.assertEqual(result.returncode, 1)
        self.assertIn("无法读取文件", result.stderr)

    def test_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "invalid.txt"
            path.write_bytes(b"\xff\xfe\xff")
            result = self.run_program(path)
        self.assertEqual(result.returncode, 1)
        self.assertIn("不是有效的 UTF-8", result.stderr)


if __name__ == "__main__":
    unittest.main()
