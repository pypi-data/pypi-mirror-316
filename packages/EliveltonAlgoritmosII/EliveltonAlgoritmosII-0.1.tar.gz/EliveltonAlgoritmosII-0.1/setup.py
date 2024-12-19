from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='EliveltonAlgoritmosII',
    version='0.1',
    author='Elivelton Bouteille',
    author_email='eliveltoncontact@gmail.com',
    description='Algoritmos de subarray máximo e multiplicação de Strassen',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/xxvelho/EliveltonAlgoritmosII',  # URL do repositório do GitHub
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',  # Dependência externa necessária
    ],
)
