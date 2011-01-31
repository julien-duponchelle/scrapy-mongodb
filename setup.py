from distutils.core import setup
setup(name='ScrapyMongoDB',
      version='0.2.1',
      license='Apache License, Version 2.0',
      description='Scrapy pipeline which allow you to store scrapy items in MongoDB database.',
      author='Julien Duponchelle',
      author_email='julien@duponchelle.info',
      url='http://github.com/noplay/scrapy-mongodb',
      keywords="scrapy mongodb",
      py_modules=['scrapymongodb'],
      platforms = ['Any'],
      install_requires = ['scrapy', 'pymongo'],
      classifiers = [ 'Development Status :: 4 - Beta',
                      'Environment :: No Input/Output (Daemon)',
                      'License :: OSI Approved :: Apache Software License',
                      'Operating System :: OS Independent',
                      'Programming Language :: Python']
)
