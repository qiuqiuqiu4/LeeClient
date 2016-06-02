@echo off
setlocal EnableDelayedExpansion

echo --------------------------------------------------------------------------------
echo                             rAthenaCN 开发团队出品
echo                     _               ____ _ _            _
echo                    ^| ^|    ___  ___ / ___^| (_) ___ _ __ ^| ^|_
echo                    ^| ^|   / _ \/ _ \ ^|   ^| ^| ^|/ _ \ '_ \^| __^|
echo                    ^| ^|__^|  __/  __/ ^|___^| ^| ^|  __/ ^| ^| ^| ^|_
echo                    ^|_____\___^|\___^|\____^|_^|_^|\___^|_^| ^|_^|\__^|
echo.
echo                               http://rathena.cn/
echo.
echo              rAthenaCN 模拟器仅供研究学习使用，切莫用于商业用途。
echo          对使用 rAthenaCN 带来的法律责任，rAthenaCN 开发团队概不负责！
echo.
echo --------------------------------------------------------------------------------
:main
	rem 列出RagexeClient目录下的所有文件夹名称，并存到 ClientArray 数组
	set index=0
	for /D %%i in (.\RagexeClient\*) do (
		set _DirectoryPath=%%i
		set _ClientVersion=!_DirectoryPath:~-10!
		set /a index=index+1
		set ClientArray[!index!]=!_ClientVersion!
	)
	
	echo [信息] 以下为目前 LeeClient 支持的客户端版本:
	echo.
	for /l %%n in (1,1,!index!) do (
		echo        [%%n] - !ClientArray[%%n]!
	)
	echo.
	rem 让用户选择其中一个
	set /p input=[选择] 想以哪个客户端版本为基础来进行初始化, 请填写其中括号里的数字[1-!index!]:
	if %input% lss 1 (
		echo [错误] 填写的序号不能小于1, 请重新输入...
		echo.
		goto main
	)
	if %input% gtr !index! (
		echo [错误] 填写的序号不能大于!index!, 请重新输入...
		echo.
		goto main
	)
	
	echo [信息] 选择以 !ClientArray[%input%]! 为基础...
	echo.
	echo [注意] 确认执行后, 此脚本将会完成以下工作:
	echo.
	echo        - 将 RagexeClient/!ClientArray[%input%]!/Basic 中的文件覆盖到 LeeClient 根目录
	echo.
:confirm
	set /p confirm=[选择] 确定要执行以上初始化操作吗?(y/n)
	
	if /i "%confirm%"=="n" exit
	if /i "%confirm%"=="y" goto initial
	echo [错误] 只能选择 y 或者 n 请重新输入
	echo. & goto confirm
:initial
	rem 将选中的 RagexeClient/{date}/Basic 目录中的全部，覆盖到 LeeClient 根目录
	echo.
	echo [信息] 正在复制文件, 请耐心等候...
	xcopy ".\RagexeClient\!ClientArray[%input%]!\Basic" "..\" /s /e /h /q /y
	echo [信息] 文件复制完毕, 初始化已完成!...
	echo.
	echo [信息] 如需重新初始化, 请先执行 clean.bat 进行清理...
	echo.
pause