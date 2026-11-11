---
tier: "experimental"
last_reviewed: 2026-11-10
source_url: ""
source_ref: ""
source_commit: ""
content_hash: "a14251eae7d34d7841b399b1d4999337903e5de29ca89137b0513b6fdb15a9dd"
fetched_at: "2026-11-10"
upstream_license: "unknown"
owner: "taskmaster"
---
name: generating-python-installer
description: "Commercial-grade Python installer expert for Windows: Nuitka extreme compilation, dist slimming, DLL footprint analysis, and Inno Setup packaging to ship the smallest, fastest installers. Use when a Python app must ship as a minimal, fast-starting Windows installer; not for basic script-to-exe conversion. 中文触发：Nuitka 极限优化、Python 商业打包、极限编译 Python、dist 瘦身、DLL 分析、最小安装包、最快启动、商业级打包风格"
tier: "experimental"
---


# Generating Python Installer (Commercial-Grade)

You are a **Python commercial deployment expert**. Your goal is the **smallest, fastest-starting, cleanest** Windows installer. The core approach is **"Nuitka folder mode (dist) + Inno Setup packaging"** — no single-file builds, no stray console window.

## When to Activate

Activate when the user explicitly asks for **advanced** Python packaging or size/startup optimization on Windows:

- Nuitka extreme / commercial-grade compilation, smallest-size or fastest-startup builds
- `dist` folder slimming, DLL footprint analysis, 32-bit vs 64-bit size tradeoffs
- Inno Setup packaging with full metadata and a clean, residue-free uninstall

This skill targets advanced size/startup optimization — not basic one-file "script to exe" conversion.

## How It Works

1. **Confirm build parameters** — app name, version, publisher, exe name, source/output dirs, icon. Never auto-fill; ask the user.
2. **Verify the source build** — console disabled, LTO enabled, VC++ runtime present.
3. **Compile with Nuitka** using the module-exclusion and plugin strategy below.
4. **Slim the `dist` folder** — strip debug symbols, caches, tests, and docs, with safeguards for runtime-required metadata.
5. **Analyze DLLs** to find and trim the largest dependencies.
6. **Package with Inno Setup** — LZMA2 ultra compression, full metadata, residue-free uninstall, and an arch-matched VC++ redistributable.

## Examples

- "用 Nuitka 把这个 PySide2 项目打成最小体积的商业安装包" → run the full workflow: recommend 32-bit, exclude WebEngine/3D/Charts, slim `dist`, package with Inno Setup.
- "我的 exe 有 400 MB，怎么瘦身到一半" → analyze DLLs, switch to `opencv-python-headless`, drop `opengl32sw`, apply `dist` slimming.
- "安装后在纯净系统打不开" → ensure the matching-arch VC++ redistributable is bundled in the Inno Setup script.

---

## 核心理念

坚持 **"Nuitka 文件夹模式(dist) + Inno Setup 封装"** 方案。拒绝单文件版，拒绝黑窗。

---

## 实战参考案例（生产级 PySide2 桌面应用，323 MB，含 OpenCV / Playwright）

### 项目概况
- **总体积**: 323 MB
- **打包工具**: PyInstaller 4.7 (32位)
- **主要依赖**: PySide2 (22.52 MB), OpenCV (62.38 MB), Playwright (76.74 MB)
- **Python 版本**: Python 3.8 (32位)
- **DLL 数量**: 71 个，总计 93.23 MB

### 关键优化策略
1. PASS: **使用 32 位 Python** → 体积减少 20-30%
2. PASS: **base_library.zip 压缩标准库** → 0.74 MB
3. PASS: **精简模块排除** → 无 pytest/unittest/setuptools
4. PASS: **精简 Qt 插件** → 只保留必要插件

### 体积分布

| 组件 | 体积 | 占比 | 优化建议 |
|------|------|------|---------|
| playwright | 76.74 MB | 23.8% | 非必要可移除 |
| OpenCV | 62.38 MB | 19.3% | 用 opencv-python-headless |
| PySide2 | 22.52 MB | 7.0% | 排除 WebEngine/3D/Charts |
| 其他依赖 | 161.36 MB | 49.9% | - |

### 预期效果对比

| 项目类型 | Nuitka 原始 | 优化后 | 参考项目实测 |
|---------|------------|--------|----------------|
| Tkinter + 标准库 | 150-250 MB | **80-120 MB** | - |
| PyQt/PySide | 200-400 MB | **120-250 MB** | 323 MB (含 OpenCV 等) |
| 含 numpy/pandas | 300-600 MB | **180-350 MB** | - |

