@echo off
chcp 65001 >nul
echo ========================================
echo   AI头条新闻系统 - 快速启动脚本
echo ========================================
echo.

echo [1/3] 检查虚拟环境...
if not exist ".venv\Scripts\python.exe" (
    echo 错误: 未找到虚拟环境，请先创建虚拟环境
    pause
    exit /b 1
)
echo ✓ 虚拟环境存在

echo.
echo [2/3] 检查依赖包...
.venv\Scripts\pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    .venv\Scripts\pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
) else (
    echo ✓ 依赖包已安装
)

echo.
echo [3/3] 启动后端服务...
echo.
echo ========================================
echo   服务即将启动
echo   API文档: http://127.0.0.1:8000/docs
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

.venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
