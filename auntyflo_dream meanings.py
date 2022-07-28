import requests
from bs4 import BeautifulSoup as bs
import re



l_main_url = []
for i in range(1,4):
    main_url = f'https://www.auntyflo.com/sitemap.xml?page={i}'
    l_main_url.append(main_url)

l_url = []

for i in range(len(l_main_url)):
    r = requests.get(l_main_url[i])
    soup = bs(r.content, 'xml')
    urls = soup.find_all('loc')
    url = [loc.text for loc in urls]
    for num in range(len(url)):
        if re.search(r'https://www.auntyflo.com/dream-dictionary/.*', url[num]):
            l_url.append(url[num])

l_url = sorted(l_url)

l_data = []

for num in range(len(l_url)):
    r = requests.get(l_url[num])
    soup = bs(r.content)

    main_head = soup.find("h2", class_ = "node-title field-wrapper text-center")
    print(main_head.text.strip(), end='')   # This line of code is only to confirm if code is running smoothly.

    sub_head = soup.find("h2", class_ = "node-title text-left")

    div = soup.find("div", class_="field-wrapper body field field-node--body field-name-body field-type-text-with-summary field-label-hidden")

    tag_p = list(div.p.next_siblings)

    try:
        l_data.append([l_url[num]+',\n', '@# '+main_head.text.strip()+',\n', '@## '+sub_head.text.strip()+',\n', div.find('p').text, '\n'])
        l_data.append('\n')

        for i in range(len(tag_p)):
            if tag_p[i].name == 'h3':
                break
            elif tag_p[i].name == 'p':
                l_data.append([l_url[num]+',\n','@# '+main_head.text.strip()+',\n','@## '+sub_head.text.strip()+',\n', tag_p[i].text, '\n'])
                l_data.append('\n')

        for i in range(len(tag_p)):
            if tag_p[i].name == 'h3':
                for c in range(1, len(div.find_all(['p', 'li']))):
                    if tag_p[i+c].name == 'p':
                        l_data.append([l_url[num]+',\n', '@# '+main_head.text.strip()+',\n', '@## '+sub_head.text.strip()+',\n', '@### '+tag_p[i].text+',\n', tag_p[i+c].text, '\n'])
                        l_data.append('\n')
                    elif tag_p[i+c].name == 'ul':
                        for txt_line in (tag_p[i+c].text.split('\n')[1:-1]):
                            l_data.append([l_url[num]+',\n', '@# '+main_head.text.strip()+',\n', '@## '+sub_head.text.strip()+',\n', '@### '+tag_p[i].text+',\n', txt_line, '\n'])
                            l_data.append('\n')
                    elif tag_p[i+c].name == 'h3':
                        break
    except Exception as e:
        print()

with open('auntyflo data text file.txt', 'w', encoding="utf-8") as f:
    for datas in l_data:
        for data in datas:
            f.write(data)
