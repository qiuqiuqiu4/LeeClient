#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import copy
import distutils
import hashlib
import os
import platform
import sys
from distutils import dir_util

class LeeCommonLib:
	'''
	这个类用来存放一些通用的函数
	主要为了让后面代码的分类更加直观一些
	'''
	def atoi(self, val):
		'''
		用于将一个字符串尝试转换成 Int 数值
		转换成功则返回 Int 数值，失败则返回布尔类型的 False
		'''
		try:
			int(val)
			return int(val)
		except ValueError:
			return False
	
	def strDictItemExists(self, dictobj, key):
		'''
		判断字典指定的 key 是否存在
		如果存在, 那么判断它的值是否为空字符串, 任何一个不成立则返回 False
		'''
		if dictobj is None or key is None:
			return False
		if key not in dictobj:
			return False
		return not (dictobj[key] is None or len(dictobj[key]) <= 0)
	
	def md5(self, data):
		'''
		获得给定字符串的 MD5 哈希值
		'''
		m = hashlib.md5(data.encode(encoding='utf8'))
		return m.hexdigest()
	
	def getSpiltText(self, str, spiltchar, index):
		'''
		将字符串按照特定分隔符切割, 并取得指定位数的字符串
		'''
		fields = str.split(spiltchar)
		if len(fields) < index + 1:
			return None
		else:
			return fields[index]

	def getStringLen(self, val):
		'''
		计算字符串长度, 一个中文算两个字符
		'''
		length = len(val)
		utf8_length = len(val.encode('utf-8'))
		return int((utf8_length - length)/2 + length)

	def cleanScreen(self):
		'''
		用于清理终端的屏幕 (Win下测试过, Linux上没测试过)
		'''
		sysstr = platform.system()
		if (sysstr == 'Windows'):
			os.system('cls')
		else:
			os.system('clear')

	def remove_file(self, path):
		'''
		能够忽略文件不存在错误的文件删除函数
		'''
		try:
			return os.remove(path)
		except FileNotFoundError:
			return None

	def remove_tree(self, path):
		'''
		能够忽略目录不存在错误的目录删除函数
		'''
		try:
			return dir_util.remove_tree(path)
		except FileNotFoundError:
			return None

	def throwMessageAndExit(self, mes):
		'''
		抛出一个错误消息并终止脚本的运行
		'''
		print(mes)
		sys.exit(0)
		return

	def getScriptDirectory(self):
		'''
		获取当前脚本所在的目录位置 (末尾自动补充斜杠)
		'''
		return os.path.split(os.path.realpath(__file__))[0] + os.sep

	def getLeeClientDirectory(self):
		'''
		获取 LeeClient 的主目录 (末尾自动补充斜杠)
		'''
		scriptDir = self.getScriptDirectory()
		return os.path.abspath(scriptDir + '..') + os.sep
	
	def simpleConfirm(self, lines, title, prompt, evalcmd):
		'''
		简易的确认对话框
		'''
		commonlib.cleanScreen()
		if not title is None:
			titleFmt = '= %s%-' + str(60 - commonlib.getStringLen(title)) + 's ='
			print('================================================================')
			print(titleFmt % (title, ''))
			print('================================================================')
		
		for line in lines:
			print(line)
		
		print('')
		user_select = input(prompt + ' [Y/N]: ')
		print('----------------------------------------------------------------')
		
		if user_select in ('N', 'n'):
			mainMenu_End()
		elif user_select in ('Y', 'y'):
			eval(evalcmd)
		else:
			commonlib.throwMessageAndExit('请填写 Y 或者 N 之后回车确认, 请不要输入其他字符')
		
		return

	def simpleMenu(self, items, title, prompt):
		'''
		简易的选择菜单
		'''
		commonlib.cleanScreen()
		if not title is None:
			titleFmt = '= %s%-' + str(60 - commonlib.getStringLen(title)) + 's ='
			print('================================================================')
			print(titleFmt % (title, ''))
			print('================================================================')
		
		index = 0
		for item in items:
			print('%d - %s' % (index, item[0]))
			index = index + 1
		print('')
		user_select = input('%s (%d - %d): ' % (prompt, 0, len(items) - 1))
		print('----------------------------------------------------------------')
		
		if (False == commonlib.atoi(user_select) and user_select != '0'):
			commonlib.throwMessageAndExit('请填写正确的菜单编号(纯数字), 不要填写其他字符')
			
		user_select = commonlib.atoi(user_select)
		
		if not (items[user_select][1] is None):
			eval(items[user_select][1])
		
		return commonlib.atoi(user_select)

