from setuptools import setup, find_packages

setup(
    name='calculate_statistics',  # 包名
    version='1.0.0',
    packages=find_packages(), 
    install_requires=[
        'matplotlib',
        'numpy',
        'opencv-python',
    ],
)

