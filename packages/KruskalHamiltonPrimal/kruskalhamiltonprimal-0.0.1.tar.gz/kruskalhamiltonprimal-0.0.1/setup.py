from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='KruskalHamiltonPrimal',
  version='0.0.1',
  author='Prosina_Chetvergova_Toychubecova',
  author_email='prosinaksenia@gmail.com',
  description='Библиотека для работы с графами и алгоритмами, включая алгоритмы Крускала, Гамильтона и минимального остовного дерева',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/Ksenia72/graph_algorithms',
  packages=find_packages(),
  install_requires=['matplotlib==3.9.2', 'networkx==3.4.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='графы алгоритмы Крускала Краскала Гамильтона минимальное остовное дерево ',
  project_urls={
    'GitHub': 'https://github.com/Ksenia72'
  },
  python_requires='>=3.6'
)