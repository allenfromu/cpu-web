import util

util.init('test.bib')

f = open('./People.html', 'w')
f.write(util.getPeople())
f.close()

f = open('./Software.html', 'w')
f.write(util.getSoftware())
f.close()

f = open('./Publications.html', 'w')
f.write(util.getPublications())
f.close()
