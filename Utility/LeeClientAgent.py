#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import distutils
import os
import platform
import sys

from distutils import dir_util

def atoi(val):
	'''
	用于将一个字符串尝试转换成 Int 数值
	转换成功则返回 Int 数值，失败则返回布尔类型的 False
	'''
	try:
		int(val)
		return int(val)
	except ValueError:
		return False

def getStringLen(val):
	'''
	计算字符串长度, 一个中文算两个字符
	'''
	length = len(val)
	utf8_length = len(val.encode('utf-8'))
	return int((utf8_length - length)/2 + length)

def cls():
	'''
	用于清理终端的屏幕 (Win下测试过, Linux上没测试过)
	'''
	sysstr = platform.system()
	if (sysstr == 'Windows'):
		os.system('cls')
	else:
		os.system('clear')

def throwMessageAndExit(mes):
	'''
	抛出一个错误消息并终止脚本的运行
	'''
	print(mes)
	sys.exit(0)
	return

def getScriptDirectory():
	'''
	获取当前脚本所在的目录位置 (末尾自动补充斜杠)
	'''
	return os.path.split(os.path.realpath(__file__))[0] + os.sep

def getLeeClientDirectory():
	'''
	获取 LeeClient 的主目录 (末尾自动补充斜杠)
	'''
	scriptDir = getScriptDirectory()
	return os.path.abspath(scriptDir + '..') + os.sep

def verifyAgentLocation():
	'''
	用于验证此脚本是否处于正确的运行位置
	'''
	scriptDir = getScriptDirectory()
	leeClientDir = getLeeClientDirectory()
	verifyPassFlag = True
	
	# 检查脚本所在的目录中, 是否存在特定的平级目录
	verifyDirList = ['RagexeClient', 'TranslateData']
	for dir in verifyDirList:
		verifyPath = (os.path.abspath(scriptDir + dir) + os.sep)
		if False == (os.path.isdir(verifyPath) and os.path.exists(verifyPath)):
			verifyPassFlag = False
	
	# 检查脚本所在的上级目录中, 是否存在特定的文件
	verifyFileList = ['cps.dll', 'aossdk.dll']
	for file in verifyFileList:
		verifyPath = (os.path.abspath(leeClientDir + file))
		if False == (os.path.isfile(verifyPath) and os.path.exists(verifyPath)):
			verifyPassFlag = False
	
	# 任何一个不通过, 都认为脚本所处的位置不正确, 终止执行
	if False == verifyPassFlag:
		throwMessageAndExit('脚本所处的位置不正确, 验证失败')
	
	return

def getRagexeClientList(dir):
	'''
	根据指定的 dir 中枚举出子目录的名字
	这里的目录名称为 Ragexe 客户端版本号的日期
	
	返回: Array 保存着每个子目录名称的数组
	'''
	dirlist = []
	
	try:
		list = os.listdir(dir)
	except:
		print("getRagexeClientList Access Deny")
		return None
	
	for dname in list:
		dirlist.append(dname)
	
	return dirlist

def remove_file(path):
	'''
	能够忽略文件不存在错误的文件删除函数
	'''
	try:
		return os.remove(path)
	except FileNotFoundError:
		return None

def remove_tree(path):
	'''
	能够忽略目录不存在错误的目录删除函数
	'''
	try:
		return dir_util.remove_tree(path)
	except FileNotFoundError:
		return None

