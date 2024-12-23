from setuptools import setup, find_packages

setup(
    name="artix_engine",
    version="0.0.4",
    description="Do you want to try your hand at creating a Discord bot? Let's do it with Artix!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="harttman",
    author_email="dakiv.work.vitaliy@example.com",
    url="https://github.com/harttman/artix_engine",
    packages=find_packages(),
    install_requires=[
        "websockets"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
