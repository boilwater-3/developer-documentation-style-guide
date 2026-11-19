#!/usr/bin/env python3
"""lint_doc.py 的单元测试。"""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_doc  # noqa: E402


class LintDocTests(unittest.TestCase):
    def _rules(self, markdown: str, ignored: set[str] | None = None) -> list[tuple[int, str]]:
        issues = lint_doc.lint_lines(markdown.splitlines(), "test.md", ignored_rules=ignored)
        return [(i.line, i.rule) for i in issues]

    def test_clean_document_passes(self) -> None:
        doc = """---
title: 示例文档
---

# 部署指南

本指南介绍如何在 macOS 上部署 Node.js 应用，并配置 64 GB 内存与 85% 告警阈值。

## 配置环境变量

运行 `kubectl get pods` 命令查看状态，详情请参阅[集群管理指南](https://example.com/cluster:8080?a=1,b=2)。

流程顺序：需求评审（RFC） → 开发实现 → 灰度发布；写法支持“方式一” / “方式二”。
支持多个中文行内代码并列：`3 个节点`、`5 秒`、`8 像素`。

> [!NOTE]
> 这是一条补充说明。

```bash
# 代码块中的 64GB、！、e.g. 和未空格中文不应误报
echo "测试64GB！"
```
"""
        self.assertEqual(self._rules(doc), [])

    def test_heading_rules(self) -> None:
        doc = """# 主标题

## 二级标题。

#### 跳级标题

# 第二个一级标题
"""
        rules = self._rules(doc)
        self.assertIn((3, "H001"), rules)
        self.assertIn((5, "H002"), rules)
        self.assertIn((7, "H003"), rules)

    def test_pangu_and_units(self) -> None:
        doc = """# 排版测试

使用Git配置64GB内存，延迟低于100ms，CPU 不超过 80 %。
运行`kubectl`查看日志。
支持 JSON 、 YAML 格式。
"""
        rules = self._rules(doc)
        self.assertIn((3, "P001"), rules)
        self.assertIn((3, "P004"), rules)
        self.assertIn((3, "P005"), rules)
        self.assertIn((4, "P002"), rules)
        self.assertIn((5, "P003"), rules)

    def test_punctuation_and_style(self) -> None:
        doc = """# 样式测试

传入“`true`”参数！
这里使用了*中文斜体*。
中文里混用了,半角逗号。
"""
        rules = self._rules(doc)
        self.assertIn((3, "P008"), rules)
        self.assertIn((3, "P006"), rules)
        self.assertIn((4, "P007"), rules)
        self.assertIn((5, "P009"), rules)

    def test_wording_typos_and_anchors(self) -> None:
        doc = """# 措辞测试

详情请[点击这里](https://example.com)。
配置报警阀值，然后登陆控制台。
支持多种格式（e.g. JSON 和/或 YAML）。
让我们简单地完成部署，目前尚不支持 Windows。
"""
        rules = self._rules(doc)
        self.assertIn((3, "L001"), rules)
        self.assertIn((4, "W001"), rules)
        self.assertIn((5, "W002"), rules)
        self.assertIn((5, "W003"), rules)
        self.assertIn((6, "W004"), rules)
        self.assertIn((6, "W005"), rules)

    def test_placeholder_prefix_in_code_and_prose(self) -> None:
        doc = """# 占位符测试

替换 `YOUR_API_KEY` 后运行命令：

```bash
export TOKEN=MY_SECRET_TOKEN
```
"""
        rules = self._rules(doc)
        self.assertIn((3, "W006"), rules)
        self.assertIn((6, "W006"), rules)

    def test_ignore_rules(self) -> None:
        doc = "使用Git配置 64 GB 内存！"
        rules = self._rules(doc, ignored={"P001", "P006"})
        self.assertEqual(rules, [])


if __name__ == "__main__":
    unittest.main()
