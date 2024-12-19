from setuptools import setup, find_packages
setup(
    name='dischub',
    version='1.5',
    packages=find_packages(),
    install_requires=['requests'],
    description='A Django SDK to initiate online payment to the Dischub API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/stanleychihz/my_sdk',
    author='Stanford Chihoyi',
    author_email='chihoyistanford@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

