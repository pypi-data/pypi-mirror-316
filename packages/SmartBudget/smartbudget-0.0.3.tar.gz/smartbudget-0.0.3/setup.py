from setuptools import setup, find_packages

setup(
    name="SmartBudget",
    version='0.0.3',
    author='',
    author_email='1sergeiivanov1@mail.ru',
    description='Бибилиотека для удобного управления финансами, анализом расходов и бюджетированием',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)


