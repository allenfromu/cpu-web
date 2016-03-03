import parser


file = open('test.bib', 'r')
input = file.read()

p = (parser.Parser(input)).getEntries()



people = {}
sw = {}
pb = {}

for k in p:
    v = p[k]
    if 'TYPE' in v and v['TYPE'] == 'person':
        people[k] = v
    elif 'TYPE' in v and (v['TYPE'] == 'software' or v['TYPE'] == 'sw'):
        sw[k] = v
    else:
        pb[k] = v

print(sw)
f1 = open('people.html', 'w')

for k in people:
    v = people[k]
    if 'TITLE' in v:
        html = '\n<p>\n<span class = \"person_name\">'
        if 'URL' in v and len(v['URL']) > 2:
            html+='\n<a href=\"'+v['URL']+'\">'+v['TITLE']
            html+='</a>'
        else:
            html+=v['TITLE']
        html+='\n</span>'
        html+='\n<br>'
        if 'NOTES' in v:
            html+='\n<span>'
            html+=v['NOTES']+'\n</span>'
        if 'CROSSREF' in v:
            html+='\n<br><span>Related:'+ v['CROSSREF']+'</span>'
        html+='\n</p>\n'
        f1.write(html)
f1.close()


f2 = open('sw.html', 'w')

for k in sw:
    v = sw[k]
    if 'TITLE' in v:
        html= '\n<p>\n<span class=\"sw_name\">'
        if 'URL' in v and len(v['URL']) > 2:
            html+='\n<a href=\"'+v['URL']+'\">'+v['TITLE']
            html+='</a>'
        else:
            html+=v['TITLE']
        html+='\n</span>'
        html+='\n<br>'
        if 'NOTES' in v:
            html+='\n<span>'
            html+=v['NOTES']+'\n</span>'
        if 'CROSSREF' in v:
            html+='\n<br><span>Related:'+ v['CROSSREF']+'</span>'
        html+='\n</p>\n'
        f2.write(html)
f2.close()

f3 = open('pb.html', 'w')

for k in pb:
    v = pb[k]
    
f3.close()

def split_authors(s):
    l = re.split(',|and', s)
    ll = []
    for a in l:
        ll.append(a.strip())
    return ll
    
    





#print (pb)
