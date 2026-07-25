import json

with open('data_embedded.json', 'r') as f:
    raw_data = json.load(f)

json_districts = json.dumps(raw_data['districts'])
json_taluks = json.dumps(raw_data['taluks'])
json_updated_date = raw_data.get('updated_date', '')
json_period_dates = json.dumps(raw_data.get('period_dates', {}))

with open('template_rainfall_status.html', 'r', encoding='utf-8') as f:
    template = f.read()

template = template.replace('__JSON_DISTRICTS__', json_districts)
template = template.replace('__JSON_TALUKS__', json_taluks)
template = template.replace('__JSON_UPDATED_DATE__', json_updated_date)
template = template.replace('__JSON_PERIOD_DATES__', json_period_dates)

for fname in ['rainfall status.html', 'rainfall_status.html']:
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(template)

print('Updated rainfall status.html and rainfall_status.html successfully!')
