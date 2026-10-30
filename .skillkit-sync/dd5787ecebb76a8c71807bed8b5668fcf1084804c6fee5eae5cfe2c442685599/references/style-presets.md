# 风格预设 style-presets

4 套风格的 CSS token 块。直接覆盖 `base.css` 已有的 `--pad` / `--font-display` / `--font-body`，
并新增统一命名的风格 token。**4 套用同一套变量名，仅取值不同**，方便 HTML 模板复用。

> 引入顺序：`base.css` → 本文件 token → 各风格化的类。
> 选择器统一为 `[data-style="<id>"]`，挂在 `.poster` 或更外层。

## 统一 token 变量清单（4 套都提供）

| 变量 | 含义 |
|------|------|
| `--bg` | 画布背景色 |
| `--ink` | 主文字色 |
| `--ink-soft` | 次级文字色（注脚 / 辅助说明） |
| `--accent` | 强调色（关键词、序号、线条焦点） |
| `--accent-soft` | 强调色的柔和版（色卡底、淡背景块） |
| `--font-display` | 展示字体（标题），带中文兜底 |
| `--font-body` | 正文字体，带中文兜底 |
| `--pad` | 安全区内边距（覆盖 base 默认 72px） |
| `--fs-cover-title` | 封面主标题字号 |
| `--fs-h1` | 内页大标题字号 |
| `--fs-body` | 正文字号（≥28） |
| `--fs-caption` | 注脚 / 辅助字号（≥22） |
| `--radius` | 圆角基准 |
| `--hairline` | 描边 / 分隔线粗细 |
| `--line-color` | 分隔线 / 描边颜色 |

---

## 爆款原生 (baokuan)

```css
/* 奶油底承托高饱和但降一档的暖橙强调，砖橙不刺眼；近黑墨字保证大字报重量。 */
[data-style="baokuan"] {
  --bg: #FBF6EC;            /* 奶油米白，干净打底 */
  --ink: #211C18;           /* 近黑暖墨，大字报主色 */
  --ink-soft: #6B6258;      /* 暖灰，辅助说明 */
  --accent: #F06A2E;        /* 砖暖橙，关键词色块/序号（降饱和不刺眼） */
  --accent-soft: #FCE3C4;   /* 浅橙奶油，关键词淡底 */

  --font-display: "Smiley Sans", "PingFang SC", "Microsoft YaHei", sans-serif; /* 得意黑：海报级大字报展示字体 */
  --font-body: "PingFang SC", "Microsoft YaHei", sans-serif;
  --pad: 64px;              /* 信息密度高，留白略紧 */

  --fs-cover-title: 116px;  /* 大字报封面主标题 */
  --fs-h1: 64px;
  --fs-body: 32px;          /* ≥28 */
  --fs-caption: 24px;       /* ≥22 */
  --radius: 16px;
  --hairline: 4px;          /* 关键词描边偏粗，呼应大字报 */
  --line-color: #211C18;
}
```

## 高级杂志 (magazine)

```css
/* 纸白 + 近黑宋体，几乎无色块；克莱因蓝仅作一处极克制的点缀，靠发丝线与留白立调性。 */
[data-style="magazine"] {
  --bg: #F7F5F0;            /* 纸白偏暖灰，杂志内页质感 */
  --ink: #1A1A1A;           /* 近黑（非纯黑），衬线主色 */
  --ink-soft: #8A8378;      /* 暖灰，栏目元数据/页码 */
  --accent: #2E4A9E;        /* 克莱因蓝点缀，仅用于一条线或一个符号 */
  --accent-soft: #E6E2D8;   /* 浅暖灰，极淡分区底 */

  --font-display: "Songti SC", "SimSun", serif;  /* 衬线撑文化感 */
  --font-body: "Songti SC", "SimSun", serif;
  --pad: 96px;              /* 大留白，呼吸感 */

  --fs-cover-title: 88px;   /* 标题靠字号反差而非加粗 */
  --fs-h1: 56px;
  --fs-body: 30px;          /* ≥28，行高宜宽松 */
  --fs-caption: 23px;       /* ≥22 */
  --radius: 2px;            /* 几乎直角，硬朗编辑感 */
  --hairline: 1px;          /* 发丝线 */
  --line-color: #1A1A1A;
}
```

## 柔和氛围 (ambient)

```css
/* 燕麦奶油底 + 暖棕灰文字，刻意压低对比；藕粉作柔和色卡，边缘全用大圆角，温柔不喧哗。 */
[data-style="ambient"] {
  --bg: #F3EBDF;            /* 燕麦奶油，暖调打底 */
  --ink: #5B5048;           /* 暖棕灰，柔和不锐利（不用纯黑） */
  --ink-soft: #9A8E80;      /* 雾感浅棕灰，辅助文字 */
  --accent: #C98C7A;        /* 浅陶土/藕粉，莫兰迪强调 */
  --accent-soft: #E8D5CC;   /* 淡藕粉，柔和色卡底 */

  --font-display: "PingFang SC", "Microsoft YaHei", sans-serif; /* 用细/轻字重营造柔软 */
  --font-body: "PingFang SC", "Microsoft YaHei", sans-serif;
  --pad: 100px;            /* 大面积留白，呼吸感最强 */

  --fs-cover-title: 76px;  /* 标题轻盈，不压迫 */
  --fs-h1: 48px;
  --fs-body: 30px;         /* ≥28 */
  --fs-caption: 23px;      /* ≥22 */
  --radius: 32px;          /* 大圆角，边缘"软" */
  --hairline: 1px;
  --line-color: #D8CABA;   /* 极淡暖线 */
}
```

## 极简冲击 (minimal)

```css
/* 有态度的深墨蓝单色背景 + 奶白超大字，全画面只一种色块，对比拉满，一句话砸脸。 */
[data-style="minimal"] {
  --bg: #14181F;            /* 深墨蓝，单色背景（有态度，非纯黑） */
  --ink: #F4F1E9;           /* 奶白，与深底强对比 */
  --ink-soft: #8A9099;      /* 冷灰，仅用于极小注脚 */
  --accent: #F4F1E9;        /* 与主文字同色——极简不引入第二色块 */
  --accent-soft: #232A35;   /* 比背景略亮一档，必要时的角标底 */

  --font-display: "Smiley Sans", "PingFang SC", "Microsoft YaHei", sans-serif; /* 得意黑斜体：态度向冲击力 */
  --font-body: "PingFang SC", "Microsoft YaHei", sans-serif;
  --pad: 80px;

  --fs-cover-title: 140px;  /* 超大字，顶满画面 */
  --fs-h1: 96px;
  --fs-body: 30px;          /* ≥28，正文极少，仅垫脚 */
  --fs-caption: 24px;       /* ≥22 */
  --radius: 0px;            /* 无圆角，干脆 */
  --hairline: 3px;          /* 偶尔一条短下划线 */
  --line-color: #F4F1E9;
}
```
