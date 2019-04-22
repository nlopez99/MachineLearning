from distutils.core import setup

setup(
    name='NHLRegressionModel',
    version='0.1dev',
    packages=['requests', 'bs4', 'pandas', 'numpy', 'scikit-learn', 'statsmodels'],
    license='MIT License',
    long_description=open('README.txt').read(),
)
