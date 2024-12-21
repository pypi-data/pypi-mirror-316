from setuptools import setup, find_packages

setup(
    name='Babaji',
    version='0.4',
    author='Nachiket Shinde',
    author_email='nachiketshinde@gmail.com',
    description='A package in which various of Pretrain models are implemented.',
    long_description='this package is help to make a ml projects for the dtudent who .',
    url='https://github.com/PyBabaji',  # Replace with your GitHub repo link
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