class TranslateMapDictItem:
	'''
	此类用于保存从翻译对照表中加载成功的内容
	'''
	def __init__(self, lineno = None, content = None, origin = None, target = None):
		'''
		类的初始化, 主要做赋值工作
		'''
		self.lineno = lineno	# 行号
		self.content = content	# 读取到的一整行信息
		self.origin = origin	# 原文
		self.target = target	# 译文
		return
	
	def __str__(self):
		return ('LineNo: %d\nContent: %s\nOrigin: %s\nTarget: %s\n' % (self.lineno, self.content, self.origin, self.target))

class SingleKeyReferItem:
	'''
	引用计数的记录类, 就是一个简单的计数器
	'''
	def __init__(self, origin = None):
		self.origin = origin
		self.referCount = 0
		return
	
	def incRefer(self):
		'''
		引用计数器自增1次
		'''
		self.referCount = self.referCount + 1
		return
	
	def __str__(self):
		return ('Origin: %s\nReferCount: %d\n' % (self.origin, self.referCount))
		
class LeeTransMsgStringTable:
	def __init__(self, mapsdir):
		self.dictTranslate = {}
		self.dictSingleTranslate = {}
		
		self.commonlib = LeeCommonLib()
		self.scriptDir = self.commonlib.getScriptDirectory()
		self.mapsdir = mapsdir
		return
	
	def execute(self, lang):
		'''
		对 RagexeClient 目录下的各个版本客户端的 msgstringtable.txt 执行汉化工作
		'''
		if not self.__loadTranslateDict(lang):
			self.commonlib.throwMessageAndExit('翻译映射表加载失败, 无法继续汉化')
		
		clientList = getRagexeClientList(os.path.abspath(self.scriptDir + 'RagexeClient') + os.sep)
		
		for clientver in clientList:
			msgstringtablePath = os.path.abspath(self.scriptDir + 'RagexeClient' + os.sep + clientver) + os.sep
			msgstringtablePath = os.path.abspath(msgstringtablePath + 'Basic' + os.sep + 'data') + os.sep
			
			try:
				msgstringtableData = self.__loadMsgStringTable(msgstringtablePath + 'msgstringtable_original.txt')
				self.__translate(msgstringtableData)
				self.__saveMsgStringTable(msgstringtableData, msgstringtablePath + 'msgstringtable.txt')
				print('已成功汉化 %s 客户端版本的 msgstringtable.txt !' % clientver)
			except Exception as e:
				print('对 %s 客户端版本的 msgstringtable.txt 汉化出现了错误: %s' % (clientver, e))
				continue
		
		print('----------------------------------------------------------------')
		print('完成汉化之后您需要切换一次客户端版本, 才能使修改生效. 请务必记得')
		print('备份一下自己添加或修改的文件, 避免在切换版本的过程中被误删.')
		
		return
	
	def __buildKey(self, obj, index, callback, attr):
		'''
		类私有函数, 用于建立一个与上下文对象关联的 Key
		主要用于将 A-1, A, A+1 自己前后的两个对象的 origin (在 attr 里面指定) 构建成一个 key
		'''
		identity = ''
		
		if index >= 1: identity = '%s|' % callback(obj[index - 1], attr)
		identity = '%s%s|' % (identity, callback(obj[index], attr))
		if index + 1 < len(obj): identity = '%s%s|' % (identity, callback(obj[index + 1], attr))
		identity = self.commonlib.md5(identity)
		
		return identity
	
	def __buildKey_callback_for_attribute(self, item, attr):
		'''
		类私有函数, 服务于 __buildKey 的回调
		直接使用 eval 函数返回给定 item 指定的属性名称的值
		'''
		return eval('item.' + attr)
	
	def __buildKey_callback_for_msgstringtable_list(self, item, attr):
		'''
		类私有函数, 服务于 __buildKey 的回调
		将给定的 item 字符串按 # 分割, 返回第一个元素
		'''
		return self.commonlib.getSpiltText(item, '#', 0)

	def __loadMsgStringTable(self, path):
		'''
		类私有函数, 读取指定路径的 msgstringtable.txt 并返回一个列表
		'''
		file = open(path, 'r', encoding='gb18030')
		msgstringtableData = file.readlines()
		file.close()
		
		# 去掉每行结尾的换行符
		for index in range(len(msgstringtableData)):
			line = msgstringtableData[index]
			msgstringtableData[index] = line.rstrip()
		
		return msgstringtableData
		
	def __loadTranslateDict(self, lang):
		'''
		类私有函数, 用来载入特定语言的翻译字典文件
		'''
		mappath = os.path.abspath(self.mapsdir + lang + '.txt')
		if not (os.path.exists(mappath) and os.path.isfile(mappath)):
			self.commonlib.throwMessageAndExit('翻译映射表不存在, 请检查: %s' % mappath)
		
		# 仅在加载字典时需要的一个列表
		# 里面存放的都是 TranslateMapDictItem 对象
		translateMap = []
		
		# 将字典文件载入到内存中
		file = open(mappath, 'r', encoding='gb18030')
		line = file.readline()
		lineNo = 1
		while line:
			line = line.rstrip()
			fields = line.split('#')
			origin = self.commonlib.getSpiltText(line, '#', 0)
			target = self.commonlib.getSpiltText(line, '#', 1)
			
			if (len(fields) < 2 or origin.startswith('//')):
				line = file.readline()
				continue
			
			item = TranslateMapDictItem(lineNo, line, origin, target)
			translateMap.append(item)
			# print(item)
			
			line = file.readline()
			lineNo = lineNo + 1
		file.close()
		
		# 根据读取到的数组内容 基于上下文的原文(origin) 构建字典
		# 并保存 A 的 target 值作为字典的 value
		self.dictTranslate.clear()
		
		for index in range(len(translateMap)):
			item = translateMap[index]
			origin_key = self.__buildKey(translateMap, index, self.__buildKey_callback_for_attribute, 'origin')
			
			if origin_key not in self.dictTranslate:
				self.dictTranslate[origin_key] = item.target
		
		# 创建以 origin 为 key 的引用计数表(字典)
		dictRefer = {}
		
		for item in translateMap:
			key = self.commonlib.md5(item.origin)
			
			if key in dictRefer:
				dictRefer[key].incRefer()
			else:
				referItem = SingleKeyReferItem(item.origin)
				referItem.incRefer()
				dictRefer[key] = referItem
		
		# 将引用计数为 1 的项目挑出来, 单独建立一个独立项字典
		self.dictSingleTranslate.clear()
		
		for item in translateMap:
			key = self.commonlib.md5(item.origin)
			
			if key in dictRefer and dictRefer[key].referCount == 1:
				self.dictSingleTranslate[key] = item.target
		
		return True
	
	def __translate(self, msgstringtableData):
		'''
		根据字典来翻译 msgstringtableData 列表对象中的内容
		'''
		# 浅拷贝 msgstringtableData 列表
		msgstringtableBackupData = copy.copy(msgstringtableData)
		
		# 根据上下文字典进行翻译
		for index in range(len(msgstringtableBackupData)):
			line = msgstringtableBackupData[index]
			origin_key = self.__buildKey(msgstringtableBackupData, index, self.__buildKey_callback_for_msgstringtable_list, None)
			
			if self.commonlib.strDictItemExists(self.dictTranslate, origin_key):
				msgstringtableData[index] = self.dictTranslate[origin_key] + '#'
		
		# 根据独立项字典进行翻译
		for index in range(len(msgstringtableData)):
			line = msgstringtableData[index]
			line = self.commonlib.getSpiltText(line, '#', 0)
			key = self.commonlib.md5(line)
			
			if self.commonlib.strDictItemExists(self.dictSingleTranslate, key):
				msgstringtableData[index] = self.dictSingleTranslate[key] + '#'
		
		return
	
	def __saveMsgStringTable(self, msgstringtableData, savepath):
		'''
		将 msgstringtableData 列表对象的内容保存到文件
		'''
		file = open(savepath, 'w+', newline='', encoding='gb18030')
		for index in range(len(msgstringtableData)):
			msgstringtableData[index] = msgstringtableData[index] + os.linesep
			try:
				file.write(msgstringtableData[index])
			except:
				print('Index %d | Error: %s' % (index, msgstringtableData[index]))
		file.close
		return


