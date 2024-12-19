from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zhiwowo",  # 包名，PyPI上将显示的名称
    version="0.0.4",            # 版本号
    author="wowohr#middleend",  # 作者信息
    description="人力窝-智窝助手sdk",  # 简要描述
    long_description=long_description,  # 详细描述（从 README.md 中读取）
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
