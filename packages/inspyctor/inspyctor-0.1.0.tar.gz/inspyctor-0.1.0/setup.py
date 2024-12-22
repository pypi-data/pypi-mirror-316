from setuptools import setup, find_packages

setup(
    name='inspyctor',  # Replace with your package name
    version='0.1.0',  # Increment this version for each release
    packages=find_packages(),
    install_requires=[
        'flake8',  # Example dependency, add your dependencies here
        'bandit',
        'huggingface-hub',  # or any other dependencies your package needs
    ],
    description='Your intelligent Python code reviewer and analyzer.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your-email@example.com',
    url='https://github.com/yourusername/inspyctor',  # Link to your GitHub repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
