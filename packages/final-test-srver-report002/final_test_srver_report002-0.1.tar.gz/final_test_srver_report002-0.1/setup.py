from setuptools import setup, find_packages

setup(
    name='final_test_srver_report002',               # Name of the package
    version='0.1',                         # Version number
    author='Your Name',
    author_email='your.email@example.com',
    description='A monitoring system with an agent and a server.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),                # Finds all subpackages automatically
    include_package_data=True,               # Includes files specified in MANIFEST.in
    install_requires=[
        # List your dependencies here
        'flask',  # Example dependency
        'psutil'
    ],
    package_data={
        'my_package': ['config.conf'],  # Include the config file in the package
    },
    entry_points={
        'console_scripts': [
            'ruuuuuun.py=monitoring_system_report6.ruuuuuun.py:main',  # New command to run all
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
