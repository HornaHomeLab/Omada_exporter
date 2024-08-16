def map_data_values(data: dict, fields_to_map: list[str], fields_values: dict[str,dict]) -> dict:
    for field in fields_to_map:
        if field in list(data.keys()):
            data[field] = fields_values[field].get(data[field])
            
    return data