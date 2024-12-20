'''
Author: LYG liaoyanguo
Date: 2024-12-20 15:34:01
LastEditors: LYG liaoyanguo
LastEditTime: 2024-12-20 17:30:37
Email: liaoyanguo@foxmail.com
Description: 
FilePath: /practice/python/setup/setup.py
'''
from setuptools import setup, find_packages

setup(
    name='yg_project_demo',
    version='0.3',
    packages=find_packages(),
    package_data={
        'yg_project_demo': ['./demo2.py'],
    },
    install_requires=[
        # 列出你的项目依赖的其他包
    ],
)