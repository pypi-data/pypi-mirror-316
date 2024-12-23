from setuptools import setup, find_packages
setup(
    name = "whlee",
    version = "0.0.1",
    description="toy tools",
    author = "whl",
    author_email = "2631@139.com",
    license="MIT",
    packages = find_packages(),
    python_requires=">=3.6",
    install_requires=['numpy==1.24.3', 'pandas>=1.3.5', 'addict']
)
