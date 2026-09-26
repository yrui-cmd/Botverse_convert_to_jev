# Botverse Convert to Jev

很多 Skill 已经很好用，真正浪费时间和费用的，是运行中反复出现的同类判断。

Botverse Convert to Jev 可以给现有 Skill 增加 Jev 判断部分。你不需要从头写 Skill，也不需要手工拆流程。提供原 Skill 路径，它会自动复制一份增强版，找出适合 Jev 的封闭文本判断，并用最小修改接入。

原来的绘图、代码、浏览器、文件操作和开放推理继续照常运行。Jev 只接管答案固定、证据明确的判断节点。这样可以减少重复的大模型调用，让原有 Skill 跑得更快，花费更低。

## 你会得到

- 原 Skill 保持不变；
- 一个可独立安装的 Jev 增强版；
- 自动生成的 Jev 节点合同和薄适配器；
- Jev 不确定时自动回到当前 GPT；
- 清楚的转换报告、来源快照和验证结果；
- 有真实测试时提供运行时间、调用次数和 token 对照。

## 三步使用

1. 安装本 Skill。
2. 告诉 Codex 原 Skill 的路径。
3. 获取 `原名称-jev` 增强版。

也可以先建立转换工作区：

```powershell
python scripts/bootstrap_conversion.py "C:\path\to\your-skill" --output-parent "C:\path\to\skills"
```

然后告诉 Codex：

> 使用 botverse-convert-to-jev，把这个 Skill 增加 Jev 判断部分。

## 自动分工

| 工作 | 执行者 |
|---|---|
| 路径、哈希、字段、格式、状态 | 固定代码 |
| 固定选项的文本判断 | Jev |
| 开放规划、生成、解释和修复 | 当前 LLM |
| 图像、浏览器、文件、渲染和 API | 原工具 |

正常运行时不需要用户再选择模型。转换器会把合适的判断交给 Jev，其余步骤继续使用原执行器。

## 安装

```powershell
git clone https://github.com/yrui-cmd/Botverse_convert_to_jev.git
```

把仓库目录放入 Codex Skills 目录，重新打开任务即可使用。

## 开源协议

MIT
