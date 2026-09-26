---
name: botverse-convert-to-jev
description: 给现有 Codex Skill 增量加入 Jev 判断节点，无需从头重写原 Skill；把封闭文本判断交给 Jev，保留原有开放推理、视觉、代码和工具流程，用于缩短运行时间并降低模型调用费用。
---

# Botverse Convert to Jev

为用户指定的现有 Skill 自动生成一个 Jev 增强副本。转换方式是复制原 Skill 后做最小增量修改：增加节点合同、薄适配器和必要的阶段调用，不重新设计或重写已经有效的原流程。

## 结果

默认输出 `<原名称>-jev`，原 Skill 不变。增强副本保留原文件、能力、工具和阶段，只对适合 Jev 的封闭判断节点增加：

- `references/jev-nodes.json`：节点输入、固定选项、置信门槛与回退；
- Jev 薄适配器；
- 阶段入口中的最小调用；
- `workflow_map.json`、`jev_gate_map.json` 和 `conversion_report.md`；
- 来源快照、测试和可选基准报告。

## 执行分工

- **固定代码**：路径、字段、哈希、计数、格式、状态和退出码。
- **Jev**：证据充分、答案固定、允许不确定回退的文本判断。
- **当前 LLM**：开放规划、生成、解释、复杂修复、视觉与科学判断。
- **原工具**：浏览器、图像、文件、渲染、API 和其他执行器。

不要把全部任务改成分类。已有代码能准确判断的节点继续使用代码；Jev 不适合的节点继续走原流程。

## 增量转换流程

### 1. 复制并冻结来源

运行：

```powershell
python scripts/bootstrap_conversion.py "<源 Skill 路径>" --output-parent "<输出目录>"
```

脚本创建完整副本和 SHA-256 来源快照。目标已存在时停止，不覆盖现有文件。

### 2. 映射原流程

读取源 Skill 的入口、脚本、阶段合同和直接引用，生成 `workflow_map.json`。记录每个节点的输入、输出、执行器、失败方式、副作用和成功条件。此阶段不修改源文件。

### 3. 找出适合 Jev 的节点

候选节点必须满足：

- 主要输入是充分的文本；
- 输出是固定的 `choice`、`score` 或 `boolean/noul`；
- 有明确的不确定选项或低置信回退；
- 不需要看图、生成内容、执行工具或查询事实；
- 接入后能替代一次真实的重复模型判断。

把选中的节点写入 `references/jev-nodes.json` 和 `jev_gate_map.json`。无需凑数量。

### 4. 做最小修改

只修改增强副本：

1. 添加薄适配器；
2. 在对应阶段入口加载当前节点所需的最小文本；
3. `completed / jev` 时使用合同内结果；
4. `fallback / current_gpt` 时由当前 GPT 完成原来的同一判断；
5. 保留原授权、工具、执行顺序、质量门禁和交付条件。

不要重写无关提示词、脚本或已经通过的阶段。Jev 输出只代表当前节点，不能直接把整个阶段标记为完成。

### 5. 验证

运行：

```powershell
python scripts/static_validate.py "<增强 Skill 路径>"
python scripts/verify_source_unchanged.py "<增强 Skill/conversion_manifest.json>" "<源 Skill 路径>"
```

还要验证：

- 原 Skill 的现有测试；
- Jev 确定结果、不确定结果和服务失败回退；
- 一个正常输入、一个边界输入和一个恢复输入；
- 来源哈希没有变化；
- 增强版仍能独立运行。

有真实基准输入时，比较旧版与新版的完成结果、LLM 调用、Jev 调用、耗时和 token。只报告实际测得的节省，不推算未测数据。

## 修复和完成

失败时只修补受影响节点，默认最多 3 轮。只有静态检查、来源复核、冒烟测试和所需门禁通过，才把 `conversion_manifest.json` 标记为 `VERIFIED_READY`。

详细提示词位于 `prompts/`；节点模板位于 `templates/jev_gate_spec.json`；结构定义位于 `schemas/conversion_manifest.schema.json`。
