@echo off
chcp 65001 >nul
echo ========================================
echo   AI掘金头条新闻系统 - 数据库导入脚本
echo ========================================
echo.

set SQL_FILE=D:\BaiduNetdiskDownload\项目物料\02-数据库sql文件\database.sql

if not exist "%SQL_FILE%" (
    echo 错误: 未找到SQL文件
    echo 文件路径: %SQL_FILE%
    pause
    exit /b 1
)

echo SQL文件已找到: %SQL_FILE%
echo.
echo 请输入MySQL root密码（输入时不会显示）:
mysql -u root -p < "%SQL_FILE%"

if errorlevel 1 (
    echo.
    echo 错误: 数据库导入失败
    echo 请检查:
    echo   1. MySQL是否已安装并正在运行
    echo   2. root密码是否正确
    echo   3. 是否有足够的权限
    pause
    exit /b 1
)

echo.
echo ========================================
echo   数据库导入成功！
echo ========================================
echo.
echo 验证导入结果:
mysql -u root -p -e "USE news_app; SHOW TABLES; SELECT COUNT(*) as news_count FROM news;"

echo.
echo 下一步:
echo   1. 修改 config/db_config.py 中的数据库密码
echo   2. 运行 start.bat 启动服务
echo.
pause