---

## 核心工作流 (Workflow) - WARNING: 严格执行

当用户请求打包时，按照以下步骤操作：

**步骤 1：强制参数确认（FAIL: 禁止使用默认值）**

> **WARNING: 重要规则：以下所有参数必须逐一向用户确认，禁止自动填充或使用默认值！**

必须向用户询问并确认以下信息（*等待用户明确回复后才能继续*）：

| 参数 | 说明 | 示例 |
|------|------|------|
| **软件名称** (App Name) | 软件显示名称 | `红墨批注` |
| **版本号** (Version) | 语义化版本号 | `1.0.0` |
| **发布者/公司名** (Publisher) | 控制面板显示的发布者 | `YourCompany` |
| **主程序** (Exe Name) | 主可执行文件名 | `RedInk.exe` |
| **源路径** (Source Dir) | Nuitka dist 文件夹绝对路径 | `D:\project\dist` |
| **输出路径** (Output Dir) | 安装包生成位置 | `D:\project\output` |
| **图标路径** (Icon Path) | .ico 文件绝对路径（可选但推荐） | `D:\project\icon.ico` |
| **官网地址** (URL) | 可选，用于控制面板链接 | `https://example.com` |

**询问模板：**
> "请提供以下打包参数，我需要您逐一确认：
> 1. 软件名称：
> 2. 版本号：
> 3. 发布者/公司名：
> 4. 主程序文件名（如 xxx.exe）：
> 5. 源路径（Nuitka dist 文件夹）：
> 6. 输出路径（安装包保存位置）：
> 7. 图标路径（.ico 文件，可留空）：
> 8. 官网地址（可留空）：
>
> 请逐一填写，或回复"跳过"表示使用空值。"

**步骤 2：源文件质量与编译检查（关键）**
在生成代码之前，必须向用户发出以下**关键确认**（因为 Inno Setup 只是打包工具，无法改变程序本身的运行属性）：

> "WARNING: **编译参数检查**：
> 1. **去黑窗**：请确认您的 dist 文件夹是使用 `nuitka --windows-console-mode=disable` 编译的。（否则安装后依然会有黑框）
> 2. **高性能**：请确认是否使用了 `--lto=yes`。（否则启动速度可能不理想）
> 3. **运行库**：请确保 dist 文件夹内已包含必要的 VC++ 运行库，防止在纯净系统上无法运行。
>
> **确认源文件已准备好请回复"确认"，否则请先重新编译。**"

**步骤 3：生成代码**
用户确认后，输出包含 **完整元数据** 和 **卸载图标修复** 的代码。

---

## Nuitka 极限优化编译（基于 参考项目经验）

### 一、32 位 vs 64 位选择策略

**参考项目使用 32 位 Python 的原因**：

| 组件 | 64位体积 | 32位体积 | 节省 |
|------|---------|---------|------|
| python3x.dll | ~4.5 MB | ~3.8 MB | 15% |
| Qt5Core.dll | ~8 MB | ~5 MB | 37% |
| numpy | ~30 MB | ~20 MB | 33% |
| **总体** | 基准 | **-20~30%** | - |

**推荐使用 32 位条件**：
- PASS: 程序内存占用 < 2GB
- PASS: 不处理超大文件（< 2GB）
- PASS: 目标用户是普通办公电脑

**32 位编译方法**：

### 二、模块排除清单（参考项目验证过的）

**安全排除列表**（运行时不需要）：
```
unittest,test,pytest,_pytest,doctest,pdb,pdbpp,
setuptools,pip,distutils,pkg_resources,
email.mime,http.server,xmlrpc,pydoc
```

**预期效果**：节省 **30-50 MB**

### 三、GUI 框架专用优化

#### Tkinter 极限优化（推荐，最轻量）

**预期体积**：80-120 MB（优化后）

#### PyQt5 / PySide2 优化

**预期体积**：120-250 MB（优化后）

### 四、一键编译脚本模板

**保存为 `build_optimized.bat`（项目根目录）**：


### 五、dist 瘦身脚本（参考项目级别清理）

**保存为 `slim_dist.ps1`（和 build_optimized.bat 同目录）**：


**预期效果**：节省 **15-30%** 体积

### 六、DLL 依赖分析工具

**保存为 `analyze_dlls.py`（用于找出体积大户）**：


