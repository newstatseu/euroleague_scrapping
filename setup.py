from setuptools import setup

setup(
    setup_requires=["pbr"],
    pbr=True,
    name='euroleague_scrapping',
    packages=['euroleague_scrapping'],
    url='https://github.com/newstatseu/euroleague_scrapping',
    license='Apache 2.0',
    author='NewstatsEu',
    author_email='euroleague.dataguy@gmail.com',
    description='Eurocup/Euroleague Scrapping',
    long_description='Eurocup/Euroleague Scraping'
)
