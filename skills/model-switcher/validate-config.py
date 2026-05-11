#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Switcher Configuration Validator
验证 Claude Code 和 Claudian 配置是否同步

This script checks if your model configurations are consistent across:
1. ~/.claude/settings.json (Claude Code)
2. Obsidian Vault/.claude/claudian-settings.json (Claudian UI)

If configurations are out of sync, it explains why OpenRouter might be billing
you for the wrong model.
"""

import json
import os
import sys
from pathlib import Path

# Enable UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def find_obsidian_vault():
    """Find Obsidian Vault directory"""
    possible_paths = [
        os.path.expanduser("~/Documents/Obsidian Vault"),
        os.path.expanduser("~/Obsidian Vault"),
        Path.home() / "Documents" / "Obsidian Vault",
        Path.home() / "Obsidian Vault",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return str(path)
    return None

def extract_model_alias(runtime_id):
    """Extract model alias from runtime ID

    Examples:
    - open_router/moonshotai/kimi-k2.6 → kimi
    - open_router/anthropic/claude-sonnet-4.6 → sonnet
    """
    if not runtime_id or "/" not in runtime_id:
        return runtime_id

    parts = runtime_id.split("/")
    if len(parts) >= 3:
        # For open_router/provider/model-version format
        model_part = parts[2]

        # Handle special cases
        if "kimi" in model_part.lower():
            return "kimi"
        elif "glm" in model_part.lower():
            return "glm4"
        elif "qwen" in model_part.lower():
            if "turbo" in model_part:
                return "qwen-turbo"
            elif "plus" in model_part:
                return "qwen-plus"
            elif "max" in model_part:
                return "qwen-max"
        elif "deepseek" in model_part.lower():
            if "v3" in model_part:
                return "deepseek-v3"
            return "deepseek"
        elif "claude" in model_part.lower():
            if "sonnet" in model_part:
                return "sonnet"
            elif "opus" in model_part:
                return "opus"
            elif "haiku" in model_part:
                return "haiku"
        elif "step" in model_part.lower():
            return "step1"
        elif "ernie" in model_part.lower():
            return "ernie-bot"
        elif "minimax" in model_part.lower():
            return "minimax"
        elif "gpt" in model_part.lower():
            if "gpt-4-turbo" in model_part:
                return "gpt4-turbo"
            elif "gpt-4" in model_part:
                return "gpt4"
            elif "gpt-3.5" in model_part:
                return "gpt35-turbo"
        elif "llama" in model_part.lower():
            if "70b" in model_part:
                return "llama3-70b"
            elif "8b" in model_part:
                return "llama3-8b"
        elif "mistral" in model_part.lower():
            return "mistral-large"
        elif "gemini" in model_part.lower():
            return "gemini-pro"

    return runtime_id

def validate():
    """Main validation function"""
    print("\n" + "="*70)
    print("[CHECK] Model Switcher Configuration Validator")
    print("="*70 + "\n")

    errors = []
    warnings = []
    info = []

    # Step 1: Check Claude Code settings
    print("[INFO] Step 1: Reading Claude Code configuration...")
    claude_code_config = None
    claude_model = None
    model_overrides = None

    claude_path = os.path.expanduser("~/.claude/settings.json")
    if os.path.exists(claude_path):
        try:
            with open(claude_path, "r", encoding="utf-8") as f:
                claude_code_config = json.load(f)
            claude_model = claude_code_config.get("model")
            model_overrides = claude_code_config.get("modelOverrides", {})
            print(f"  [OK] Read: {claude_path}")
            print(f"  [OK] Current model: {claude_model}")
        except json.JSONDecodeError as e:
            errors.append(f"Claude Code settings.json has invalid JSON: {e}")
            print(f"  [FAIL] JSON parse error: {e}")
        except Exception as e:
            errors.append(f"Cannot read Claude Code settings.json: {e}")
            print(f"  [FAIL] Error: {e}")
    else:
        errors.append(f"Claude Code settings not found: {claude_path}")
        print(f"  [FAIL] File not found: {claude_path}")
        return

    # Step 2: Check Claudian config
    print("\n[INFO] Step 2: Checking Claudian configuration...")
    vault_path = find_obsidian_vault()
    claudian_path = None
    claudian_config = None
    claudian_model = None

    if vault_path:
        claudian_path = os.path.join(vault_path, ".claude", "claudian-settings.json")
        if os.path.exists(claudian_path):
            try:
                with open(claudian_path, "r", encoding="utf-8") as f:
                    claudian_config = json.load(f)
                claudian_model = claudian_config.get("model")
                print(f"  [OK] Found: {claudian_path}")
                print(f"  [OK] Claudian model: {claudian_model}")
            except json.JSONDecodeError as e:
                errors.append(f"Claudian settings.json has invalid JSON: {e}")
                print(f"  [FAIL] JSON parse error: {e}")
            except Exception as e:
                errors.append(f"Cannot read Claudian settings: {e}")
                print(f"  [FAIL] Error: {e}")
        else:
            info.append(f"Claudian config not found at {claudian_path} (OK if not using Claudian)")
            print(f"  [INFO]  Not found: {claudian_path}")
            print(f"  [INFO]  This is OK if you're not using Claudian")
    else:
        info.append("Obsidian Vault not found (OK if not using Claudian)")
        print(f"  [INFO]  Obsidian Vault not found")
        print(f"  [INFO]  This is OK if you're not using Claudian")

    # Step 3: Detailed validation
    print("\n" + "="*70)
    print("[PASS] VALIDATION REPORT")
    print("="*70 + "\n")

    # Check 1: Claude Code settings
    print("Check [1] : Claude Code Configuration")
    print("-" * 70)
    if claude_model:
        print(f"  [OK] Model field exists: {claude_model}")

        # Verify it's in modelOverrides
        if claude_model in model_overrides.values():
            print(f"  [OK] Model ID exists in modelOverrides")
        else:
            warnings.append(f"Model ID {claude_model} not found in modelOverrides")
            print(f"  [WARN] [WARN] Model ID not in modelOverrides!")
    else:
        errors.append("Claude Code model field is empty")
        print(f"  [FAIL] Model field is empty!")

    # Check 2: Claudian config (if exists)
    if claudian_config:
        print("\nCheck [2] : Claudian Configuration")
        print("-" * 70)

        # Extract fields
        claudian_last_claude = claudian_config.get("lastClaudeModel")
        claudian_last_custom = claudian_config.get("lastCustomModel", "")
        load_user_settings = claudian_config.get("loadUserClaudeSettings", True)

        print(f"  model: {claudian_model}")
        print(f"  lastClaudeModel: {claudian_last_claude}")
        print(f"  lastCustomModel: {claudian_last_custom}")
        print(f"  loadUserClaudeSettings: {load_user_settings}")

        # Validate fields
        if claudian_model == claudian_last_claude:
            print(f"  [OK] model == lastClaudeModel (consistent)")
        else:
            errors.append(f"Claudian model ({claudian_model}) != lastClaudeModel ({claudian_last_claude})")
            print(f"  [FAIL] model != lastClaudeModel (INCONSISTENT!)")

        if claudian_last_custom == "":
            print(f"  [OK] lastCustomModel is empty (expected)")
        else:
            warnings.append(f"lastCustomModel is not empty: {claudian_last_custom}")
            print(f"  [WARN] lastCustomModel should be empty: {claudian_last_custom}")

        if load_user_settings:
            print(f"  [OK] loadUserClaudeSettings = true (Claudian config is active)")
        else:
            warnings.append("loadUserClaudeSettings = false (Claudian config may be inactive)")
            print(f"  [WARN] loadUserClaudeSettings = false (Claudian may not be active)")

        # Check 3: Cross-validate
        print("\nCheck [3] : Cross-Validation")
        print("-" * 70)

        extracted_alias = extract_model_alias(claude_model)
        print(f"  Claude Code model ID: {claude_model}")
        print(f"  Extracted alias: {extracted_alias}")
        print(f"  Claudian model: {claudian_model}")

        if extracted_alias == claudian_model:
            print(f"  [OK] MATCH! Both systems use same model")
        else:
            errors.append(
                f"[WARN] [WARN]  MODEL MISMATCH! [WARN] [WARN]\n"
                f"    Claude Code: {claude_model}\n"
                f"    Claudian: {claudian_model}\n"
                f"    This is why OpenRouter bills you for {claudian_model}!"
            )
            print(f"  [FAIL] MISMATCH!")
            print(f"  [FAIL] Claude Code is using {extracted_alias}")
            print(f"  [FAIL] But Claudian is using {claudian_model}")
            print(f"  [FAIL] OpenRouter will bill based on Claudian's setting!")
    else:
        print("\nCheck [2] & [3]: Claudian Configuration (SKIPPED)")
        print("-" * 70)
        print("  [INFO] Claudian config not found or not using Claudian")
        print("  [INFO] Only Claude Code configuration matters in this case")

    # Summary
    print("\n" + "="*70)
    print("[REPORT] SUMMARY")
    print("="*70 + "\n")

    if errors:
        print("[ERROR] ERRORS FOUND:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        print()

    if warnings:
        print("[WARN]  WARNINGS:")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
        print()

    if info:
        print("[INFO]️  INFO:")
        for i, msg in enumerate(info, 1):
            print(f"   {i}. {msg}")
        print()

    # Final status
    if errors:
        print("[RED] STATUS: CONFIGURATION HAS ERRORS")
        print("\n⚡ ACTION REQUIRED:")
        print("   Your models are out of sync. OpenRouter is likely billing")
        print("   you for the wrong model. Please sync your configurations.")
        if claudian_config and extracted_alias != claudian_model:
            print(f"\n   Quick fix: Update Claudian model from '{claudian_model}' to '{extracted_alias}'")
        return 1
    elif warnings:
        print("[YELLOW] STATUS: CONFIGURATION HAS WARNINGS")
        print("\n💡 RECOMMENDATIONS:")
        print("   Your configuration might work, but it's not optimal.")
        print("   Consider addressing the warnings above.")
        return 0
    else:
        print("[GREEN] STATUS: CONFIGURATION IS CONSISTENT")
        print("\n[PASS] All checks passed!")
        print("   Your configurations are in sync.")
        print("   OpenRouter will bill correctly.")
        return 0

if __name__ == "__main__":
    exit_code = validate()
    sys.exit(exit_code)
