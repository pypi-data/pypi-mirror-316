from setuptools import setup, find_packages
 
classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Education",
  "Operating System :: Microsoft :: Windows :: Windows 10",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3"
]
 
setup(
  name="cpulib_py",
  version="1.0.3",
  description="This is a test module.",
  long_description=open("README.rst").read(),
  long_description_content_type="text/x-rst",
  url="",  
  author="CPUcademy",
  author_email="cpucademy@gmail.com",
  license="MIT", 
  classifiers=classifiers,
  keywords="cpucademy learning test",
  packages=find_packages(),
  install_requires=[] 
)