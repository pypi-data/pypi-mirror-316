from setuptools import setup, find_packages

setup(
    name='sphinx-each-pdf',  # Название пакета
    version='1.0.0',  # Версия пакета
    author='NeleGALL',  # Ваше имя или команда
    author_email='ru@burubu.ru',  # Ваш email
    description='Tool for converting HTML files to PDF using Sphinx and Playwright.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NeleGALL/each-pdf',  # Ссылка на репозиторий
    packages=find_packages(),  # Поиск всех модулей в проекте
    install_requires=[
        'playwright>=1.0.0',  # Зависимости
    ],
    python_requires='>=3.8',  # Минимальная версия Python
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'each-pdf=each_pdf:main',  # Консольная команда для запуска
        ],
    },
    include_package_data=True,  # Включить дополнительные файлы (например, CSS)
)