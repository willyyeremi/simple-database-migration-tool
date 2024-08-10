"""
Transform longtext data type from mysql to mysql

Args:
    - metadata_dict(dictionary): dictionary of column metadata

Returns:
    target_script(string): string for the column ddl
"""

def default(metadata_dict: dict[str: str]) -> str:
    char_max_length = metadata_dict['char_max_length']
    target_script = f'longtext({char_max_length})'
    return target_script