def buildResetInformation():
	'''
	构建重置时需要移除的文件和目录信息
	'''
	
	# 重置时将会被移除的目录
	resetDir = [
		'AI',
		'AI_sakray',
		'_tmpEmblem',
		'memo',
		'Replay',
		'savedata',
		'Navigationdata',
		'System',
		'data' + os.sep + 'luafiles514'
	]
	
	# 重置时将会被移除的文件
	resetFile = [
		'data' + os.sep + 'msgstringtable.txt',
		'data' + os.sep + 'clientinfo.xml'
	]
	
	# 确定要移除的 LeeClient 根目录 EXE 时, 避免被删除的文件名 (白名单)
	excludeFile = [
		'setup.exe'
	]

	resetInfo = []
	leeClientDir = getLeeClientDirectory()
	
	for dir in resetDir:
		path = os.path.abspath(leeClientDir + dir) + os.sep
		resetInfo.append([0, path])
	
	for file in resetFile:
		path = os.path.abspath(leeClientDir + file)
		resetInfo.append([1, path])
	
	for item in os.listdir(leeClientDir):
		path = os.path.join(leeClientDir, item)
		if not os.path.isfile(path):
			continue
		if not item.lower().endswith('exe'):
			continue
		if not (item.lower() in excludeFile):
			resetInfo.append([1, path])
	
	return resetInfo

def getResetInfomationLines(resetInfo):
	'''
	将重置时需要移除的文件和目录信息转换成文本数组
	用于在必要的时候输出到终端
	'''
	lines = []
	leeClientDir = getLeeClientDirectory()
	for info in resetInfo:
		line = ('%s - LeeClient\\%s' % (('目录' if info[0] == 0 else '文件'), os.path.relpath(info[1], leeClientDir)))
		lines.append(line)
	return lines

def resetWorkshop():
	'''
	重置 LeeClient 客户端环境
	为接下来切换其他版本的客户端做好准备
	'''
	try:
		resetInfo = buildResetInformation()
		for info in resetInfo:
			if info[0] == 0:		# 目录
				remove_tree(info[1])
			elif info[0] == 1:		# 文件
				remove_file(info[1])
		
		print('已成功重置 LeeClient 客户端环境')
		return
		
	except:
		print('很抱歉, 重置 LeeClient 客户端环境的过程中发生了意外, 请检查结果')
		return

def switchWorkshop(clientver):
	'''
	切换 LeeClient 到指定的客户端版本
	'''
	scriptDir = getScriptDirectory()
	leeClientDir = getLeeClientDirectory()
	clientList = getRagexeClientList(os.path.abspath(scriptDir + 'RagexeClient') + os.sep)
	
	if not clientver in clientList:
		throwMessageAndExit('您期望切换的版本号 %s 是无效的' % clientver)
	
	# 确认对应的资源目录在是存在的
	sourceDir = os.path.abspath(scriptDir + 'RagexeClient' + os.sep + clientver + os.sep + 'Basic') + os.sep
	if not (os.path.exists(sourceDir) and os.path.isdir(sourceDir)):
		throwMessageAndExit('无法找到 %s 版本对应的资源目录: %s' % (clientver, sourceDir))
	
	# 重置一下工作区
	resetInfo = buildResetInformation()
	resetLines = getResetInfomationLines(resetInfo)
	
	lines = [
		'在切换版本之前, 需要将 LeeClient 客户端恢复到干净状态',
		'请将自己添加的额外重要文件移出 LeeClient 目录, 避免被程序误删'
		'',
		'以下为本次重置将会删除的目录和文件, 请仔细确认: ',
		''
	]
	lines.extend(resetLines)
	
	title = '切换主程序版本到 %s' % clientver
	prompt = '是否执行重置操作, 删除上述的目录和文件并切换版本?'
	
	simpleConfirm(lines, title, prompt, 'resetWorkshop()')
	
	# 将对应的资源覆盖到 LeeClient 主目录
	try:
		print('正在切换版本, 请耐心等待...')
		dir_util.copy_tree(sourceDir, leeClientDir)
		print('已切换仙境传说的主程序到 %s 版本' % clientver)
	except:
		print('很抱歉, 切换仙境传说的主程序到 %s 版本的时发生错误, 请检查结果' % clientver)
	
