from setuptools import setup, find_packages

setup(
    name='py-crave-sync',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'py-crave-sync = py_crave_sync.server:app.run',
        ],
    },
)
