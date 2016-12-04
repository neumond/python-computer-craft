from setuptools import setup
from sys import argv


def is_register_command(a):
    for item in a:
        if item.startswith('-'):
            continue
        return item in ('register', 'bdist_wheel')
    return False

longdesc = None
if is_register_command(argv[1:]):
    import os
    with os.popen('pandoc -f markdown_github -t rst README.md') as f:
        longdesc = f.read()


setup(
    name='computercraft',
    version='0.1.1',
    description='Pythonization of ComputerCraft Minecraft mod. Write Python instead Lua!',
    long_description=longdesc,
    url='https://github.com/neumond/python-computer-craft',
    author='Vitalik Verhovodov',
    author_email='knifeslaughter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
    ],
    keywords='computercraft minecraft',
    packages=['computercraft', 'computercraft.subapis'],
    package_data={'computercraft': ['back.lua']},
    install_requires=['aiohttp'],
    entry_points={
        'console_scripts': ['computercraft = computercraft.server:main'],
    },
)
