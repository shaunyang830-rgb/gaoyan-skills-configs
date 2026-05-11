# Model Switcher - Enhanced Implementation

## Core Task
Implement complete model switching with full Claudian synchronization and validation.

## Step-by-Step Workflow

### Phase 1: Parse & Validate User Request
1. Extract model name from user's natural language request
   - Accept both English and Chinese names
   - Accept aliases and informal references
2. Resolve to exact model alias from supported list
3. If ambiguous, ask user to choose
4. Confirm with user before proceeding

### Phase 2: Read Current Configurations
1. Read `~/.claude/settings.json`
   - Extract `model` field (current runtime ID)
   - Extract `modelOverrides` (available model mappings)
2. Look for Claudian config at `Obsidian Vault/.claude/claudian-settings.json`
   - If exists: read and parse
   - If missing: note it (not an error, may not be using Claudian)
3. Store old model info for reporting

### Phase 3: Resolve Model Alias to Runtime ID
1. Look up user's requested alias in `modelOverrides`
2. Get the full runtime ID (e.g., `open_router/moonshotai/kimi-k2.6`)
3. Validate that runtime ID is properly formatted
4. If not found, suggest closest matches and ask user to clarify

### Phase 4: Update Claude Code Configuration
1. Read `~/.claude/settings.json` again to ensure fresh copy
2. Update the `model` field to the resolved runtime ID
3. Do NOT modify `modelOverrides` unless user explicitly requests
4. Write back using Edit tool with precise old_string matching
5. Verify JSON syntax is valid after update

### Phase 5: Synchronize Claudian Configuration (CRITICAL)
**This is the key to fixing the OpenRouter bug!**

**5a. Check if Claudian config exists**
```bash
ls -la "Obsidian Vault/.claude/claudian-settings.json"
```

**5b. If Claudian config exists, sync immediately**
Execute this Python script via Bash:
```python
import json
import os
from pathlib import Path

# Find Obsidian Vault
vault_path = None
for possible_path in [
    os.path.expanduser("~/Documents/Obsidian Vault"),
    os.path.expanduser("~/Obsidian Vault"),
    "./Obsidian Vault"
]:
    if os.path.exists(possible_path):
        vault_path = possible_path
        break

if vault_path:
    claudian_config_path = os.path.join(vault_path, ".claude", "claudian-settings.json")
    
    if os.path.exists(claudian_config_path):
        try:
            # Read current Claudian config
            with open(claudian_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Update with new model alias
            config["model"] = "{model_alias}"
            config["lastClaudeModel"] = "{model_alias}"
            config["lastCustomModel"] = ""
            # Keep loadUserClaudeSettings as-is
            
            # Write back
            with open(claudian_config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Claudian config synced successfully")
        except Exception as e:
            print(f"✗ Error syncing Claudian config: {e}")
    else:
        print(f"ℹ Claudian config not found at {claudian_config_path}")
else:
    print("ℹ Obsidian Vault not found")
```

**5c. If Claudian config missing (but Obsidian vault exists)**
Create default Claudian config:
```python
{
  "model": "{model_alias}",
  "thinkingBudget": "off",
  "effortLevel": "high",
  "enableAutoTitleGeneration": false,
  "lastClaudeModel": "{model_alias}",
  "lastCustomModel": "",
  "loadUserClaudeSettings": true,
  "userScriptsEnabled": false
}
```

### Phase 6: Comprehensive Validation & Verification
**This prevents the "switched but OpenRouter still charges wrong model" bug**

**6a. Verify Claude Code Configuration**
```python
# Read ~/.claude/settings.json
# Confirm: model field = full runtime ID ✓
# Confirm: JSON parses without errors ✓
# Confirm: model value exists in modelOverrides ✓
```

**6b. Verify Claudian Configuration (if exists)**
```python
# Read claudian-settings.json
# Confirm: model field = alias (e.g., "kimi") ✓
# Confirm: lastClaudeModel field = alias ✓
# Confirm: lastCustomModel field = "" (empty) ✓
# Confirm: JSON parses without errors ✓
# Confirm: loadUserClaudeSettings = true ✓
```

**6c. Cross-validate Both Files**
```python
# Extract model alias from Claude Code runtime ID
#   e.g., "open_router/moonshotai/kimi-k2.6" → "kimi"
# Compare with Claudian model field
# Result: MUST MATCH exactly or resync failed!
```

**6d. Validation Results Report**
Generate detailed report:
```
┌─ VALIDATION REPORT ─────────────────────────┐
│                                             │
│ ✓ Claude Code config readable              │
│ ✓ Claude Code model updated correctly       │
│ ✓ Claudian config found & readable         │
│ ✓ Claudian model field synced              │
│ ✓ Claudian lastClaudeModel synced          │
│ ✓ Cross-validation: both files consistent  │
│                                             │
│ Status: ✅ ALL CHECKS PASSED               │
└─────────────────────────────────────────────┘
```