# ==============================================================================
# 以上为各种类的定义, 以下为未被封装为类的散户方法
# ==============================================================================

# 实体化公用库类
commonlib = LeeCommonLib()

def verifyAgentLocation():
	'''
	用于验证此脚本是否处于正确的运行位置
	'''
	scriptDir = commonlib.getScriptDirectory()
	leeClientDir = commonlib.getLeeClientDirectory()
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
		commonlib.throwMessageAndExit('脚本所处的位置不正确, 验证失败')
	
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
	
	dirlist.sort()

	return dirlist

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
	leeClientDir = commonlib.getLeeClientDirectory()
	
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
	leeClientDir = commonlib.getLeeClientDirectory()
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
				commonlib.remove_tree(info[1])
			elif info[0] == 1:		# 文件
				commonlib.remove_file(info[1])
		
		print('已成功重置 LeeClient 客户端环境')
		return
		
	except:
		print('很抱歉, 重置 LeeClient 客户端环境的过程中发生了意外, 请检查结果')
		return

def switchWorkshop(clientver):
	'''
	切换 LeeClient 到指定的客户端版本
	'''
	scriptDir = commonlib.getScriptDirectory()
	leeClientDir = commonlib.getLeeClientDirectory()
	clientList = getRagexeClientList(os.path.abspath(scriptDir + 'RagexeClient') + os.sep)
	
	if not clientver in clientList:
		commonlib.throwMessageAndExit('您期望切换的版本号 %s 是无效的' % clientver)
	
	# 确认对应的资源目录在是存在的
	sourceDir = os.path.abspath(scriptDir + 'RagexeClient' + os.sep + clientver + os.sep + 'Basic') + os.sep
	if not (os.path.exists(sourceDir) and os.path.isdir(sourceDir)):
		commonlib.throwMessageAndExit('无法找到 %s 版本对应的资源目录: %s' % (clientver, sourceDir))
	
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
	
	commonlib.simpleConfirm(lines, title, prompt, 'resetWorkshop()')
	
	# 将对应的资源覆盖到 LeeClient 主目录
	try:
		print('正在切换版本, 请耐心等待...')
		dir_util.copy_tree(sourceDir, leeClientDir)
		print('已切换仙境传说的主程序到 %s 版本' % clientver)
	except:
		print('很抱歉, 切换仙境传说的主程序到 %s 版本的时发生错误, 请检查结果' % clientver)
	
