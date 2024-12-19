from setuptools import setup, find_packages

setup(
    name='yhd_acquisition',
    version='1.0',
    packages=find_packages(),
    description='interface',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='08479',
    license='MIT',  # 或其他许可证
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
