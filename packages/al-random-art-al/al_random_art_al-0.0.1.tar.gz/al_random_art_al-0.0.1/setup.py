from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="al-random-art-al",
    version="0.0.1",
    description="Инструменты для генерации случайных художественных элементов.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alina&Alyona",
    author_email="alinasusenko3@gmail.com",
    url="https://github.com/your-repo/text-game-engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
