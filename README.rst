
Euroleague and Eurocup Scrapper
-------------------------------

Welcome to `newstats.eu <https://newstats.eu>`_ **Euroleague
and Eurocup scrapper**\ !

This is a simple project to help you download basketball data from
`euroleague <https://www.euroleague.net>`_ and `eurocup <https://www.eurocupbasketball.com>`_

You need to have **python>=3.6** installed in order to use the library.

Installation and usage
----------------------

Install it using:

.. code-block::

   pip install euroleague_scrapping

If you want to download Euroleague data for season 2019-2020 try:

.. code-block::

   scrapper = Euroscrapper(years=[2019])
   scrapper.start()

It will create a ``data/euroleague`` folder in your current path.
If you prefer a different path to store the data (lets say ``/tmp/data``\ ), try:

.. code-block::

   scrapper = Euroscrapper(datadir="/tmp/data",years=[2019])
   scrapper.start()

If you want to download Eurocup data for season 2019-2020 try:

.. code-block::

   scrapper = Euroscrapper(league="eurocup",years=[2019])
   scrapper.start()

If you want to download Euroleague data for all the seasons try (it will take a while): 

.. code-block::

   scrapper = Euroscrapper()
   scrapper.start()

If you want to download Euroleague data for the last 3 seasons try:

.. code-block::

   scrapper = Euroscrapper(years=[2017,2018,2019])
   scrapper.start()

Hopefully you can adopt the calls to fit your needs.

If you enjoyed the library and found it useful give us a shout in
Twitter `@newstatseu <twitter.com/newstatseu>`_
