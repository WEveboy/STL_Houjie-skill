# 教程编译与检查

两份独立TeX使用XeLaTeX、CTeX、Fandol字体和A4版面。命令从本目录执行，每份两次以更新目录/链接：

```text
xelatex -interaction=nonstopmode -halt-on-error Codex-First-Edition.tex
xelatex -interaction=nonstopmode -halt-on-error Codex-First-Edition.tex
xelatex -interaction=nonstopmode -halt-on-error DeepSeek-First-Edition.tex
xelatex -interaction=nonstopmode -halt-on-error DeepSeek-First-Edition.tex
```

只提交最终TeX与PDF；aux/log/toc/out为构建中间文件。教程区分Codex ZIP根部的install_codex.py与源码中的scripts/install_codex.py，后续C++实验需源码项目结构。

2026-11-01先编译基础教程，再因增量功能补写11模型、归档/重算与边界。最终页数、日志及目视检查记录在docs/PUBLICATION.md。Fandol的Script CJK字体声明警告与缺字不同；以渲染实图和Missing character检查共同判断。
