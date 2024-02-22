import xml.etree.ElementTree as ET

from thesis.osm import (ChangeInfo, ChangeType, ElementIdentifier, ElementType,
                        OSCInfo)


def get_change_info(osc_file_path: str) -> OSCInfo:
    """Get change info from osc file."""
    tree = ET.parse(osc_file_path)
    root = tree.getroot()
    result: OSCInfo = []
    for change_tag in root:
        info = _get_change_info_for_group(change_tag)
        result.extend(info)
    return result


def _get_change_info_for_group(change_tag: ET.Element) -> OSCInfo:
    result = []
    change_type = ChangeType[change_tag.tag.upper()]
    for element_tag in change_tag:
        entity_id = int(element_tag.attrib["id"])
        idf = ElementIdentifier(entity_id, ElementType[element_tag.tag.upper()])
        info = ChangeInfo(change_type, idf)
        result.append(info)

    return result
