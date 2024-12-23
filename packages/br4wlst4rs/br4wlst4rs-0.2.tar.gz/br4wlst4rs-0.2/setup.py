from setuptools import setup, find_packages

setup(
    name="br4wlst4rs",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        'frida',
        'pynput',
        'requests'
    ],
    author="slayy2357",
    author_email="slayy2357pro@gmail.com",
    description="Brawl Stars more open source for ios",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/slayy2357/br4wlst4rs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={
        'br4wlst4rs': [
            'config/config.json',
            'js/*.js',
        ],
    },
    include_package_data=True
)