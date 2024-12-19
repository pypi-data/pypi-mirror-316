from setuptools import setup, find_packages

setup(
    name='saiCxDataFrameloader',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2"
        ,"plotly==5.22.0"
    ],
    author='Amit Gupta',
    author_email='amit.gupta@securiti.ai',
    license='MIT',
    description='A package for loading data frames for cx data files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amitgupta7/base-saiCxDataFrameloader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

