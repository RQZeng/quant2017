### from ** import

## 同目录
.
|-- mod1.py
|-- mod2.py
`-- main.py
* 则main.py里面想要使用,则import mod1可以使用mod1

## 不同目录
`-- dir1
|	|-- __init__.py
|	|-- mod11.py
|	`-- mod12.py
`-- dir2
|	|-- __init__.py
|	|-- mod21.py
|	`-- mod22.py
`-- main.py

* 则若是main.py想要使用mod11,则需要
	* 先touch dir1/__init__.py
	* 在append目标目录的父目录,再import
	import sys
	sys.path.append('..')
	from dir1 import mod11
