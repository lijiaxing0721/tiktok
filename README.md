# 抖音视频下载工具 (Android APK)

这是一个基于 Python Kivy 和 yt-dlp 开发的安卓应用，用于下载抖音视频。

## 功能
- 解析抖音分享链接
- 下载无水印视频到手机
- 简单易用的界面

## 项目结构
- `main.py`: 主程序入口，负责 UI 界面
- `downloader.py`: 核心下载逻辑，调用 yt-dlp
- `requirements.txt`: Python 依赖库
- `buildozer.spec`: 打包成 APK 的配置文件

## 如何在 Windows 上运行 (测试)
1. 安装 Python 3.x
2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序:
   ```bash
   python main.py
   ```

## ❓ 常见问题：可以使用 HBuilderX 打包吗？
不可以。
- **原因**: HBuilderX 是针对 HTML5/JS/Vue (uni-app) 开发的工具，无法编译 Python 代码。
- **替代方案**: 本项目使用 **Buildozer**，它是专为 Python Kivy 应用设计的打包工具。
- **最简单的打包方式**: 使用 GitHub Actions (见下文)，无需在本地安装 Linux 环境。

## 🚀 如何打包成 APK (最简单方法：GitHub Actions)
无需本地配置环境，利用 GitHub 的免费云端服务器自动打包。

1. **Fork 本项目**: 将代码上传到你的 GitHub 仓库。
2. **启用 Actions**:
   - 进入仓库页面，点击顶部 `Actions` 标签。
   - 如果看到警告，点击 "I understand my workflows, go ahead and enable them"。
3. **触发构建**:
   - 可以在 `Actions` -> `Build Android APK` -> `Run workflow` 手动触发。
   - 或者直接推送代码更新，也会自动触发。
4. **下载 APK**:
   - 构建完成后（约 15 分钟），点击该次运行记录。
   - 在页面底部的 `Artifacts` 区域，点击 `package` 下载 zip 包。
   - 解压后即可得到 `.apk` 安装包。

## 🛠️ 如何在本地打包 (Linux/Mac)
如果你有 Linux 环境 (或 WSL)，可以使用命令行打包：
