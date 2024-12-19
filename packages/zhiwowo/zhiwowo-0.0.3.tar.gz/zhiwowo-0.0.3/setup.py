import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zhiwowo",  # 包名称
    version="0.0.3",  # 版本号
    author="wowohr#middleend",  # 作者信息
    description="人力窝-智窝助手sdk",  # 简要描述
    long_description=long_description,  # 详细描述（从 README.md 中读取）
    long_description_content_type="text/markdown",  # 描述内容类型
    packages=["core"],  # 指定需要打包的模块为 core
    package_dir={"core": "core"},  # 告诉 setuptools core 对应的路径
    python_requires=">=3.6",  # Python 版本要求
    include_package_data=False,  # 包括额外文件（如果有）
)
