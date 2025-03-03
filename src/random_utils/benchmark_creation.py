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

def main():
    annotated_policies_path = '../data/benchmark/annotated_policies/20_theatlantic.com.json'
    benchmarked_policies_path = '../data/benchmark/benchmarked_policies/20_theatlantic.com.json'
    mappings_path = '../data/benchmark/annotation_to_icon_mappings.json'

    annotated_policies = load_json(annotated_policies_path)
    mappings = load_json(mappings_path)
    benchmarked_policies = {}

    for section, annotations in annotated_policies.items():
        icons = []
        for annotation in annotations:
            icons.extend(get_icon_mapping(annotation, mappings))
        benchmarked_policies[section] = icons

    save_json(benchmarked_policies_path, benchmarked_policies)

if __name__ == '__main__':
    main()
