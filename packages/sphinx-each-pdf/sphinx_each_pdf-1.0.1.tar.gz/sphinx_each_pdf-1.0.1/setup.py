from setuptools import setup, find_packages

setup(
    name="sphinx-each-pdf",  # Название пакета на PyPI
    version="1.0.1",  # Версия пакета
    author="NeleGALL",  # Имя автора
    author_email="ru@burubu.ru",  # Email автора
    description="Tool for converting HTML files to PDFs using Sphinx and Playwright.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NeleGALL/each-pdf",  # Ссылка на репозиторий
    packages=find_packages(),  # Автоматическое обнаружение пакетов
    install_requires=[
        "playwright>=1.0.1",  # Зависимости
    ],
    python_requires=">=3.8",  # Минимальная версия Python
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Включение дополнительных файлов (например, CSS)
)
