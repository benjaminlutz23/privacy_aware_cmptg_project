import json
import os

def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_json(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

def get_icon_mapping(annotation, mappings):
    icons = []
    for category in mappings['categories']:
        if category['name'] == annotation['category']:
            for attribute in category['attributes']:
                for value in attribute['values']:
                    if value['name'] == annotation['details'].get(attribute['name'], {}).get('value', ''):
                        icons.append({'icon': value['icon'], 'color': value['color']})
    return icons

def prioritize_icons(icons):
    priority = {'red': 1, 'yellow': 2, 'green': 3, 'gray': 4, 'white': 5}
    unique_icons = {}
    for icon in icons:
        icon_name = icon['icon']
        icon_color = icon['color'].lower()
        if icon_name not in unique_icons or priority[icon_color] < priority[unique_icons[icon_name]['color'].lower()]:
            unique_icons[icon_name] = icon
    return list(unique_icons.values())

def process_file(annotated_policies_path, benchmarked_policies_path, mappings):
    annotated_policies = load_json(annotated_policies_path)
    benchmarked_policies = {}

    for section, annotations in annotated_policies.items():
        icons = []
        for annotation in annotations:
            icons.extend(get_icon_mapping(annotation, mappings))
        benchmarked_policies[section] = prioritize_icons(icons)

    save_json(benchmarked_policies_path, benchmarked_policies)

def main():
    annotated_policies_dir = '../data/benchmark/annotated_policies'
    benchmarked_policies_dir = '../data/benchmark/benchmarked_policies'
    mappings_path = '../data/benchmark/annotation_to_icon_mappings.json'

    mappings = load_json(mappings_path)

    if not os.path.exists(benchmarked_policies_dir):
        os.makedirs(benchmarked_policies_dir)

    for filename in os.listdir(annotated_policies_dir):
        if filename.endswith('.json'):
            annotated_policies_path = os.path.join(annotated_policies_dir, filename)
            benchmarked_policies_path = os.path.join(benchmarked_policies_dir, filename)
            process_file(annotated_policies_path, benchmarked_policies_path, mappings)

if __name__ == '__main__':
    main()
