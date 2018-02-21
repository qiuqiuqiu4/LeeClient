# LeeClient 仙境传说完整客户端

为 [rAthenaCN](http://rathena.cn/) / [Hercules](https://github.com/HerculesWS/Hercules) 等模拟器整理的仙境传说完整客户端, 
设计愿景为整合官方全球各服的所有图档资源, 并方便 GM 在不同版本客户端之间进行切换测试. 此客户端主要面向的用户是各位GM而不是游戏玩家.
在将它提供给玩家使用之前, 还需要各位 GM 对内容进行相应的调整, 包括资源汉化、将 data 目录打包等操作.

## 内容汉化暂不完善

目前 LeeClient 只保证程序运行无报错, 无异常. 基本没有做过多的汉化, 而且目前也没有在汉化上投入精力.
所以还需要请各位 GM 根据自己的要求和品位, 各显神通来进行汉化. 未来 LeeClient 会提供较为自动化或完善的汉化功能, 尽请期待.

## 推荐使用的下载方式

建议通过克隆的方式将 LeeClient 项目同步到电脑中, 这样将包含 Git 的仓库信息, 
使未来更新 LeeClient 更加方便, 虽然第一次同步非常慢但是以后更新只需要同步少量文件, 非常值得. 

建议不要选择直接点击 Github 项目主页的 Download 按钮来下载, 因为这样下载的文件虽然较小, 
但也由于没有包含 Git 的仓库信息, 导致未来想更新 LeeClient 的话需要重新下载一次, 长远来说更不划算.

> 接下来会在百度网盘中提供带仓库信息的 LeeClient 仓库压缩包, 方便国内用户更快的进行下载. 
> 只需要在下载完成后用 Git / TortoiseGit 进行一次更新, 即可获得 LeeClient 的最新版本.

## 克隆仓库后请更新子模块

当你使用克隆的方式将 LeeClient 同步到电脑中之后, 请初始化(Init)并更新(Update)一下子模块(Submodule). LeeClient 使用子模块(Submodule)来同步一些第三方的项目(比如我们用于DIFF客户端的NEMO等).

- 若使用 TortoiseGit 来操作 Git 的话, 请在 LeeClient 目录中使用 TortoiseGit 的右键菜单, 选择"更新子模块"菜单项(英文菜单项名为“Submodule Update..”), 然后按照默认选项直接点击确定即可.

- 若使用命令行方式直接操作 Git 的话, 请在 LeeClient 目录下先执行 `git submodule init` 再执行 `git submodule update` 即可

## 需要的磁盘空间

由于需要对 data 目录中的所有文件进行版本跟踪, LeeClient 将整个 data.grf 解压了出来, 
这样虽然带来了版本跟踪的便利性, 但是同时也扩大了整个仓库的体积.

根据 2018-2-19 的统计, 克隆本仓库完整解压后需要大约 11 GB 的磁盘空间, 包含接近 10 万个文件, 1000 多个目录.

## 目前支持的客户端版本

您可以在 [Utility/RagexeClient](https://github.com/CairoLee/LeeClient/tree/master/Utility/RagexeClient) 目录中找到目前 LeeClient 支持的客户端版本, 
其中子目录的名称 (比如: 2015-11-04) 就是客户端版本号, 子目录中包含了所有该版本所需要的各种文件和档案.

注意: 请不要通过手动复制粘贴版本目录中的文件来切换 LeeClient 支持的版本, 建议通过 LeeClientAgent 辅助程序来完成版本切换工作, 具体方法请继续往下看.

## 安装 Python 解析器

为了提供更加便捷的客户端版本切换等功能, 我们用 Python 编写了一个比较便捷的辅助程序, 
名为 LeeClientAgent, 它位于 Utility 目录下. 您需要先安装 Python 3.6.4 或更新版本的 
Python 脚本解析器, 才能够成功运行它.

- 若您是 x64 操作系统, 请点此下载 [Windows x86-64 executable installer](https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe)
- 若您是 x86 操作系统, 请点此下载 [Windows x86 executable installer](https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe)

## 使用 LeeClientAgent 切换客户端版本

当您安装完成 Python 解析器之后, 就可以双击 Utility/LeeClientAgent.py 文件来运行辅助程序.
当您成功启动辅助程序时, 将看到以下几个选项可供选择:

> 0. 切换仙境传说主程序的版本
> 1. 重置 LeeClient 客户端到干净状态
> 2. 汉化各版本客户端的 msgstringtable.txt 文件
> 3. 退出程序

请填写数字 0 并回车, 随后将看到类似如下的版本选择菜单:

> 0. 2013-08-07
> 1. 2013-12-23
> 2. 2015-09-16
> 3. 2015-11-04
> 4. 2016-02-03
> 5. 2017-06-14

请填写你想切换到的目标版本对应的菜单编号, 回车确认后, 仔细阅读重置说明然后按 Y 回车确认, 即可完成版本的切换操作.
例如: 2016-02-03 对应的菜单编号是 4, 那么填写数字 4 之后回车, 并按 Y 回车进行确认, 就可以了.


