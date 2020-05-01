import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="app-status",
    version="0.0.1",
    author="Axel Catoire",
    author_email="axel.catoire@gmail.com",
    description="A simple way to monitor your running application in real time, on your phone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acatoire/app_status",
    packages=setuptools.find_packages(),
    install_requires=[
          'blynklib',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
