# -*- coding: utf-8 -*-
import os

# 指定目录
dir_path = 'F:\\botsForPublish'

# 遍历目录
for root, dirs, files in os.walk(dir_path):
    for file in files:
        # 判断文件类型，仅处理 Python 文件
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            # 打开文件，读取内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 判断文件头部是否已经有编码声明，没有则添加
            if not content.startswith('# -*- coding:'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('# -*- coding: utf-8 -*-\n' + content)
            # 已经有编码声明，更新为 utf-8
            elif 'utf-8' not in content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content.replace('coding:', 'coding: utf-8'))