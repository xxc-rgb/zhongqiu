# 中秋快乐 · 峰和岩

一个使用 Pygame 程序化绘制的中秋动态贺卡 MVP：以“峰岩”为视觉主角，月亮、远山、岩石、云海、星尘和流星组成一幅可实时播放的夜景。

## 运行

```powershell
py -m pip install -r requirements.txt
py main.py
```

如果系统的 `py` 启动器不可用，也可以替换为本机 Python 可执行文件运行。

快捷键：

- `Space`：暂停/继续
- `R`：重置动画
- `F`：切换全屏
- `Esc`：退出

## 测试

```powershell
py -m unittest discover -s tests -v
```

测试会在 SDL dummy 视频驱动下验证场景初始化、更新、绘制、缩放和最小事件循环。
