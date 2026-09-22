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

## 浏览器版本

浏览器入口在 `web/index.html`，不依赖 Python 或第三方库，直接用浏览器打开即可预览。
也可以在项目根目录启动静态服务器：

```powershell
py -m http.server 8000
```

然后访问 `http://localhost:8000/web/`。部署 `web/` 目录到 GitHub Pages、Netlify 或 Vercel 后，即可生成可分享给他人的公开链接。
