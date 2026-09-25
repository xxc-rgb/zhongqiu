@echo off
title 中秋网页 - 一键部署到 GitHub Pages
cd /d "D:\zhongqiu"

echo.
echo ============================================
echo   中秋网页  一键部署
echo ============================================
echo.

echo [1/5] 检查代理 FlyingBird (端口 7892) ...
netstat -ano | findstr "LISTENING" | findstr ":7892" >nul
if errorlevel 1 (
    echo   [失败] 没检测到端口 7892。
    echo          请先打开 FlyingBird 代理，然后再双击这个脚本。
    echo.
    pause
    exit /b 1
)
echo   代理正常
echo.

echo [2/5] 收集本次所有改动 ...
git add -A
echo   完成
echo.

echo [3/5] 生成提交记录 ...
if "%~1"=="" ( set "MSG=更新内容" ) else ( set "MSG=%~1" )
git commit -m "%MSG%"
if errorlevel 1 (
    echo   没有检测到新的改动，跳过提交步骤。
)
echo.

echo [4/5] 推送到 GitHub （大约需要 1 到 3 分钟，请不要关闭窗口）...
git push origin main
if errorlevel 1 (
    echo.
    echo   [失败] 推送出错。把窗口里的红色提示截图发给我。
    echo.
    pause
    exit /b 1
)
echo.

echo [5/5] 部署完成
echo.
echo   GitHub 正在自动生成新版页面，大约 1 分钟后刷新即可看到：
echo.
echo       https://xxc-rgb.github.io/zhongqiu/
echo.
echo   自动构建进度可以看这里：
echo       https://github.com/xxc-rgb/zhongqiu/actions
echo.
echo ============================================
echo.
pause
