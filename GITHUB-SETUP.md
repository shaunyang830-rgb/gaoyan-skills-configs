# GitHub 推送步骤指南

## 现状

✅ 本地 git 仓库已初始化  
✅ 所有文件已提交到本地 git  
⏳ 等待推送到 GitHub

## 快速开始（4 步）

### 第一步：在 GitHub 创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `claude-configs-skills` (或你喜欢的名字)
   - **Description**: `My Claude Code skills, configurations, and agent strategies`
   - **Visibility**: 选择 **Public**（想公开分享）或 **Private**（只有你能访问）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
3. 点击 **Create repository**

你会看到一个页面，上面有推送命令。记住你的仓库 URL（看起来像 `https://github.com/YOUR_USERNAME/claude-configs-skills.git`）

### 第二步：配置远程仓库

在命令行执行（用你的实际 URL 替换）：

```bash
cd ~/claude-configs-skills
git remote add origin https://github.com/YOUR_USERNAME/claude-configs-skills.git
git branch -M main
git push -u origin main
```

**说明**：
- `git remote add origin ...` - 连接到 GitHub 仓库
- `git branch -M main` - 将主分支重命名为 main（GitHub 默认分支）
- `git push -u origin main` - 推送本地代码到 GitHub

### 第三步：输入 GitHub 凭证

系统会提示输入凭证：

**选项 A：使用 GitHub Personal Access Token（推荐）**

1. 获取 token：https://github.com/settings/tokens
   - 点击 "Generate new token"
   - Scope 选择：`repo`（完全仓库访问）
   - 复制生成的 token
2. 在 terminal 中粘贴 token 作为密码

**选项 B：使用 GitHub CLI（最简单）**

```bash
# 安装 GitHub CLI（如果没有）
# Windows: 访问 https://cli.github.com/ 下载
# 或 choco install gh

gh auth login
# 选择 GitHub.com
# 选择 HTTPS
# 选择 Paste an authentication token
# 粘贴你的 token

# 然后推送
git push -u origin main
```

### 第四步：验证推送成功

执行：
```bash
git log --oneline -1
# 应该显示：2ad0bc6 Initial commit: Claude Code skills and configurations package

git remote -v
# 应该显示你的 GitHub 仓库 URL
```

访问你的 GitHub 仓库页面（`https://github.com/YOUR_USERNAME/claude-configs-skills`），应该看到所有文件。

---

## 分享你的仓库

推送成功后，你可以分享仓库链接给别人：

### 公开分享

```
https://github.com/YOUR_USERNAME/claude-configs-skills
```

别人可以：
```bash
git clone https://github.com/YOUR_USERNAME/claude-configs-skills.git
cd claude-configs-skills
# 然后按照 INSTALLATION.md 的步骤安装
```

### 私人分享

如果仓库是 Private，你可以：
1. 在 GitHub 仓库页面点击 **Settings**
2. 选择 **Collaborators**
3. 添加他们的 GitHub 用户名

---

## 常见问题

### Q1: 我没有 GitHub 账户怎么办？

```bash
# 访问 https://github.com/signup 注册一个免费账户
```

### Q2: 推送时出现 "Authentication failed"

```bash
# 确认你的 token 有效
# 或使用 GitHub CLI
gh auth logout
gh auth login
```

### Q3: 如何更新仓库（添加新 skills）？

```bash
# 在本地修改文件后
cd ~/claude-configs-skills
git add .
git commit -m "Add new skill: xyz"
git push
```

### Q4: 如何创建发布版本（Release）？

```bash
# 创建标签
git tag -a v1.0 -m "Version 1.0 - Initial skills release"

# 推送标签到 GitHub
git push origin v1.0

# 然后在 GitHub 上创建 Release（可视化界面）
```

---

## 推送命令速查

```bash
# 完整的推送命令（复制粘贴即用）
cd ~/claude-configs-skills
git remote add origin https://github.com/YOUR_USERNAME/claude-configs-skills.git
git branch -M main
git push -u origin main

# 后续更新（简单）
cd ~/claude-configs-skills
git add .
git commit -m "描述你的更改"
git push
```

---

## ✅ 完成后

推送成功后：

1. ✅ 你的 skills 和配置已备份到 GitHub
2. ✅ 可以与他人分享
3. ✅ 有完整的版本历史
4. ✅ 可以在任何地方克隆恢复

---

**需要帮助？** 查看 [README.md](./README.md) 或 [INSTALLATION.md](./INSTALLATION.md)

---

**最后更新**: 2026-05-11
