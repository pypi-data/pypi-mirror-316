from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='sijeydev',
  version='1.0.0',
  author='sijeydev',
  author_email='sijeydev@gmail.com',
  description='This is my first module!',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://t.me/sijeydev',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='sijeydev',
  project_urls={
      'Documentation': 'https://t.me/sijeydev'
  },
  python_requires='>=3.7'
)
