---
name: wechat-article-archive
description: 从用户提供的公开微信公众号文章链接出发，采集可公开访问的文章正文与图片，按公众号隔离保存为本地 Markdown 归档，生成文章清单，并按需调用 author-methodology-analysis 生成方法论报告与文案框架；进入分析流程后默认自动生成 HTML 看板并同步飞书，最后校验并打包 ZIP。适用于“采集公众号最近 N 篇”“公众号文章带图 Markdown 归档”“按之前一样整理文章”“归档后分析作者方法论”等请求；不用于绕过登录、验证码、反爬或获取私密内容。
---

# 微信公众号文章归档

## 默认行为

- 只采集用户有权访问的内容，不绕过验证码或风控。正文抓取不使用 Cookie；精确获取公众号历史列表时可由用户扫码登录微信公众平台，登录态仅保存在用户本机缓存。
- 用户可自定义采集篇数；未指定时默认目标为最近 50 篇。
- 默认生成文章归档、`<博主>-文章清单.csv` 和 ZIP。
- 仅当用户要求分析作者方法论时，调用 `author-methodology-analysis`。
- 进入方法论分析流程后，默认自动生成 HTML 看板并同步飞书。
- 只有用户明确要求“不生成 HTML”或“不同步飞书”时才关闭对应产物。
- 公开来源不足时交付实际数量，不伪造“最近 N 篇”或“完整历史”。

## 唯一输出契约

先识别公众号名称和 `biz`，再确定：

```text
author_root = <workspace>/output/<safe-author-name>/
```

若同名目录已属于其他 `biz`，使用 `<safe-author-name>-<biz-tail>`。微信内部标识、时间置信度、时间线完整性、采集来源和内部状态只用于采集与校验，不写入最终文章清单。

最终结构：

```text
output/<safe-author-name>/
  <safe-author-name>-文章清单.csv
  articles/
    01-文章标题/
      <文章标题>.md
      images/
  <safe-author-name>-方法论报告.md          # 仅按需分析
  <safe-author-name>-文案框架.md            # 仅按需分析
  <safe-author-name>-分析数据.json           # 分析时生成
  <safe-author-name>-文章特征.csv            # 分析时生成
  <safe-author-name>-方法论看板.html          # 分析时默认生成
  <safe-author-name>-飞书同步.json            # 成功同步飞书后生成
  <safe-author-name>-竞品标题样本.json        # 提供竞品样本时生成
  <safe-author-name>-文章归档.zip
```

ZIP 内必须保留 `<safe-author-name>/` 顶层目录，内部结构与上面一致，但不得把 ZIP 自身打入 ZIP。

每篇文章目录只允许包含一个同名 Markdown 文件和 `images/`。文件和目录名需移除 `/\\:*?"<>|`，目录名前保留两位数字序号。

## 工作流

### 1. 解析入口并锁定身份

从入口文章提取：

- 标题：`#activity-name`、`msg_title` 或 `<title>`
- 公众号名：`#js_name` 或 `nickname`
- `__biz`/`biz`、`mid`/`appmsgid`、`idx`、`sn`
- 发布时间、合集信息及页面显式文章链接

创建或核验 `author_root`。已有目录只有在 `biz` 相同，或 `biz` 缺失但公众号名和多条文章 URL 均一致时才能增量复用。

### 2. 锁定候选列表

候选字段至少包括：

```text
title,url,publish_time,source_type,accessible,biz,mid,idx,sn
```

来源优先级：

1. 用户扫码授权后的微信公众平台文章历史列表
2. 无需登录即可分页的公众号公开历史入口
3. 公开合集/专辑
4. 当前文章页显式内链
5. 最多两轮公开搜索补充
6. 经身份核验的本地既有归档

候选按 `biz + mid + idx + sn` 和规范化 URL 去重。同名但文章键不同的文章必须保留。

用户要求“最近 N 篇”“完整采集”或只提供公众号名称时，优先使用确定性历史列表脚本。`N` 为用户指定数量；未指定时取 `50`：

```bash
python3 scripts/discover_account_articles.py \
  --account "<公众号精确名称>" \
  --limit <N> \
  --output "<workspace>/tmp/<safe-author-name>-candidates.csv"
```

