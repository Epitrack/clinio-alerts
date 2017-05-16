from core import InfoExtractor

def start_extractor(url):
    i = InfoExtractor(url)
    i.run()
    i.print()
    i.persist()
    return