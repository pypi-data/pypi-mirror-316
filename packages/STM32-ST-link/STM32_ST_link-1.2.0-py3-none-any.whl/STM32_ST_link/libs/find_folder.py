#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/20 上午11:29
# @Author  : 周梦泽
# @File    : find_folder.py
# @Software: PyCharm
# @Description:查找文件夹


import os


def find_folder(base_path, target_prefix):
    found_folders = []

    # 遍历FileRepository目录
    for folder in os.listdir(base_path):
        # 检查文件夹名是否以目标前缀开始
        if folder.lower().startswith(target_prefix.lower()):
            full_path = os.path.join(base_path, folder)
            if os.path.isdir(full_path):  # 确认是文件夹
                found_folders.append({
                    "folder_name": folder,
                    "full_path": full_path
                })
    return found_folders


if __name__ == '__main__':

    # 执行搜索
    results = find_folder()

    if results:
        print(f"找到 {len(results)} 个匹配的驱动文件夹：")
        for item in results:
            print(f"\n文件夹名: {item['folder_name']}")
            print(f"完整路径: {item['full_path']}")
    else:
        print("未找到匹配的驱动文件夹")
