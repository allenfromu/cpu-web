import parser
import re

file = open('test.bib', 'r')
input = file.read()

p = (parser.Parser(input)).getEntries()


def split_crossref(s):
    l = s.split(',')
    ll = []
    for a in l:
        ll.append(a.strip())
    return ll

people = {}
sw = {}
pb = {}

for k in p:
    v = p[k]
    #print(k)
    if 'TYPE' in v and v['TYPE'].upper() == 'PERSON':
        people[k] = v
    elif 'TYPE' in v and (v['TYPE'].upper() == 'SOFTWARE' or v['TYPE'].upper() == 'SW'):
        sw[k] = v
    else:
        pb[k] = v

f1 = open('./People.html', 'w')

def get_people():
    html = '<ul>'
    for k in people:
        v = people[k]
        html+='\n<li>'
        if 'TITLE' in v:
            html += '\n<p>\n<span id = \"'+k+'\">'
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
                ll = split_crossref(v['CROSSREF'])
                #print(ll)
                html+='\n   <br> <span>Related: '
                for a in ll:
                    if a in p:
                        av = p[a]
                        if 'TYPE' in av and av['TYPE']=='person':  
                            html+='[<a href=\"\\People.html#'+a+'\">'+a+'</a>]'
                        elif 'TYPE' in av and av['TYPE']=='software':  
                            html+='[<a href=\"\\Software.html#'+a+'\">'+a+'</a>]'
                        else:
                            html+='[<a href=\"\\Publications.html#'+a+'\">'+a+'</a>]'
                html+='\n </span>\n<br>'
            html+='\n</p>\n'
        html+='\n</li>'
    html += '\n</ul>'
    f1.write(html)
    f1.close()
    return html

get_people()

f2 = open('./Software.html', 'w')
def get_sw():
    html = '<ul>'
    for k in sw:
        v = sw[k]
        if 'TITLE' in v:
            html +='\n<li>'
            html += '\n<p>\n<span id=\"'+k+'\">'
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
                ll = split_crossref(v['CROSSREF'])
                html+='\n    <br><span>Related: '
                for a in ll:
                    if a in p:
                        av = p[a]
                        if 'TYPE' in av and av['TYPE']=='person':  
                            html+='[<a href=\"\\People.html#'+a+'\">'+a+'</a>]'
                        elif 'TYPE' in av and av['TYPE']=='software':  
                            html+='[<a href=\"\\Software.html#'+a+'\">'+a+'</a>]'
                        else:
                            html+='[<a href=\"\\Publications.html#'+a+'\">'+a+'</a>]'
                html+='\n     </span>\n    <br>'
            html+='\n</p>\n'
            html+='</li>'
    html+='\n</ul>'
    f2.write(html)
    f2.close()
    return html

get_sw()




def split_authors(s):
    l = re.split(',|and', s)
    ll = []
    for a in l:
        ll.append(a.strip())
    return ll
    
    
def get_author_url(name):
    for k in people:
        v = people[k]
        if 'TITLE' in v and v['TITLE'].strip() == name:
            url = '/People.html#'+k
            return url
    return None
            


f3 = open('./Publications.html', 'w')

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
def get_pb():
    html = '<ul class = \"list-group\">'
    for y in years:
        keys = year_keys[y]
        html += '\n <li class=\"pb_'+str(y)+' list-group-item\"><p><h3>'+str(y)+'</h3></p>'
        html += '\n  <ul class=\"list-group\">'
        for k in keys:
            v = pb[k]
            if 'TITLE' in v or 'BOOKTITLE' in v:
                html+='\n   <li class=\"list-group-item\"><div id=\"'+k+'\">'
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
                if 'TITLE' in v and 'BOOKTITLE' in v:
                    html+='\n    <span>'+v['BOOKTITLE']+'</span>\n    <br>'
                if 'PUBLISHER' in v:
                    html+='\n    <span>'+v['PUBLISHER']+'</span>\n    <br>'
                if 'YEAR' in v and 'MONTH' in v:
                    html+='\n    <span>'+v['MONTH']+', '+v['YEAR']+'</span>\n    <br>'
                if 'CROSSREF' in v:
                    ll = split_crossref(v['CROSSREF'])
                    html+='\n    <span>Related: '
                    for a in ll:
                        if a in p:
                            av = p[a]
                            if 'TYPE' in av and av['TYPE']=='person':  
                                html+='[<a href=\"\\People.html#'+a+'\">'+a+'</a>]'
                            elif 'TYPE' in av and av['TYPE']=='software':  
                                html+='[<a href=\"\\Software.html#'+a+'\">'+a+'</a>]'
                            else:
                                html+='[<a href=\"\\Publications.html#'+a+'\">'+a+'</a>]'
                    html+='\n     </span>\n    <br>'
                html+='\n  </div> </li>'
        html+='\n  </ul>'
        html+='<span class=\"badge\">'+str(len(keys))+'</span>'
        html+='\n </li>'
    html+='\n</ul>'
    f3.write(html)
    f3.close()
    return html

get_pb()




#print (pb)
