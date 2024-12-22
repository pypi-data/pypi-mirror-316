from setuptools import setup, find_packages

setup(
    name='luciusassistant',
    version=open("version.txt").read(),
    author='Matthew Sanchez',
    author_email='',
    description='An agentic AI assistant built on top of the Llama language model, designed to provide intelligent assistance through a robust function calling system. It offers seamless integration of chat capabilities with file operations and memory management.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        "": ["**/*"],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'chatollama'
    ],
)
