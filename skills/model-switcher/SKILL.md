---
name: model-switcher
description: Quick model switching for Claude Code sessions. Trigger when the user wants to switch AI models, change to a different model, or use a specific model like "switch to kimi", "use GLM-4", "change to qwen", "切换到智谱", etc. Handles both Chinese and English model names and supports all configured models in settings.json.
---

# Model Switcher

Switch between different AI models quickly during your Claude Code session. This skill updates your settings.json file to change the active model.

## Supported Models

All available models are routed through LiteLLM proxy at `http://127.0.0.1:4000`.

**Anthropic Models** (Default + Sonnet + Haiku slots, + Opus 4.6)
- `opus` / `claude-opus-4.7` → Claude Opus 4.7
- `claude-opus-4.6` → Claude Opus 4.6
- `sonnet` / `claude-sonnet-4.6` → Claude Sonnet 4.6
- `haiku` / `claude-haiku-4.5` → Claude Haiku 4.5

**Chinese Providers**
- `kimi` / `kimi-k2.6` → Moonshot Kimi K2.6
- `glm` / `glm-4.6` → Zhipu GLM-4.6
- `qwen` / `qwen3-max` → Alibaba Qwen3-Max

**Reasoning Models**
- `deepseek-v3` → DeepSeek V3 (latest)
- `deepseek-r1` → DeepSeek R1 (reasoning)

**Google**
- `gemini-pro` / `gemini-2.5-pro` → Google Gemini 2.5 Pro

**OpenAI**
- `gpt4` / `gpt-4` → GPT-4
- `gpt4-turbo` / `gpt-4-turbo` → GPT-4 Turbo

> Routed through LiteLLM 1.83.14 at `http://127.0.0.1:4000`, using OpenRouter backend.
> Last updated: 2026-05-08

## Instructions

When the user requests a model switch:

1. **Parse the request** - Identify which model they want from their natural language:
   - English names: “switch to kimi”, “use GLM-4”, “change to qwen”, “try gemini”
   - Chinese names: “切换到智谱”, “用月之暗面”, “换成通义千问”, “试试Gemini”
   - Informal references: “用kimi”, “试试GLM”, “deepseek的推理版”

2. **Map to exact model ID** - Use short aliases OR full names:
   - `opus`, `sonnet`, `haiku` → map to claude-{opus,sonnet,haiku}-4.X (Opus/Sonnet/Haiku slots)
   - `claude-opus-4.6`, `kimi`, `glm`, `qwen`, `deepseek-v3`, `deepseek-r1`, `gemini-pro`, `gpt4`, `gpt4-turbo` → map to custom slot
   - For ambiguous requests, suggest options and ask user to clarify
   - Always confirm the exact model name being switched to

3. **Read current settings** - Use Read tool to check `~/.claude/settings.json`:
   - Current `ANTHROPIC_DEFAULT_OPUS_MODEL`
   - Current `ANTHROPIC_DEFAULT_SONNET_MODEL`
   - Current `ANTHROPIC_DEFAULT_HAIKU_MODEL`
   - Current `ANTHROPIC_CUSTOM_MODEL_OPTION` (Custom slot)

4. **Update settings.json** - Based on which slot user is switching:

   **If switching to Opus/Sonnet/Haiku:**
   - Change the corresponding `ANTHROPIC_DEFAULT_*_MODEL` field to the new model ID
   - Example: `”ANTHROPIC_DEFAULT_OPUS_MODEL”: “claude-opus-4.7”` → `”gpt-4”` (if switching to GPT-4 for that slot)
   - Always update `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` + `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` to match
   
   **If switching Custom slot (for non-Claude models):**
   - Change `ANTHROPIC_CUSTOM_MODEL_OPTION` to the new model ID (e.g., `kimi-k2.6`)
   - Update `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` and `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` accordingly
   - Example names: “Kimi K2.6”, “GLM-4.6”, “Qwen3-Max”, “Gemini 2.5 Pro”, etc.

5. **Confirm the change** - Tell the user:
   ```
   ✅ 模型已切换成功！
   
   从: [旧模型名称]  
   到: [新模型名称]
   
   📋 配置已更新:
   ✓ settings.json 已修改
   
   重启 Claude Code 扩展后生效，或在 /model 菜单中选择新模型。
   ```

## Special Cases

- **Ambiguous requests**: If user says "快点的模型" or "最好的", suggest 3 options and ask to pick
- **Unknown models**: If requesting a model not in the supported list, list all available models
- **Already using**: If they're already using the requested model, acknowledge and ask if they want to switch anyway
- **Settings file issues**: If unable to read/write settings.json, explain the issue and suggest remediation

## Validation Checklist

After any model switch, verify:

```
✓ Step 1: settings.json is valid JSON
✓ Step 2: Updated field (OPUS/SONNET/HAIKU/CUSTOM_OPTION) has correct value
✓ Step 3: NAME and DESCRIPTION fields updated to match
✓ Step 4: Read settings.json to confirm all changes persisted
```

Example validation output:
```
┌────────── ✅ 配置更新成功 ──────────┐
│                                    │
│ ✓ settings.json 已更新             │
│ ✓ ANTHROPIC_CUSTOM_MODEL_OPTION    │
│   = kimi-k2.6                      │
│ ✓ NAME = Kimi K2.6                │
│ ✓ DESCRIPTION = Moonshot...        │
│                                    │
│ 📝 重启 Claude Code 或用 /model     │
│    菜单选择新模型立即生效           │
│                                    │
└────────────────────────────────────┘
```

## Examples

**Example 1: Normal switch to Custom slot**
```
User: "切换到kimi"

Process:
1. Parse "kimi" → model_id = "kimi-k2.6"
2. Read ~/.claude/settings.json to get current ANTHROPIC_CUSTOM_MODEL_OPTION
3. Update settings.json:
   - ANTHROPIC_CUSTOM_MODEL_OPTION = "kimi-k2.6"
   - ANTHROPIC_CUSTOM_MODEL_OPTION_NAME = "Kimi K2.6"
   - ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION = "Moonshot Kimi K2.6 via LiteLLM"
4. Validate settings.json is valid JSON ✓
5. Confirm changes persisted ✓

Result:
✅ 模型已切换成功！

从: Kimi K2.6
到: Kimi K2.6

📋 配置已更新:
✓ settings.json 已修改
✓ ANTHROPIC_CUSTOM_MODEL_OPTION = kimi-k2.6

重启 Claude Code 或在 /model 菜单中选择 "Kimi K2.6" 槽位立即生效。
```

**Example 2: Ambiguous request**
```
User: "换个快点的模型"

Action:
→ Ask: "您想要哪个快速模型？推荐：
   1. claude-haiku-4.5 (Claude快速版) - 质量最好，便宜
   2. qwen3-max (通义千问) - 快速、质量好
   3. deepseek-v3 (DeepSeek V3) - 性价比高"
```

**Example 3: Switch Default slot (Opus)**
```
User: "把默认模型改成 GPT-4"

Process:
1. Parse "gpt-4" → model_id = "gpt-4"
2. Update settings.json:
   - ANTHROPIC_DEFAULT_OPUS_MODEL = "gpt-4"
   - ANTHROPIC_DEFAULT_OPUS_MODEL_NAME = "GPT-4"
   - ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION = "OpenAI GPT-4 via LiteLLM"
3. Validate and confirm ✓

Result:
✅ 默认模型已切换成功！

从: Claude Opus 4.7
到: GPT-4

重启后 /model 菜单中的 "Default (recommended)" 将显示 GPT-4。
```

## Error Handling

### General Principles
- Handle all file operations with try-catch; never let errors crash the flow
- Provide clear, actionable error messages in both Chinese and English
- Always validate JSON syntax after every file modification
- Maintain data integrity - only update fields that need changing, preserve others

### Specific Scenarios

**❌ File not found errors:**
```
Issue: ~/.claude/settings.json 不存在或无法读取
Action: 显示文件路径，建议用户检查文件权限或重启 Claude Code
```

**❌ JSON parsing errors:**
```
Issue: settings.json 包含无效 JSON (e.g., 多余逗号、引号不匹配)
Action: 
  1. 显示具体错误行号
  2. 备份原文件 (settings.json.bak)
  3. 提示用户手动修复或恢复备份
```

**❌ Permission denied:**
```
Issue: 无法写入配置文件（权限不足）
Action: 提示用户检查文件权限或以管理员身份运行 Claude Code
```

**⚠️ Model validation errors:**
```
Issue: 用户请求的模型不在 LiteLLM 挂载列表中
Action:
  1. 确认用户输入是否有拼写错误
  2. 列出所有可用模型（见 Supported Models 章节）
  3. 建议最接近的匹配模型
```

**⚠️ LiteLLM 不可达:**
```
Issue: http://127.0.0.1:4000 无响应（LiteLLM 进程未启动）
Action:
  1. 提示用户 SessionStart hook 将自动拉起 LiteLLM
  2. 建议手动检查：curl http://127.0.0.1:4000/health/liveliness
  3. 如需手动启动：litellm --config ~/.claude/litellm/config.yaml --port 4000
```

### Recovery Steps
- If settings.json is corrupted, restore from backup or regenerate from scratch
- If LiteLLM fails to start, check logs at `~/.claude/litellm/logs/litellm.log`
- Always end error messages with actionable next steps