### Phase 7: Confirm Success to User
Provide detailed report in both English and Chinese:

**Success Report Format:**
```
✅ 模型已切换成功！Model switched successfully!

从: [OLD_MODEL_NAME]  
到: [NEW_MODEL_NAME] ([RUNTIME_ID])

📋 配置同步状态 Configuration Sync Status:
✓ Claude Code settings.json 已更新 ✓ Updated
✓ Claudian 配置已同步 ✓ Synced  
✓ 两个系统配置一致 ✓ Configs are consistent

🚀 新的对话将使用 [NEW_MODEL_NAME]。
   New conversations will use [NEW_MODEL_NAME].
   
💡 当前对话仍使用之前的模型，请开始新的对话来体验新模型。
   Current conversation still uses previous model. Start a new one to use the new model.

🔍 验证结果 Validation Results:
   ✓ Claude Code config: {RUNTIME_ID}
   ✓ Claudian config: {ALIAS}
   ✓ Cross-check: PASSED
```

**Partial Failure Report (if Claudian sync fails):**
```
⚠️ 模型在 Claude Code 中已切换，但 Claudian 同步遇到问题
   Model switched in Claude Code, but Claudian sync encountered issues.

从: [OLD_MODEL_NAME]
到: [NEW_MODEL_NAME]

问题 Issue:
[SPECIFIC_ERROR_MESSAGE]

建议 Recommendation:
[ACTION_STEPS_TO_FIX]

立即修复? Do you want me to fix it now?
```

## Error Handling & Recovery

### Error Type: File Not Found
**Symptom:** Cannot read ~/.claude/settings.json or claudian-settings.json
**Action:**
1. Display exact file path
2. Suggest: check file permissions, restart Claude Code
3. Offer manual editing instructions if needed

### Error Type: Invalid JSON
**Symptom:** File exists but contains malformed JSON
**Action:**
1. Show error line number and problematic character
2. Create backup (e.g., claudian-settings.json.bak)
3. Attempt automatic repair (remove trailing commas, fix quotes)
4. Validate after repair
5. If repair fails, provide manual fix instructions

### Error Type: Permission Denied
**Symptom:** Cannot write to configuration file
**Action:**
1. Explain permission issue
2. Provide chmod command for Linux/Mac
3. Suggest running as administrator on Windows
4. Alternative: create new file in temp location and move

### Error Type: Configuration Mismatch Detected
**Symptom:** During validation, Claude Code and Claudian have different models
**Action:**
1. Display both current values
2. Resync Claudian to match Claude Code immediately
3. Re-validate both files
4. Report auto-correction to user

### Error Type: Model Not Found
**Symptom:** User requests model not in modelOverrides
**Action:**
1. Check for typos/spelling errors
2. List all available models with aliases
3. Suggest closest matches
4. Ask user to clarify their choice

## Special Cases

### Case: User already on target model
- Claude Code AND Claudian both show target model
- Action: Politely inform user "You're already using [MODEL]"
- Do NOT make unnecessary file changes

### Case: Claudian inactive but config exists
- Claudian config found but loadUserClaudeSettings = false
- Action: Still sync it anyway (for consistency when user later activates Claudian)
- Do NOT enable loadUserClaudeSettings unless user requests

### Case: Multiple Obsidian vaults
- Multiple .claude directories found
- Action: Ask user which vault to sync to
- Default to most recently modified one if user doesn't specify

## Implementation Checklist

Before confirming success:
- [ ] Parsed user request correctly
- [ ] Resolved to correct model alias
- [ ] Confirmed with user before changing files
- [ ] Read Claude Code settings.json successfully
- [ ] Updated model field to correct runtime ID
- [ ] Verified JSON syntax after update
- [ ] Checked for Claudian config
- [ ] If Claudian exists, synced model, lastClaudeModel, lastCustomModel
- [ ] Ran all 4 validation checks (Claude Code, Claudian, Cross-validate, Report)
- [ ] All validation checks PASSED
- [ ] Reported success/failure with detailed info to user
- [ ] Provided actionable next steps

## Key Points to Remember

1. **This skill is fixing a real bug:** Users were switching models in Claude Code but still getting charged for the old model by OpenRouter. The root cause: Claudian config wasn't syncing.

2. **Validation is NOT optional:** Many users thought they switched successfully when really the Claudian config was stale. Validation prevents this.

3. **Report everything:** Users need to know:
   - Old → New model names
   - Whether both configs synced successfully
   - If there were any issues, what and why
   - What happens next

4. **Claudian is a real system:** It's an Obsidian plugin that maintains its own config. If it's not synced when a user switches models, OpenRouter will bill based on Claudian's config, not Claude Code's.

5. **Both files matter:**
   - ~/.claude/settings.json (Claude Code's runtime)
   - Obsidian Vault/.claude/claudian-settings.json (Claudian UI)
   - They MUST stay in sync, or chaos ensues.
