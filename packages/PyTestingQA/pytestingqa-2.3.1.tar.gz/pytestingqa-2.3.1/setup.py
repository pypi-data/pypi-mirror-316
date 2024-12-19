from setuptools import setup

readme = open("./README.md","r")

setup(
      # Basic data for the library.
      name = "PyTestingQA",
      packages = ['PyTestingQA'], # The same as "name"
      version = '2.3.1',
      description = "It's a automatic testing program, for QA.",
      long_description = readme.read(),
      long_description_content_type = 'text/markdown',
      author = 'CyberCoral', # The author
      
      url = "https://github.com/CyberCoral/PyTesting", # The urls
      download_url = "https://github.com/CyberCoral/PyTesting/archive/refs/tags/v2.3.tar.gz",
      
      classifiers = [],
      include_package_data = True
      )
