from setuptools import setup

setup(
    name='pyesoify',
    version='0.1',
    author='Tathya Garg',
    author_email='coding.tathya+gh@gmail.com',
    url='https://github.com/tathyagarg/pyeosify',
    description='A simple Python package to convert Python code to a much, much, much less readable form.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'pyesoify=pyesoify.pyesoify:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
