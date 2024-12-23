from setuptools import setup, find_namespace_packages

setup(
    name='gamerl',
    version='0.1.0',
    description='Collection of RL algorithms in the gamerl namespace.',
    packages=find_namespace_packages(
        include=['gamerl.*'],
    ),
    author='pi-tau',
    url='https://github.com/game-rl/gamerl',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
