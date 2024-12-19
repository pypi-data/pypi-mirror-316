from setuptools import setup, find_packages

setup(
    name='markitdown-document-processor',
    version='1.3',
    packages=find_packages(),
    install_requires=['markitdown'],
    entry_points={
        'console_scripts': [
            'document_processor=document_processor.main:main',
        ],
    },
    author='Eduardo Brigham',
    author_email='edubrigham@gmail.com',
    description='A document processor that converts documents to Markdown using Microsoft markitdown package',
    long_description=open('../README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/edubrigham/markitdown-document-processor',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)