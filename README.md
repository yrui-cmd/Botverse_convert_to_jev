# Botverse Convert to Jev

不用从头重写 Skill，也能把其中重复、封闭的文本判断交给 Jev。

Botverse Convert to Jev 接收一个现有 Skill，先复制出独立增强版，再识别答案固定、证据明确、失败后可以回退的判断节点。原 Skill 保持不变，绘图、代码、浏览器、文件操作和开放推理继续使用原来的执行器。

转换的目标很具体：减少不必要的重复模型判断，缩短运行时间，并降低对应调用成本。实际收益以转换后的测试数据为准；没有实测时不会编造提速或节省比例。

## 什么时候适合转换

- 同一种文本分类、字段判断或固定选项选择反复出现；
- 输入证据充分，输出集合明确；
- Jev 不确定时可以安全回到当前 GPT；
- 希望保留原 Skill，只新增一个可独立安装的增强版。

开放创作、视觉判断、复杂规划和工具执行不交给 Jev，继续由原模型和工具完成。

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
