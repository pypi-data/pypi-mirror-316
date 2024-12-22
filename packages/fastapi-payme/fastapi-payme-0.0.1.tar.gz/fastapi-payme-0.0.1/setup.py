from setuptools import setup, find_packages


setup(
    name="fastapi-payme",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
    ],
    author="Karimov Murodilla",
    author_email="karimovmurodilla15@gmail.com",
    description="A FastAPI library for Payme integration",
    url="https://github.com/KarimovMurodilla/fastapi-payme.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)