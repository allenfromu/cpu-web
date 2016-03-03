import parser
import re

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

#print(sw)
f1 = open('../People.html', 'w')

html = '<ul>'
for k in people:
    v = people[k]
    html+='\n<li>'
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
    html+='\n</li>'
html += '\n</ul>'
f1.write(html)
f1.close()


f2 = open('../Software.html', 'w')
html = '<ul>'
for k in sw:
    v = sw[k]
    if 'TITLE' in v:
        html +='\n<li>'
        html += '\n<p>\n<span class=\"sw_name\">'
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
        html+='</li>'
html+='\n</ul>'
f2.write(html)
f2.close()




def split_authors(s):
    l = re.split(',|and', s)
    ll = []
    for a in l:
        ll.append(a.strip())
    return ll
    
    
def get_author_url(name):
    for k in people:
        v = people[k]
        if 'TITLE' in v and v['TITLE'].strip() == name and 'URL' in v:
            return v['URL']
    return None
            



f3 = open('../Publications.html', 'w')

#(key, year) tuple of pb
years = []
year_keys = {}

for k in pb:
    v = pb[k]
    if 'YEAR' in v:
        year = int(v['YEAR'])
        if year in year_keys:
            year_keys[year].append(k)
        else:
            year_keys[year] = [k]
            years.append(year)
            
years.sort()
years.reverse()
html = '<ul class = \"list-group\">'
for y in years:
    keys = year_keys[y]
    html += '\n <li class=\"pb_'+str(y)+' list-group-item\"><p><h3>'+str(y)+'</h3></p>'
    html += '\n  <ul>'
    for k in keys:
        v = pb[k]
        print(v)
        print('\n')
        if 'TITLE' in v or 'BOOKTITLE' in v:
            html+='\n   <li>'
            if 'TITLE' in v:
                html+='\n    <span>'+v['TITLE']+'</span>'
            else:
                html+='\n    <span>'+v['BOOKTITLE']+'</span>'
            
            if 'URL' in v:
                html+='\n    <span>[<a href=\"'+v['URL']+'\">PDF</a>]</span>'
            html+='\n     <br>'
            if 'AUTHOR' in v:
                authors = split_authors(v['AUTHOR'])
                html+='\n    <span>'
                num = len(authors)
                for n in range(num):
                    name = authors[n]
                    url = get_author_url(name)
                    if url is not None:
                        html+='<a href=\"'+url+'\">'+name+'</a>'
                    else:
                        html+=name
                    if n != num -1:
                        html+=','
                html+='</span>\n    <br>'
#            if 'NOTES' in v:
#               html+='\n    <span>Note:'+v['NOTES']+'</span><br>'
#            elif 'NOTE' in v:
#             html+='\n    <span>Note:'+v['NOTE']+'</span><br>'
                
            html+='\n   </li>'
    html+='\n  </ul>'
    html+='<span class=\"badge\">'+str(len(keys))+'</span>'
    html+='\n </li>'
html+='\n</ul>'

f3.write(html)                
                
             
    
f3.close()





#print (pb)
