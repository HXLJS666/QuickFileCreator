# QuickFileCreator

一个轻量级的 Windows 快速文件创建工具，通过全局快捷键在资源管理器当前路径快速创建文件或文件夹。

## 程序特殊性

本程序全程使用 AI 开发，使用 Trae CN IDE 进行开发，选择 GLM-5 模型。

## 功能特性

- **全局快捷键** - 按 `Ctrl+Alt+N` 随时唤出创建窗口
- **智能识别** - 自动判断创建类型：
  - 输入 `test.txt` → 创建文件
  - 输入 `newfolder` → 创建文件夹
  - 输入 `.gitignore` → 创建隐藏文件
- **自动获取路径** - 检测当前资源管理器窗口路径
- **鼠标位置定位** - 输入框在鼠标位置显示，更好的使用体验
- **自动聚焦** - 唤出窗口后自动聚焦输入框，无需点击
- **错误提示** - 创建失败时显示红色提示，3 秒后自动隐藏
- **系统托盘** - 启动后自动最小化到托盘
- **极简界面** - 深色主题输入框，即用即走

## 安装使用

### 方式一：直接运行可执行文件

双击 `dist/QuickFileCreator.exe` 即可运行。

### 方式二：从源码运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

### 开机自启（可选）

将 `QuickFileCreator.exe` 的快捷方式放到 Windows 启动文件夹：

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

## 使用方法

1. 运行程序后，会在系统托盘显示图标
2. 打开资源管理器，导航到目标文件夹
3. 按 `Ctrl+Alt+N` 唤出输入框（在鼠标位置显示）
4. 输入名称后按 `Enter` 创建，按 `Esc` 取消
5. 如果创建失败，会显示红色错误提示
6. 右键托盘图标可查看快捷键或退出程序

## 配置说明

可在 `config.py` 中自定义以下配置：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `HOTKEY` | `ctrl+alt+n` | 全局快捷键 |
| `WINDOW_WIDTH` | `400` | 窗口宽度 |
| `WINDOW_HEIGHT` | `50` | 窗口高度 |
| `WINDOW_BG_COLOR` | `#2d2d2d` | 窗口背景色 |
| `ENTRY_BG_COLOR` | `#3d3d3d` | 输入框背景色 |
| `ENTRY_FG_COLOR` | `#ffffff` | 输入框文字颜色 |

## 打包说明

使用 PyInstaller 打包为独立可执行文件：

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "QuickFileCreator" main.py
```

## 项目结构

```
QuickFileCreator/
├── main.py            # 主程序入口，托盘和快捷键管理
├── ui.py              # 输入框窗口界面
├── explorer.py        # 获取资源管理器当前路径
├── file_creator.py    # 文件/文件夹创建逻辑
├── config.py          # 配置文件
├── requirements.txt   # 依赖列表
├── README.md          # 项目说明
├── TECHNICAL.md       # 技术文档
└── dist/
    └── QuickFileCreator.exe
```

## 依赖

- `keyboard` - 全局快捷键监听
- `pystray` - 系统托盘功能
- `Pillow` - 图标绘制
- `pywin32` - Windows API 调用
- `pyautogui` - 鼠标位置获取、自动聚焦
- `pygetwindow` - 窗口管理

## 系统要求

- Windows 10/11
- Python 3.8+（从源码运行时）

## 技术文档

如需了解更多技术实现细节，请查看 [TECHNICAL.md](./TECHNICAL.md)，包含：

- 整体架构设计
- 各模块详细说明
- 流程图和原理图
- COM 接口使用
- 焦点获取机制
- 错误提示实现

## 参考资料

- [获取资源管理器路径](https://blog.csdn.net/m0_74389553/article/details/144492444)
- [窗口焦点获取](https://blog.51cto.com/u_16213349/12645148)

## License

MIT
