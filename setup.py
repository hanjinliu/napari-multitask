from setuptools import setup, find_packages

with open("napari_multitask/__init__.py", encoding="utf-8") as f:
    line = next(iter(f))
    VERSION = line.strip().split()[-1][1:-1]
      
with open("README.md", "r") as f:
    readme = f.read()
    
setup(
    name="napari-multitask",
    version=VERSION,
    description="Multitasking in napari",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Hanjin Liu",
    author_email="liuhanjin-sc@g.ecc.u-tokyo.ac.jp",
    license="BSD 3-Clause",
    download_url="https://github.com/hanjinliu/napari-multitask",
    packages=find_packages(),
    install_requires=[
          "magic-class>=0.5.11"
    ],
    classifiers=["Framework :: napari",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 ],
    python_requires=">=3.7",
    )