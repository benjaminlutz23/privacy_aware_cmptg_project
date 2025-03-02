import xml.etree.ElementTree as ET
import json
import os

def xml_to_json(xml_file_path, json_output_path=None):
    """
    Convert the OPP-115 categories XML file to JSON format
    
    Args:
        xml_file_path: Path to the XML file
        json_output_path: Path where the JSON file should be saved (optional)
        
    Returns:
        Dictionary containing the parsed data
    """
    # Check if XML file exists
    if not os.path.isfile(xml_file_path):
        print(f"ERROR: XML file not found at path: {xml_file_path}")
        print(f"Current working directory: {os.getcwd()}")
        return None
    
    # Parse XML
    try:
        print(f"Opening XML file: {xml_file_path}")
        # Remove the XML namespace to simplify parsing
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        print(f"XML file read successfully, size: {len(xml_content)} bytes")
            
        # Remove namespaces
        for ns in [' xmlns="http://www.w3schools.com"', 
                   ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
                   ' xsi:schemaLocation="annotation.xsd"']:
            xml_content = xml_content.replace(ns, '')
        
        # Parse the modified XML content
        root = ET.fromstring(xml_content)
        print("XML parsed successfully")
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return None

    # Initialize result dictionary
    result = {
        'version': root.find('version').text,
        'categories': []
    }
    
    # Process each category
    category_count = 0
    for category_elem in root.findall('category'):
        category = {
            'name': category_elem.find('name').text,
            'attributes': []
        }
        
        # Process attributes for this category
        attributes_elem = category_elem.find('attributes')
        if attributes_elem is not None:
            for attr_elem in attributes_elem.findall('attribute'):
                attribute = {
                    'name': attr_elem.find('name').text,
                    'values': []
                }
                
                # Add optional attribute properties
                if 'optional' in attr_elem.attrib:
                    attribute['optional'] = attr_elem.attrib['optional'] == 'true'
                if 'default' in attr_elem.attrib:
                    attribute['default'] = attr_elem.attrib['default']
                
                # Process values for this attribute
                values_elem = attr_elem.find('values')
                if values_elem is not None:
                    for value_elem in values_elem.findall('value'):
                        value = {
                            'name': value_elem.find('name').text,
                        }
                        attribute['values'].append(value)
                
                category['attributes'].append(attribute)
        
        result['categories'].append(category)
        category_count += 1
    
    print(f"Processed {category_count} categories")
    
    # Output JSON
    if json_output_path:
        try:
            with open(json_output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Verify the JSON file was created and has content
            if os.path.exists(json_output_path):
                file_size = os.path.getsize(json_output_path)
                if file_size > 0:
                    print(f"JSON data saved to {json_output_path} (size: {file_size} bytes)")
                else:
                    print(f"WARNING: JSON file {json_output_path} was created but is empty")
            else:
                print(f"ERROR: Failed to create JSON file at {json_output_path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
    
    return result

if __name__ == "__main__":
    # Get current directory for better path handling
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script running from: {current_dir}")
    
    # Define paths using os.path.join for better cross-platform compatibility
    xml_path = os.path.abspath(os.path.join(current_dir, "..", "data", "opp-115-dataset", "documentation", "categories-july30.xml"))
    json_path  = os.path.abspath(os.path.join(current_dir, "..", "data", "benchmark", "annotation_to_icon_mappings.json"))
    
    print(f"XML path: {xml_path}")
    print(f"JSON path: {json_path}")
    
    # Convert XML to JSON
    xml_to_json(xml_path, json_path)
    
    # Additional check after conversion
    if os.path.exists(json_path):
        print(f"Verification: JSON file exists at {json_path}")
        print(f"File size: {os.path.getsize(json_path)} bytes")
    else:
        print(f"Verification failed: JSON file not found at {json_path}")
