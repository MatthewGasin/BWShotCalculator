from bs4 import BeautifulSoup
import requests

stat_urls = {
    "protoss" : "https://liquipedia.net/starcraft/Protoss_Unit_Statistics",
    "terran"  : "https://liquipedia.net/starcraft/Terran_Unit_Statistics",
    "zerg"    : "https://liquipedia.net/starcraft/Zerg_Unit_Statistics",
}

NULL_TRANSFORM = lambda x: x
SIMPLE_TRANSFORM = lambda x: x.text.replace('s','').strip() # cancer

def ground_attack_transform(node):
    v = SIMPLE_TRANSFORM(node)
    return v if '/' not in v else v[:v.index('/')]

def armor_transform(node):
    v = SIMPLE_TRANSFORM(node)
    return v if '/' not in v else v[:v.index('/')]

def attack_mod_transform(node):
    v = SIMPLE_TRANSFORM(node)
    return v.replace('/', ' ') if '/' in v else f"{v} {v}"

def unit_transform(node):
    return node.findAll('a')[0].text.strip().replace(' ', '_')

html_table_header_map = {
    "Unit" : unit_transform,
    "Size" : SIMPLE_TRANSFORM,
    "Armor" : armor_transform,
    "HP" : SIMPLE_TRANSFORM,
    "Shield" : SIMPLE_TRANSFORM,
    "Ground Attack" : ground_attack_transform,
    "Air Attack" : SIMPLE_TRANSFORM,
    "Attack Mod" : attack_mod_transform,
}
print(html_table_header_map.keys())

for race, url in stat_urls.items():
    page_content = requests.get(url).text
    soup = BeautifulSoup(page_content)
    table = soup.findAll('table', {'class':'wikitable'})
    rows = table[0].findAll('tbody')[0].findAll('tr')
    if not rows:
        continue
    headers, rows = [h.text.strip() for h in rows[:1][0].findAll('th')], rows[1:]
    with open(f"{race}_stats.txt", 'w+') as f:
        for row in rows:
            transformed_vals = []
            for header, node in zip(headers, row.findAll('td')):
                if header in html_table_header_map:
                    transformed_vals.append(html_table_header_map[header](node))
            line = ' '.join(transformed_vals)+'\n'
            print(line)
            f.write(line)