def mainMenu_ResetWorkshop():
	'''
	菜单处理函数
	当选择“重置 LeeClient 客户端到干净状态”时执行
	'''
	commonlib.cleanScreen()
	
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
	
	commonlib.simpleConfirm(lines, title, prompt, 'resetWorkshop()')
	
	return

def mainMenu_SwitchWorkshop():
	'''
	菜单处理函数
	当选择“切换仙境传说主程序的版本”时执行
	'''
	commonlib.cleanScreen()
	
	scriptDir = commonlib.getScriptDirectory()
	clientList = getRagexeClientList(os.path.abspath(scriptDir + 'RagexeClient') + os.sep)
	
	menus = []
	for client in clientList:
		menuItem = [client, 'switchWorkshop(\'%s\')' % client]
		menus.append(menuItem)
	
	commonlib.simpleMenu(menus, '切换仙境传说主程序的版本', '请选择你想切换到的版本')
	
	return

def mainMenu_TransMsgStringTable():
	'''
	菜单处理函数
	当选择“汉化各版本客户端的 msgstringtable.txt 文件”时执行
	'''
	scriptDir = commonlib.getScriptDirectory()
	msgStringTableMapsDir = os.path.abspath(scriptDir + 'TranslateData' + os.sep + 'msgstringtable') + os.sep
	
	transMsg = LeeTransMsgStringTable(msgStringTableMapsDir)
	transMsg.execute('zh-CN')
	return
	
def mainMenu_End():
	'''
	菜单处理函数
	当选择“退出程序”时执行
	'''
	commonlib.throwMessageAndExit('感谢您的使用, 再见')
	return
	
def main():
	'''
	此脚本的主入口函数
	'''
	# 验证此脚本所处的位置
	verifyAgentLocation()
	
	# 获取支持的客户端版本列表
	scriptDir = commonlib.getScriptDirectory()
	ragexeClientList = getRagexeClientList(scriptDir + 'RagexeClient')
	if ragexeClientList is None:
		commonlib.throwMessageAndExit("很抱歉, 无法获取客户端版本列表, 程序终止")
	
	# 选择操作
	menus = [
		['切换仙境传说主程序的版本', 'mainMenu_SwitchWorkshop()'],
		['重置 LeeClient 客户端到干净状态', 'mainMenu_ResetWorkshop()'],
		['汉化各版本客户端的 msgstringtable.txt 文件', 'mainMenu_TransMsgStringTable()'],
		['退出程序', 'mainMenu_End()']
	]
	
	title = 'LeeClient 控制台'
	prompt = '请填写想要执行的任务的菜单编号'
	
	commonlib.simpleMenu(menus, title, prompt)
	
if __name__ == "__main__":
	main()
