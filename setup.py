from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='fhmediacollector',
      version='1.1.4',
      description='e621 media collection and organization for video creation',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://github.com/oddpawsx/fhmediacollector',
      author='OddPawsX',
      author_email='78638049+oddpawsx@users.noreply.github.com',
      packages=['fhmediacollector'],
      zip_safe=False,
      install_requires=[
          'requests',
          'python-dotenv'
      ],
      include_package_data=True,
      # scripts=['bin/fhcollector']
      entry_points={
		'console_scripts': ['fhcollector=fhmediacollector:cli']
	  }
      )
