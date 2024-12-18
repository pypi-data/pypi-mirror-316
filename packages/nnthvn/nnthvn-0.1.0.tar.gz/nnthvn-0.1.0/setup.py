from setuptools import setup, find_packages

setup(
    name='nnthvn',  # Название библиотеки
    version='0.1.0',
    author='',
    author_email='jaguar80605@gmail.ru',
    description='Простая библиотека для работы с числами и строками.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NeonitTHeav3n/nnthvn',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