首次运行会生成二维码，用户扫码确认后，登录态默认保存到 `~/.cache/wechat-article-archive/session.json`，文件权限设为仅当前用户可读写。若搜索结果重名，脚本拒绝猜测并列出候选，此时用 `--fakeid <fakeid>` 精确选择。会话失效时脚本删除缓存，重新运行并扫码即可。

历史列表脚本按后台返回顺序分页，提取标题、链接、明确发布时间和稳定账号身份，并输出候选 CSV。只有脚本返回 `timeline_complete: true`，且正文采集无失败、无未知发布时间时，正文采集命令才可传 `--timeline-complete`。

不需要或无法扫码时，使用搜索、公开历史入口或合集获得 URL，将候选写为 CSV，至少包含 `url`，可选包含 `source_type`、`publish_time`、`time_confidence`。当前文章页显式内链可由采集脚本自动发现。公开搜索和需浏览器观察的历史入口仍由可用搜索/浏览器工具完成，不在脚本中绕过访问限制。

发布时间可信来源按优先级为：

1. 页面 DOM 中明确的发布时间
2. 页面脚本中的 `ct`、`publish_time`、`create_time` 等 Unix 时间戳
3. 合集或历史接口明确返回的发布时间字段
4. 候选来源中可追溯的发布时间

`scene` 等访问场景参数不得作为发布时间。无法确认时写 `未知`。只有来源覆盖时间线且发布时间可靠时才能称为“最近 N 篇”；否则表述为“可公开采集的 N 篇”。

### 3. 抓取正文与图片

新归档优先运行确定性采集脚本：

```bash
python3 -c "import requests, lxml"
python3 scripts/collect_articles.py \
  --author-root "<author_root>" \
  --candidate-csv "<candidate_csv>" \
  --limit <N> \
  --workers 1 \
  --image-workers 2 \
  --article-delay 2 \
  --resume
```

已有完整候选 CSV 时不要使用 `--discover-links`，避免把推荐文章或其他公众号链接混入完整时间线。只有从少量入口文章探索公开内链时才开启该参数。

也可直接在命令末尾传入一个或多个公开微信文章 URL。目标目录已存在时：

- 默认拒绝操作。
- `--resume` 复用已有成功文章，只重试缺失或失败文章。
- `--replace` 不复用现有归档，重新构建。
- `--no-cache` 强制跳过外部正文和图片缓存，适合确认文章内容已经更新时使用。

所有模式都采用临时目录完整构建、校验和旁路备份，失败时保留原归档。正文与图片缓存默认位于 `~/.cache/wechat-article-archive/content/`，不进入 ZIP。

只有候选来源已被确认覆盖完整时间线时才传 `--timeline-complete`。若存在未知发布时间或抓取失败，脚本会自动降级为 `false`。

脚本执行以下操作：

- 只接受 `mp.weixin.qq.com` 公开文章 URL。
- 正文容器优先 `#js_content`，其次 `.rich_media_content`。
- 保留标题、小标题、段落、列表、引用和正文链接。
- 图片按正文顺序下载到 `images/image-01.<ext>`，仅允许已知微信图片域名，并限制单图 20 MB。
- 图片下载使用文章 URL 作为 Referer；相同 URL 只下载一次，默认 2 张并发，失败时删除远程引用并记录 `image_failures`。
- 文章默认串行采集，并在请求启动之间等待 2 秒；可用 `--workers`、`--image-workers` 和 `--article-delay` 调整。为降低环境验证风险，不建议批量任务将文章并发调高。
- 正文、图片和后台列表请求默认失败重试 2 次并指数退避，可用 `--retries` 调整。
- Markdown 转换保留标题、段落、列表、引用、链接、代码块和表格；视频、音频及嵌入内容保留为来源链接或明确占位。
- 自动生成文章目录、Markdown 和 `<博主>-文章清单.csv`。
- `--limit` 接受任意正整数；省略时默认 `50`。

Markdown 顶部必须包含：

```markdown
# 文章标题

- 公众号：<名称>
- 公众号标识：<biz 或未知>
- 原文链接：<url>
- 发布时间：<YYYY-MM-DD HH:mm:ss 或未知>
- 采集来源：<source_type>

---
```

### 4. 生成文章清单

