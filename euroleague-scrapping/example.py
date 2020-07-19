from euroleague_scrapping.Euroscrapper import Euroscrapper

if __name__ == '__main__':
    scrapper = Euroscrapper(league="eurocup",years=[2019])
    scrapper.start()