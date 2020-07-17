from pathlib import Path
from setuptools import setup


longdesc = (Path(__file__).parent / 'README.md').read_text()


setup(
    name='computercraft',
    version='0.3.0',
    description='Pythonization of ComputerCraft Minecraft mod. Write Python instead Lua!',
    long_description=longdesc,
    long_description_content_type='text/markdown',
    url='https://github.com/neumond/python-computer-craft',
    author='Vitalik Verhovodov',
    author_email='knifeslaughter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Games/Entertainment',
    ],
    keywords='computercraft minecraft',
    packages=['computercraft', 'computercraft.subapis'],
    package_data={'computercraft': ['back.lua']},
    install_requires=['aiohttp', 'greenlet'],
    entry_points={
        'console_scripts': ['computercraft = computercraft.server:main'],
    },
)
