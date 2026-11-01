# 第一版构建与发布记录

版本：V1 / 1.0.0；日期：2026-11-01；目标：WEveboy/STL_Houjie-skill。

基础蒸馏后按用户追加要求增加功能，首次公开版本统一包含18张能力卡、11个模型和归档/审计重算。基础稿没有被描述成已经发布的历史版本。

本地验证：26组Python资源测试、6项安装器测试、16组C++17契约实验及3项DeepSeek适配契约通过；项目相对引用、版本与安装清单核对通过。归档解压后重新安装，验证原8例、11操作清单与新增实验重算。Cangjie格式验证和Skill入口验证另记于源审计。

独立代理记录：39题全部完成，36个结果任务通过，39项触发/内部路由判断通过；无Skill同题35/36，另1题正确表示无法知道项目私有增长公式。该实验发生在追加工具前，不据此声称新工具也经代理盲测。

两份最终教程以XeLaTeX各编译两次，检查无Overfull、Missing character或Undefined control sequence；保留非缺字性质的Fandol Script CJK选择提示。最终两份教程各12页，A4；全页缩略及重点/末页目视未见裁切或乱码。

发布流程由GitHub Actions在双系统验证后生成Codex ZIP、DeepSeek ZIP/TGZ、源码ZIP、两份教程PDF及SHA256SUMS，再逐个下载核对。原书、全文OCR、页图、构建缓存、私人路径与凭据不上传。所有远端完成状态以实际结果为准，不能由准备好的脚本推断发布已经完成。

## 已完成远端源码上传

- 首次完整提交：`9023029b9ea9e40fc58a120a0b1e6363fe7e1b4e`。
- 源码tree：`2abd3e4af03d5a6c063e0f3b6dba996d058d19f1`，127个文件逐一Git blob SHA核对一致。
- 两份教程最终各12页，A4；全页缩略和重点/末页目视未发现裁切或乱码。
- [第一版CI](https://github.com/WEveboy/STL_Houjie-skill/actions/runs/41307555478)已成功完成：Windows、Ubuntu与publish三任务全部通过。

## 发行与下载核验完成

- [第一版Release](https://github.com/WEveboy/STL_Houjie-skill/releases/tag/edition-v1.0.0)已发布，目标提交为`9023029b9ea9e40fc58a120a0b1e6363fe7e1b4e`。
- 7个公开资产已全部实际下载，分别重算SHA256并与GitHub digest及SHA256SUMS核对一致。
- Codex ZIP和DeepSeek TGZ的31个发行运行文件逐字节一致；从实际下载的Codex包重新安装并验证11操作清单通过。
- 本地Windows构建与Linux CI的TGZ容器哈希不同；以发行SHA256SUMS为准。运行文件清单及内容一致，未把容器压缩差别误判为能力版本不同。
- 资产URL、字节数及SHA256见[发行核验记录](release-verification.json)。
- 主分支最后补记此日志和完成状态；Release标签保留原始构建快照，不覆盖既有发行资产。
