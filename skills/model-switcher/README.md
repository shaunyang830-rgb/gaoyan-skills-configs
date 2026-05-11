# Model-Switcher Skill - Quick Reference

## What is model-switcher?

A Claude Code skill that allows you to quickly switch between different AI models while automatically keeping your configurations in sync across Claude Code and Claudian (Obsidian plugin).

## Why is this important?

**Before this improvement:**
- Switching models in Claude Code didn't always update Claudian's config
- Result: OpenRouter would still bill for the old model
- You'd see different models in your UI vs. what you're actually charged for

**After this improvement:**
- Every model switch automatically syncs both systems
- Validation ensures both configs match
- OpenRouter bills correctly

## Quick Start

### Switch Models
```
/model-switcher kimi
/model-switcher switch to glm4
/model-switcher 切换到通义千问
```

### Check Configuration
```bash
python3 ~/.claude/skills/model-switcher/validate-config.py
```

This script will:
- ✓ Check Claude Code configuration
- ✓ Check Claudian configuration (if present)
- ✓ Verify both systems are using the same model
- ✓ Report any mismatches or errors
- ✓ Suggest quick fixes

## Expected Output (Success)

```
[GREEN] STATUS: CONFIGURATION IS CONSISTENT

[PASS] All checks passed!
   Your configurations are in sync.
   OpenRouter will bill correctly.
```

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | Official skill documentation with validation details |
| `prompt.md` | Implementation guide for the skill |
| `validate-config.py` | Standalone tool to verify config consistency |
| `IMPROVEMENTS.md` | Detailed changelog of what was improved |
| `README.md` | This file |

## Supported Models

**Anthropic**
- sonnet, opus, haiku, claude3-sonnet, claude3-haiku

**Chinese LLMs**
- kimi (Moonshot), glm4 (Zhipu), qwen-turbo/plus/max (Alibaba), deepseek, deepseek-v3, step1, ernie-bot, minimax

**OpenAI**
- gpt4, gpt4-turbo, gpt35-turbo

**Open Models**
- llama3-70b, llama3-8b, mistral-large, gemini-pro

## How Does It Work?

### Configuration Files

1. **Claude Code** - `~/.claude/settings.json`
   - Stores the active model as a full runtime ID
   - Example: `open_router/moonshotai/kimi-k2.6`

2. **Claudian** - `Obsidian Vault/.claude/claudian-settings.json`
   - Stores the model as an alias
   - Example: `kimi`
   - Only used if `loadUserClaudeSettings=true`

### Sync Process

When you switch models:

1. **Parse** - Understand which model you want
2. **Resolve** - Find the full runtime ID in `modelOverrides`
3. **Update Claude Code** - Set the runtime ID in `~/.claude/settings.json`
4. **Update Claudian** - Set the alias in `claudian-settings.json`
5. **Validate** - Verify both files are consistent
6. **Report** - Show you the results with detailed info

## Troubleshooting

### "Configuration has errors" - Model Mismatch

This means:
- Claude Code is using a different model than Claudian
- OpenRouter will bill based on Claudian's setting
- Solution: Run model-switcher again to sync

### "loadUserClaudeSettings = false"

This means:
- Claudian is not currently active
- Only Claude Code settings matter
- This is fine, but sync still happens for consistency

### Validation Script Shows Errors

Run the validator to diagnose:
```bash
python3 ~/.claude/skills/model-switcher/validate-config.py
```

Common issues:
1. **Model not found** - Check spelling of model name
2. **Permission denied** - File permission issue
3. **Invalid JSON** - Config file corrupted, may need repair

## Advanced Usage

### Manual Sync (if needed)

Edit `Obsidian Vault/.claude/claudian-settings.json`:
```json
{
  "model": "kimi",
  "lastClaudeModel": "kimi",
  "lastCustomModel": "",
  "loadUserClaudeSettings": true,
  ...
}
```

Then verify:
```bash
python3 ~/.claude/skills/model-switcher/validate-config.py
```

### Check What's in modelOverrides

```bash
# View all available models
python3 -c "import json; data=json.load(open(os.path.expanduser('~/.claude/settings.json'))); [print(f'{k} → {v}') for k,v in data['modelOverrides'].items()]"
```

## Performance Tips

- Model switching is instant (just updates config files)
- New conversations will use the new model immediately
- Current conversation still uses the old model (switch models only affects new conversations)
- Validation is fast (< 1 second)

## Bug Reports & Feedback

If something doesn't work:

1. Run the validation script to gather diagnostics
2. Check the error messages carefully
3. Verify file permissions are correct
4. If stuck, see the troubleshooting section above

## See Also

- `IMPROVEMENTS.md` - Detailed changelog and fixes
- `SKILL.md` - Full technical documentation
- `prompt.md` - Implementation details

---

**Last Updated:** 2026-05-05  
**Status:** ✅ Fully operational with Claudian synchronization
