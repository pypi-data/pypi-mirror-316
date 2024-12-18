def _extract_attribute_data(msg, attributes):
    attribute_data = msg
    # Skip the first attribute since it is the topic name
    for attr in attributes[1:]:
        attribute_data = getattr(attribute_data, attr)
    return attribute_data