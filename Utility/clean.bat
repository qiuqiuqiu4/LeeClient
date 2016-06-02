@echo off

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
	echo [信息] 是否清理 LeeClient 根目录, 使其回到刚下载时的状态?
	echo.
	echo [注意] 此脚本将会完成以下工作:
	echo.
	echo        - 移除根目录下的 _tmpEmblem ^| memo ^| Replay ^| savedata 文件夹
	echo        - 移除 data/luafiles514 文件夹
	echo        - 移除 data/msgstringtable.txt 文件
	echo        - 移除根目录下除了 setup.exe 之外的一切 exe 文件
	echo.
	set /p input=[选择] 确认要进行清理吗?(y/n)
	if /i "%input%"=="n" exit
	if /i "%input%"=="y" goto clean
	echo. & goto main
:clean
	echo.
	if exist "..\_tmpEmblem" (
		rd /q /s "..\_tmpEmblem"
	)
	if exist "..\memo" (
		rd /q /s "..\memo"
	)
	if exist "..\Replay" (
		rd /q /s "..\Replay"
	)
	if exist "..\savedata" (
		rd /q /s "..\savedata"
	)
	if exist "..\data\luafiles514" (
		rd /q /s "..\data\luafiles514"
	)
	if exist "..\data\msgstringtable.txt" (
		del /q "..\data\msgstringtable.txt"
	)
	
	rem =================================================
	rem 移除根目录下除了 setup.exe 之外的一切 exe 文件
	rem =================================================
	for %%i in (..\*.exe) do (
		if  /i not "%%i"=="..\setup.exe" (
			del /q "%%i"
		)
	)
	
	echo [信息] 清理完毕...
pause