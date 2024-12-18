from datetime import date
from setuptools import setup, find_packages

# VERSION = date.today().strftime("%Y.%m.%d")[2:]  # 以当天的日期作为版本号
VERSION = "0.1.0"

setup(
    name="qfree",  # 模块名称
    version=VERSION,
    author="leesp",  # 作者
    author_email="leesp8@yeah.net",  # 作者邮箱
    description="Quantitative Trading Toolkit",  # 模块描述
    long_description=open("README.md").read(),  # 长描述
    long_description_content_type="text/markdown",  # 长描述的格式
    packages=find_packages(),  # 自动发现所有包
    install_requires=["empyrical"],  # 依赖项
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
)
