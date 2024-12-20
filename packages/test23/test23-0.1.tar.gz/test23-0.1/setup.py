import os
import shutil
from setuptools import setup, Command, find_packages

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith(('.pyc', '.pyo', '.pyd')):
                    filepath = os.path.join(dirpath, filename)
                    print(f'Removing file: {filepath}')
                    os.remove(filepath)
            for dirname in dirnames:
                if dirname in ['__pycache__', 'build', 'dist', '*.egg-info']:
                    dir_to_remove = os.path.join(dirpath, dirname)
                    print(f'Removing directory: {dir_to_remove}')
                    shutil.rmtree(dir_to_remove)


setup(
    name="test23",
    version="0.1",
    packages=find_packages(),
    install_requires=[
    ],
    author="lpz",
    author_email="yywfqq@live.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'clean': CleanCommand,
    }
)
