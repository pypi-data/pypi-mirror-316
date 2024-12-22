from setuptools import setup, find_packages

setup(
    name='py-crave-sync',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'py-crave-sync = py_crave_sync.server:app.run',
        ],
    },
    author='Julox Games',  # Replace with your name or organization
    description='A lightweight Python package that creates a local live server for syncing and serving data.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',  # Minimum Python version
)
