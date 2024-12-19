import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zhiwowo",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.0.2",  # 包版本号，便于维护版本,保证每次发布都是版本都是唯一的
    author="wowohr#middleend",  # 作者，可以写自己的姓名
    description="人力窝-智窝助手sdk",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where='core'),
    package_dir={'':'core'},
    python_requires='>=3.6',  # 对python的最低版本要求
    include_package_data=False
)