def menuResetWorkshop():
	'''
	菜单处理函数
	当选择“重置 LeeClient 客户端到干净状态”时执行
	'''
	cls()
	
	resetInfo = buildResetInformation()
	resetLines = getResetInfomationLines(resetInfo)
	
	lines = [
		'此操作可以将 LeeClient 客户端恢复到干净状态',
		'请将自己添加的额外重要文件移出 LeeClient 目录, 避免被程序误删',
		'',
		'以下为本次重置将会删除的目录和文件, 请仔细确认: ',
		''
	]
	lines.extend(resetLines)
	
	title = '重置 LeeClient 客户端到干净状态'
	prompt = '是否立刻执行重置操作, 并删除上述的目录和文件?'
	
	simpleConfirm(lines, title, prompt, 'resetWorkshop()')
	
	return

def menuSwitchWorkshop():
	'''
	菜单处理函数
	当选择“切换仙境传说主程序的版本”时执行
	'''
	cls()
	
	scriptDir = getScriptDirectory()
	clientList = getRagexeClientList(os.path.abspath(scriptDir + 'RagexeClient') + os.sep)
	
	menus = []
	for client in clientList:
		menuItem = [client, 'switchWorkshop(\'%s\')' % client]
		menus.append(menuItem)
	
	simpleMenu(menus, '切换仙境传说主程序的版本', '请选择你想切换到的版本')
	
	return
	
def menuEnd():
	'''
	菜单处理函数
	当选择“退出程序”时执行
	'''
	throwMessageAndExit('感谢您的使用, 再见')
	return
	
def simpleConfirm(lines, title, prompt, evalcmd):
	'''
	简易的确认对话框
	'''
	cls()
	if not title is None:
		titleFmt = '= %s%-' + str(60 - getStringLen(title)) + 's ='
		print('================================================================')
		print(titleFmt % (title, ''))
		print('================================================================')
	
	for line in lines:
		print(line)
	
	print('')
	user_select = input(prompt + ' [Y/N]: ')
	print('————————————————————————————————')
	
	if user_select in ('N', 'n'):
		menuEnd()
	elif user_select in ('Y', 'y'):
		eval(evalcmd)
	else:
		throwMessageAndExit('请填写 Y 或者 N 之后回车确认, 请不要输入其他字符')
	
	return

def simpleMenu(items, title, prompt):
	'''
	简易的选择菜单
	'''
	cls()
	if not title is None:
		titleFmt = '= %s%-' + str(60 - getStringLen(title)) + 's ='
		print('================================================================')
		print(titleFmt % (title, ''))
		print('================================================================')
	
	index = 0
	for item in items:
		print('%d - %s' % (index, item[0]))
		index = index + 1
	print('')
	user_select = input('%s (%d - %d): ' % (prompt, 0, len(items) - 1))
	print('————————————————————————————————')
	
	if (False == atoi(user_select) and user_select != '0'):
		throwMessageAndExit('请填写正确的菜单编号(纯数字), 不要填写其他字符')
		
	user_select = atoi(user_select)
	
	if not (items[user_select][1] is None):
		eval(items[user_select][1])
	
	return atoi(user_select)
	
	
def main():
	'''
	此脚本的主入口函数
	'''
	# 验证此脚本所处的位置
	verifyAgentLocation()
	
	# 获取支持的客户端版本列表
	RagexeClientList = getRagexeClientList("./RagexeClient")
	if RagexeClientList is None:
		throwMessageAndExit("很抱歉, 无法获取客户端版本列表, 程序终止")
	
	# 选择操作
	menus = [
		['切换仙境传说主程序的版本', 'menuSwitchWorkshop()'],
		['重置 LeeClient 客户端到干净状态', 'menuResetWorkshop()'],
		['退出程序', 'menuEnd()']
	]
	
	title = 'LeeClient 控制台'
	prompt = '请填写想要执行的任务的菜单编号'
	
	simpleMenu(menus, title, prompt)
	
if __name__ == "__main__":
	main()
