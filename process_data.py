import csv
import json
import re
import urllib.parse

def extract_pub_year(source_str):
    match = re.search(r'Tahun\s+(\d{4})', source_str, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0

def clean_data():
    raw_file = 'Penyebab_Kematian_di_Indonesia_yang_Dilaporkan-Raw.csv'
    
    rows = []
    # Using utf-8-sig to automatically strip BOM characters if present
    with open(raw_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Year'] = int(row['Year'])
            row['Total Deaths'] = int(row['Total Deaths'])
            row['PubYear'] = extract_pub_year(row['Source'])
            rows.append(row)
            
    groups = {}
    for row in rows:
        key = (row['Cause'].strip(), row['Year'])
        if key not in groups:
            groups[key] = []
        groups[key].append(row)
        
    cleaned_rows = []
    for key, group_rows in groups.items():
        group_rows.sort(key=lambda x: (x['PubYear'], x['Total Deaths']), reverse=True)
        best_row = group_rows[0]
        cleaned_rows.append(best_row)
        
    cleaned_rows.sort(key=lambda x: (x['Year'], x['Cause']))
    
    final_data = []
    for row in cleaned_rows:
        src = row['Source'].strip()
        if 'Profil Kesehatan Indonesia' in src:
            url = f"https://www.google.com/search?q={urllib.parse.quote_plus(src)}+pdf"
        elif 'COVID19.go.id' in src:
            url = "https://www.google.com/search?q=Data+COVID-19+Indonesia+sumber+covid19.go.id"
        else:
            url = "https://www.kemkes.go.id/id/category/profil-kesehatan"
            
        final_data.append({
            'cause': row['Cause'].strip(),
            'type': row['Type'].strip(),
            'year': row['Year'],
            'deaths': row['Total Deaths'],
            'source': src,
            'url': url
        })
        
    with open('data_kematian_clean.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
        
    print(f"Original rows: {len(rows)}")
    print(f"Cleaned rows: {len(final_data)}")
    
    types = {}
    causes = {}
    for item in final_data:
        types[item['type']] = types.get(item['type'], 0) + item['deaths']
        causes[item['cause']] = causes.get(item['cause'], 0) + item['deaths']
        
    print("\nTotal deaths by Type:")
    for t, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f" - {t}: {count:,}")
        
    print("\nTop 10 causes of death:")
    for c, count in sorted(causes.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f" - {c}: {count:,}")

if __name__ == '__main__':
    clean_data()
