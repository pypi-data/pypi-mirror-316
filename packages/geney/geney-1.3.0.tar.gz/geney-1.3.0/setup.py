import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='geney',
    version='1.3.0',
    python_requires='>3.9',
    description='A Python package for gene expression modeling.',
    url='https://github.com/nicolaslynn/geney',
    author='Nicolas Lynn',
    author_email='nicolasalynn@gmail.com',
    license='Free for non-commercial use',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.9',
    ],
)



