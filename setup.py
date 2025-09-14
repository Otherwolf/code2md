from setuptools import setup, find_packages

setup(
    name="code2md",
    version="1.0.0",
    description="Сбор структуры проекта и содержимого файлов в Markdown",
    author="vpe304@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'code2md=code2md.main:main',
        ],
    },
)
