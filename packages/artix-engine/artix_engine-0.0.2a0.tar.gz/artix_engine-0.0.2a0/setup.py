from setuptools import setup, find_packages

setup(
    name="artix_engine",
    version="0.0.2-alpha",
    description="Хочете спробувати себе у створенні бота у діскорд? Давай з Artix",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="harttman",
    author_email="dakiv.work.vitaliy@example.com",
    url="https://github.com/harttman/artix_engine",
    packages=find_packages(),
    install_requires=[
        "websocket-client>=1.5.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
