# wechat-article-archive

微信公众号文章归档 Codex skill：从用户提供的公开微信公众号文章链接或公众号名称出发，采集可公开访问的正文与图片，按公众号隔离保存为本地 Markdown 归档，生成文章清单，并打包为可校验的 ZIP。

## 关联文章

- [公众号关联文章](https://mp.weixin.qq.com/s/fG7mdtQeO03lxcS406apow)

## 适用场景

- 采集某个公众号最近 N 篇公开文章，未指定时默认 50 篇。
- 将公开微信文章保存为带本地图片的 Markdown 归档。
- 基于入口文章、公开合集或扫码授权后的微信公众平台历史列表，生成候选文章清单。
- 在归档完成后按需交给 `author-methodology-analysis` 生成作者方法论报告、文案框架、HTML 看板并同步飞书。

这个 skill 不用于绕过登录、验证码、风控或获取私密内容。公开来源不足时，只交付实际可访问数量，不伪造“最近 N 篇”或“完整历史”。

## 产物结构

归档默认写入：

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

ZIP 内会保留 `<safe-author-name>/` 顶层目录，并只打包文章清单、成功归档的文章、图片和声明过的分析产物。

## 安装

将本目录放入 Codex skills 目录，例如：

```bash
mkdir -p ~/.codex/skills
cp -R wechat-article-archive-skill ~/.codex/skills/wechat-article-archive
```

随后在 Codex 中使用：

```text
Use $wechat-article-archive to archive the requested number of recent WeChat articles.
```

## 依赖

- Python 3.9+
- `requests`
- `lxml`

可用以下命令检查依赖：

```bash
python3 -c "import requests, lxml"
```

## 常用工作流

### 1. 通过公众号历史列表生成候选 CSV

适合“最近 N 篇”这类需要稳定时间线的任务。首次运行会生成二维码，用户扫码确认后，会话默认保存到 `~/.cache/wechat-article-archive/session.json`。

```bash
python3 scripts/discover_account_articles.py \
  --account "<公众号精确名称>" \
  --limit 50 \
  --output "tmp/<safe-author-name>-candidates.csv"
```

如果搜索结果重名，脚本会拒绝猜测并提示使用 `--fakeid` 精确选择。

### 2. 采集正文与图片

使用候选 CSV：

```bash
python3 scripts/collect_articles.py \
  --author-root "output/<safe-author-name>" \
  --candidate-csv "tmp/<safe-author-name>-candidates.csv" \
  --limit 50 \
  --workers 1 \
  --image-workers 2 \
  --article-delay 2 \
  --resume
```

也可以直接传入公开微信文章 URL：

```bash
python3 scripts/collect_articles.py \
  --author-root "output/<safe-author-name>" \
  --limit 1 \
  --resume \
  "https://mp.weixin.qq.com/s/example"
```

已有完整候选 CSV 时不要开启 `--discover-links`，避免把推荐文章或其他公众号链接混入完整时间线。只有从少量入口文章探索页面内公开链接时才使用该选项。

### 3. 校验与打包

```bash
python3 scripts/validate_archive.py "output/<safe-author-name>"
python3 scripts/package_archive.py "output/<safe-author-name>"
python3 scripts/validate_archive.py \
  "output/<safe-author-name>" \
  --zip "output/<safe-author-name>/<safe-author-name>-文章归档.zip"
```

校验器会检查 CSV 字段、文章目录、Markdown 元数据、图片引用、远程资源引用、异常页面标记、符号链接和 ZIP 文件白名单。

## 脚本说明

- `scripts/discover_account_articles.py`：通过微信公众平台扫码登录，精确搜索公众号并分页导出最近文章候选 CSV。
- `scripts/collect_articles.py`：抓取公开文章正文，转换 Markdown，本地化图片，并生成文章清单。
- `scripts/validate_archive.py`：校验归档目录和 ZIP 结构。
- `scripts/package_archive.py`：以 UTF-8 文件名生成白名单 ZIP。
- `scripts/archive_common.py`：共享 CSV schema、安全路径、命名和打包规则。

## 安全边界

- 只接受 `mp.weixin.qq.com` 公开文章 URL。
- 正文抓取不使用 Cookie。
- 历史列表需要用户扫码授权，登录态只保存在用户本机缓存。
- 图片仅从已知微信图片域名下载，单图限制 20 MB。
- 遇到验证码、访问频繁、环境异常、删除页或违规不可见页面时，不绕过，直接记录失败或降级。
- 输出清单不泄露微信内部状态字段，只保留交付所需列。
