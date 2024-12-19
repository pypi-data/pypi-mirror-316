from setuptools import setup, find_packages

setup(
    name='Babaji',
    version='0.1',
    author='Nachiket Shinde',
    author_email='nachiketshinde@gmail.com',
    description='A package for predicting height from weight using a scaler and regression model.',
    long_description='Predict height for a given weight using a pre-trained scaler and regression model.',
    url='https://github.com/Nachiket858',  # Replace with your GitHub repo link
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
