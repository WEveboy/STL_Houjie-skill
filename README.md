# STL Houjie Skills · 第一版

从侯捷《STL源码剖析》提炼的 STL 源码分析与泛型编程 Skill。一个可发现入口，内部按任务加载能力卡；保留章节精读、短引文定位、三重验证、实际任务测试与版本边界。

它帮助你追踪对象生存期、迭代器与 traits、容器不变量、算法前提、仿函数及配接器，并使用原创教学模型和当前标准库编译实验核验结论。**原书研究的是历史 SGI STL；模型输出与现代标准保证分别说明。**

当前包含18张能力卡、11个有界教学模型，以及实验归档和审计重算。新增功能、验证范围与兼容说明见[更新日志](CHANGELOG.md)。

## 安装与首次使用

从[第一版 Release](https://github.com/WEveboy/STL_Houjie-skill/releases/tag/edition-v1.0.0)选择 Codex ZIP 或 DeepSeek Harness ZIP/TGZ，先核对 SHA256SUMS。也可下载源码后使用下列命令。

Codex（Python 3.10+）：

```powershell
python scripts/install_codex.py
```

默认装入用户的 `.agents/skills/stl-houjie`；自定义位置使用 `--destination`。首次安装拒绝覆盖；有意升级使用 `--replace`，会先保留旧目录。重新加载会话后可提问：

```text
$stl-houjie 解释vector插入时哪些对象被构造、赋值、销毁，
分别讨论容量足够和触发重配置，并给一个可编译的验证例。
```

DeepSeek 版面向具备本地工具执行能力的 **DeepSeek Harness**，按[独立教程](docs/tutorial/DeepSeek-First-Edition.pdf)安装插件；普通网页聊天不等同于本地 Harness。适配器契约测试和真实宿主会话测试在[评测报告](docs/EVALUATION.md)中分别说明。

## 阅读与复现

- [Codex教程 PDF](docs/tutorial/Codex-First-Edition.pdf) · [TeX源](docs/tutorial/Codex-First-Edition.tex)
- [DeepSeek教程 PDF](docs/tutorial/DeepSeek-First-Edition.pdf) · [TeX源](docs/tutorial/DeepSeek-First-Edition.tex)
- [章节精读](source/CHAPTER_READING.md) · [精华长文](source/DIGEST.md) · [蒸馏方案](source/DISTILLATION_PLAN.md)
- [来源、原文疑点与现代边界](docs/SOURCE_BOUNDARIES.md) · [三重验证](source/verified.md) · [覆盖审计](source/coverage-audit.md)
- [Skill入口](skills/stl-houjie/SKILL.md) · [资源用法](skills/stl-houjie/resources/usage.md)
- [测试与未覆盖范围](docs/EVALUATION.md) · [维护上传流程](docs/UPLOAD_WORKFLOW.md)

确定性工具运行不依赖第三方 Python 包。作者端从 Bundle 重编译另需仓颉 2.5.0 与 PyYAML；源码包不内嵌上游依赖。C++实验需要支持 C++17 的编译器，TeX教程使用 XeLaTeX。

```powershell
python skills/stl-houjie/resources/stl_lab.py demo
python skills/stl-houjie/resources/stl_lab.py operations
python skills/stl-houjie/resources/stl_lab.py experiment examples/copy-right.json --out experiments/run-001
python skills/stl-houjie/resources/stl_lab.py audit experiments/run-001 --recompute
python -m unittest discover -s skills/stl-houjie/resources -p "test_*.py"
python -m unittest discover -s tests -p "test_*.py"
python scripts/make_release.py --prepare-only
node --test tests/test_deepseek.mjs
python scripts/verify_project.py
```

## 交付边界

本仓库不分发原书PDF、扫描页或整章OCR，不是完整STL替代库。未逐行核验全书全部源码；不把SGI内部参数写成所有标准库的要求，不承诺任意类型的字节复制合法、所有操作都有强异常保证或多线程安全。现代语义补充有独立来源，原书局部疑误保留审计。

哈希用于核对文件，不能证明数学/程序正确性。测试范围、独立代理评测和宿主限制以实际报告为准。

## 贡献与维护

WEveboy：项目发起、目标与发布范围。Codex（OpenAI AI 编程助手）：协助原文分析、技能化、原创实验、测试与文档整理。原书内容权利归其权利人；本项目未额外授予上游内容权利。
