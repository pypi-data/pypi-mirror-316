from setuptools import setup, find_packages
desc = """datablade is a suite of functions to provide standard syntax across projects."""

setup(name='datablade',version='0.0.0',
      packages=find_packages(where="src"),
      package_dir={'': 'src'},
      install_requires=['pandas','pyarrow','numpy','openpyxl','requests'],
      include_package_data=True,
      description=desc,
      author='Brent Carpenetti',
      author_email='brentcarpenetti@gmail.com',    
      license='MIT',)