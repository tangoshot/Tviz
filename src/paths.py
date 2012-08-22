from os.path import join, dirname 

SRC = dirname(__file__)
DATA = join(SRC, 'data')
TEMPLATES = join(DATA, 'templates')
TVIZ = join(SRC, '..')
TESTBED = 'c:/TestBed/tviz'
DEFAULT_IMAGES = join(DATA, 'images')

SETTINGS = join(SRC, 'data', 'settings')

HTML = join(TESTBED, 'html') 

def template_file(name):
    return join(TEMPLATES, name)
    
def html_file(name):
    return join(HTML, name)
    
if __name__ == '__main__':
    print 'SRC: ', SRC
    print 'DATA: ', DATA
    print 'TEMPLATES: ', TEMPLATES
    print 'template_file(sample): ', template_file('sample')
    