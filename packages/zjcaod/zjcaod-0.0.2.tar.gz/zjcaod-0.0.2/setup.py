import time

import setuptools
import re
import requests
from bs4 import BeautifulSoup

package_name = "zjcaod"


def curr_version():
    # 从官网获取版本号
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url, timeout=60)
    time.sleep(5)
    soup = BeautifulSoup(response.text, "html.parser")
    latest_version = soup.select_one(".release__version").text.strip()
    return str(latest_version)


def get_version():
    # 从版本号字符串中提取三个数字并将它们转换为整数类型
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", curr_version())
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))

    # 对三个数字进行加一操作
    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    new_version_str = f"{major}.{minor}.{patch}"
    return new_version_str


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zjcaod",
    version=get_version(),
    author="zjcaod",
    url='',
    author_email="1352514347@qq.com",
    description="zjcaod tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)