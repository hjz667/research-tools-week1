# research-tools-week1

数据安全实验1，基础工具使用实验仓库。



\- code：存放 Python 实验程序。

\- result：存放程序运行结果与结果说明。

\- report：存放实验报告相关文件。



程序功能

code/demo.py 用于计算从 1 到 10 的整数之和。



运行方法

在仓库根目录打开 PowerShell，执行：

py code/demo.py



预期结果

The sum from 1 to 10 is: 55


已在 GitHub 网页更新本说明，用于练习 git pull。

## 文本词频统计

入口文件：`code/word_count.py`。需要 Python 3，仅使用标准库，无需安装第三方依赖。原求和程序 `code/demo.py` 仍可独立运行。

统计规则：

- 读取 UTF-8 文本，也支持带 BOM 的 UTF-8 文件。
- 忽略英文大小写；标点、数字、下划线和空白作为分隔符，不计入词频。
- 按连续 Unicode 字母（包括汉字）统计；中文不做自动分词，例如 `数据安全` 算一个词，`数据 安全` 算两个词。英文缩写和连字符也会被拆开，例如 `don't` 分成 `don` 和 `t`。
- 按次数降序输出，次数相同时按词语的 Unicode 字典序升序输出。
- 显示总词数和不同词数；空文件正常结束，读取失败则提示错误并返回退出码 1。
- 结果只显示在终端，不会自动写入 `result/run.txt`。

### 运行与手工测试

在项目根目录打开 PowerShell，运行自带样例：

```powershell
py -B code/word_count.py code/sample.txt
```

预期输出（列之间为制表符）：

```text
总词数：10
不同词数：7
词语	次数
hello	3
python	2
data	1
is	1
security	1
useful	1
world	1
```

统计自己的 UTF-8 文件时，将最后一个参数替换成文件路径；含空格的路径需加双引号：

```powershell
py -B code/word_count.py "D:\my text.txt"
```

可用记事本准备以下内容，对照检查：

| 测试内容 | 预期结果 |
| --- | --- |
| `Apple apple APPLE` | `apple` 出现 3 次 |
| `cat, dog! cat.` | `cat` 2 次，`dog` 1 次 |
| `zebra apple` | 都出现 1 次，`apple` 排在前面 |
| `数据 安全，数据` | `数据` 2 次，`安全` 1 次 |
| 空文件或仅含 `123 !?` | 总词数和不同词数均为 0 |
| 传入不存在的文件路径 | 显示读取错误，退出码为 1 |

### 自动测试

在项目根目录执行：

```powershell
py -B -m unittest discover -s code -p "test_*.py" -v
```

测试文件为 `code/test_word_count.py`，包含 9 项测试，覆盖大小写、标点、空白、空输入、数字、中文片段、排序、文件读取、UTF-8 BOM、含空格及中文路径、文件不存在和编码错误。测试会在系统临时目录创建输入文件，并在完成后自动清理。

通过时末尾显示 `Ran 9 tests` 和 `OK`。`-B` 用于避免生成字节码缓存文件。
