---
name: lovart-image-gen
description: 使用 Lovart OpenClaw 生成图像。当用户说"用lovart生图"、"lovart画图"、"lovart生成"、"龙虾生图"、"龙虾画图"、"lovart image"时触发。需要预先设置 LOVART_ACCESS_KEY 和 LOVART_SECRET_KEY 环境变量。
---

# Lovart OpenClaw 图像生成 Skill

## 认证

使用前需设置环境变量：
```
LOVART_ACCESS_KEY=ak_xxx
LOVART_SECRET_KEY=sk_xxx
```

当前已配置（从用户提供的密钥）：
- Access Key: `ak_2324d3ef5ae927c4f23f694a1ac5893f`
- Secret Key: `sk_1071c58e546ebe10e815e88161f4a002e048afe93ad60078005018fa41d2041c`

## 使用流程

1. 读取用户的图像描述（prompt）
2. 调用 `scripts/generate.py` 脚本执行生成
3. 将结果图片保存到 vault 的 `Gaoyan Projects/其他/` 目录

## 执行

```bash
python "C:/Users/杨顺/.claude/skills/lovart-image-gen/scripts/generate.py" \
  --prompt "用户的图像描述" \
  --output "C:/Users/杨顺/Documents/Obsidian Vault/Gaoyan Projects/其他/"
```

## 参数说明

- `--prompt`：图像描述（必填）
- `--output`：保存目录（默认 vault 的 Gaoyan Projects/其他/）
- `--width`：宽度（可选，默认 1024）
- `--height`：高度（可选，默认 1024）
- `--style`：风格（可选）
