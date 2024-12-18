from setuptools import setup, find_packages

setup(
    name='robot_plugin',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author='NightMing',
    author_email='961880295@qq.com',
    description='机器人插件依赖包'
)
