from setuptools import setup,find_packages

setup(name='WeissTools',
      version='0.1',
      description='Some Useful Utilities',
      author='Alec Weiss',
      author_email='alec@weissworks.dev',
      url='https://www.weissworks.dev',
      packages=find_packages(),
     )

#build with `pip install -e .`