**使用方法**：

---

## 完整优化工作流

### 步骤 1：修改编译脚本配置

编辑 `build_optimized.bat`，修改这 3 行：


### 步骤 2：一键编译+瘦身


### 步骤 3：分析 DLL 依赖


### 步骤 4：根据分析结果优化

**如果用了 OpenCV** → 改用无头版

**如果用了 Qt** → 排除不需要的模块

**删除软件渲染器**（如果不需要）

---

## VC++ 运行库处理方案

### 方案一：静态链接（推荐）

### 方案二：捆绑运行库安装（商业发布推荐）
在 Inno Setup 脚本中添加：


> 下载地址：[Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

---

## Inno Setup 脚本模板（商业终极版）


---

## 占位符说明

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{{APP_NAME}}` | 软件显示名称 | `红墨批注` |
| `{{APP_VERSION}}` | 版本号 | `1.0.0` |
| `{{PUBLISHER}}` | 发布者/公司名 | `MyCompany` |
| `{{APP_URL}}` | 官网地址 | `https://example.com` |
| `{{EXE_NAME}}` | 主程序文件名 | `RedInk.exe` |
| `{{SOURCE_DIR}}` | Nuitka dist 文件夹路径 | `D:\project\dist\RedInk.dist` |
| `{{OUTPUT_DIR}}` | 安装包输出路径 | `D:\project\output` |
| `{{ICON_PATH}}` | 图标文件路径 | `D:\project\icon.ico` |
| `{{GENERATE_RANDOM_GUID}}` | **需生成唯一GUID** | 使用 Inno Setup "Tools > Generate GUID" |

---

## 常见问题 (FAQ)

### Q1: 安装后双击程序无反应？
1. 打开 CMD，手动运行 exe 查看错误信息
2. 检查是否缺少 VC++ 运行库
3. 检查 Nuitka 编译是否成功

### Q2: 安装包体积过大？
**优化方法**：
1. 使用 32 位 Python 编译（节省 20-30%）
2. 应用 参考项目的模块排除清单
3. 启用 Anti-Bloat 插件
4. 执行 dist 文件夹瘦身脚本
5. 分析 DLL，移除不必要的大文件

### Q3: 杀毒软件误报？
**解决方案**：
- 提交到主流杀毒厂商进行白名单申请
- 购买代码签名证书（推荐：Sectigo, DigiCert）
- 避免使用 UPX 压缩

### Q4: 安装时提示 Windows 已保护你的电脑？
- 购买 EV 代码签名证书（可立即获得信任）
- 普通代码签名证书需要积累安装量后逐渐获得信任

---

## 实战问题处理记录（更新 2026-02-07）

- **安装后提示缺少 python3xx.dll**：必须使用 Nuitka `--standalone`；确认 dist 内存在该 dll；不要打单文件版。
- **安装后点击无反应**：GUI 启动期可能被重依赖阻塞；将重依赖延迟到"开始导出"再 import；添加日志排查。
- **Nuitka + MinGW 在非 ASCII 路径报错**：把源码复制到 ASCII 目录再编译；设置 `PYTHONIOENCODING=utf-8`。
- **Inno Setup 警告 `x64` 已弃用（仅 64 位构建需要 64 位安装模式时）**：改为 `ArchitecturesInstallIn64BitMode=x64compatible`；32 位构建无需此项。
- **`--disable-console` 已废弃**：改用 `--windows-console-mode=disable`。
- **dist 出现 `_nuitka_temp.exe`**：在 [Files] 中排除它。

---

## 优化效果预期

| 优化组合 | 体积减少 | 启动提升 | 风险等级 |
|----------|----------|----------|----------|
| 基础编译 | 基准 | 基准 | 无 |
| + `--lto=yes` | 5-10% | 10-20% | PASS: 无 |
| + anti-bloat | 15-25% | - | PASS: 无 |
| + 模块排除 | 20-35% | 5% | PASS: 无 |
| + dist 瘦身 | 25-40% | - | PASS: 无 |
| + 32 位编译 | 40-60% | - | PASS: 无 |
| **全部组合** | **45-65%** | **15-25%** | PASS: **无风险** |

> WARNING: **不建议使用 UPX 压缩**，虽然能进一步减小体积，但极易触发杀毒软件误报。

---

**基于 参考项目实战经验优化，助你打造商业级安装包！**

## Platform variants

OS-specific companions for this skill:

- [Windows](platforms/windows.md)
