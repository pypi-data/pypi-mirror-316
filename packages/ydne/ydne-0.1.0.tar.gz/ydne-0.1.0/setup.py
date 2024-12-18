from setuptools import setup, find_packages

setup(
    name='ydne',
    version='0.1.0',
    author='Nugroho Satrijandi',
    author_email='satrijandi@gmail.com',
    description='A collection of data utilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/satrijandi24/ydne',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.11',
)