`<博主>-文章清单.csv` 必须使用 UTF-8 BOM，至少包含：

```text
index,title,url,publish_time,error,author_name,article_dir,markdown_file
```

- `identity_key`、`biz`、`mid`、`idx`、`sn`、`time_confidence`、`timeline_complete`、`source_type`、`status` 仅作为候选发现和内部校验字段，不得出现在最终交付清单。
- `article_dir` 和 `markdown_file` 均有值表示归档成功；均为空且 `error` 有值表示采集失败。
- `markdown_file` 显式记录清洗、截断后的文件名，避免校验器重新猜测文件名。
- 失败行必须填写 `error`，且不得引用文章目录。
- ZIP 只包含具有有效文章目录和 Markdown 文件的文章。

### 5. 分析编排

用户要求方法论分析时，调用 `author-methodology-analysis`，传入：

- `input_dir = <author_root>/articles`
- `output_dir = <author_root>`
- `author_name`
- `article_list = <author_root>/<safe-author-name>-文章清单.csv`
- `generate_html = true`，除非用户明确关闭
- `sync_lark = true`，除非用户明确关闭

归档 skill 不重复生成分析报告，也不直接依赖不存在的第三方文案 skill。

### 6. 校验与打包

先运行：

```bash
python3 scripts/validate_archive.py "<author_root>"
```

校验器必须通过以下检查：

- CSV 索引连续、URL 和文章键不重复、身份一致。
- `article_dir` 不能是绝对路径、包含 `..` 或逃逸 `articles/`。
- 归档内禁止符号链接。
- Markdown 元数据必须与 CSV 一致。
- Markdown、HTML 和引用式图片不得指向远程或越界路径。
- Markdown 正文不得为空或包含验证页、频控页、删除页等异常页面标记；过短正文和转换保留率异常计入质量统计。
- 根目录不得包含未声明文件。

校验通过后使用配套脚本重新创建 ZIP，禁止调用可能破坏中文文件名的系统 `zip`，也禁止增量覆盖旧 ZIP：

```bash
python3 scripts/package_archive.py "<author_root>"
```

打包后再运行：

```bash
python3 scripts/validate_archive.py "<author_root>" --zip "<zip_path>"
```

打包器只加入 CSV 中 `archived` 文章和六个声明的分析产物，不会递归打包未知文件。ZIP 二次校验必须检查文件白名单、额外条目、缺失条目和 CRC。

若进入分析流程，额外校验方法论报告、文案框架、分析数据、文章特征和 HTML 均存在。除非用户明确关闭飞书，否则校验飞书文档可读取且包含主报告关键章节；飞书成功后还应存在 `<博主>-飞书同步.json`。飞书失败不得阻塞本地归档和 ZIP，但必须在最终结果中说明。

## 失败边界

- `profile_ext` 返回 `no session`、登录页或验证页：记录一次后立即降级。
- 微信公众平台历史列表会话失效：删除本地会话缓存并提示重新扫码，不循环重试。
- 搜狗或其他跳转触发验证码：立即停止该路径。
- 入口文章本身不可公开访问：说明限制并请求可访问链接。
- 不可访问的搜索结果不得进入最终包。
- 转载内容不得标记为公众号原文。

## 最终回复

简要报告：

- 实际归档数与失败数
- 来源范围，以及是否能严格称为“最近 N 篇”
- 发布时间未知数、图片失败数、过短正文/转换质量警告数和校验结果
- 方法论、HTML、飞书是否完成；若被用户关闭或执行失败，说明原因
- 使用普通可点击的本地绝对路径链接返回 ZIP，不使用 `local-file://`

## 资源

- `scripts/validate_archive.py`：校验目录、CSV、Markdown、图片引用和 ZIP。
- `scripts/package_archive.py`：以 UTF-8 文件名重新创建 ZIP，并排除 ZIP 自身。
- `scripts/collect_articles.py`：从公开微信 URL/候选 CSV 抓取正文、转换 Markdown、本地化图片并生成清单。
- `scripts/discover_account_articles.py`：扫码登录微信公众平台，精确搜索公众号并分页生成最近 N 篇候选列表，默认 50 篇。
- `scripts/archive_common.py`：共享 CSV Schema、安全路径、命名和打包白名单规则。
