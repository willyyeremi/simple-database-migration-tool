'''
Module to create a class from database connection credential. This module get credential from credential.csv at root folder.
'''
from sys import path
from pathlib import Path
from pandas import DataFrame
from pandas import Series
from pandas import read_csv

root = str(Path(__file__).parent.parent)
path.insert(0,str(root))

class connection:
    '''
    Class object to create a connection object that can be accessed from another module
    '''

    def __init__(self, product: str, host: str, port: str, user: str, password: str, database: str, local_environment: str) -> None:
        # name of the database product
        self.product = product
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        # name of the database
        self.database = database
        # path to oracle instantclient, if using oracle
        self.local_environment = local_environment

    def __str__(self) -> str:
        return f'product = {self.product}, local environment path = {self.local_environment} -> {self.user}:{self.password}@{self.host}:{self.port}'

    def __repr__(self) -> str:
        return f'connection(product = {self.product}, host = {self.host}, port = {self.port}, user = {self.user}, password = {self.password}, database = {self.database}, local_environment = {self.local_environment})'

    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__

def credential_get() -> DataFrame:
    """
    Function to get the credential data from credential.csv
    
    Returns:
        credential_data (pandas dataframe): table containing credential to connect to database
        credential_dict (list): result of transforming credential_data into a list of data per row (each row stored as dictionary)
    """
    credential_data: DataFrame = read_csv(filepath_or_buffer = f"{root}\\credential.csv", sep = "|", dtype = {"port": "object"})
    credential_dict: list[dict[str, str]] = credential_data.to_dict('records')
    return credential_data, credential_dict

def credential_check(credential_data: DataFrame) -> None:
    """
    Function to check whether all credentials are unique or not. This function will raise an error if credential.csv is empty or have duplicated data.
    
    Args:
        credential_data (pandas dataframe): table produced by credential_get()
    """
    if len(credential_data) == 0:
        check_value: int = 0
        check_string: str = "credential.csv is empty. please fill it first with valid credential."
    else:
        credential_data['id']: Series = credential_data['host'] + credential_data['port'] + credential_data['user'] + credential_data['password'] + credential_data['database']
        credential_data: DataFrame = credential_data.groupby('id')['name'].apply(list).reset_index()
        credential_data: list[dict[str, str]] = credential_data.to_dict('records')
        identical_credential: list[list[str]] = [item['name'] for item in credential_data if len(item['name']) > 1]
        if len(identical_credential) > 0:
            identical_credential_string: str = """"""
            for group in identical_credential:
                group_string: str = """- """
                for name in group:
                    group_string: str = group_string + name
                    if name != group[-1]:
                        group_string: str = group_string + ", "
                group_string: str = group_string + "\n"
                identical_credential_string: str = identical_credential_string + group_string
            check_value: int = 0
            check_string: str = f"there is duplicate credential. please choose one each group of duplicate.\n{identical_credential_string}"
        else:
            check_value: int = 1
            check_string: str = "there is no problem with credential.csv data."
    if check_value != 1:
        raise Exception(check_string)
    else:
        print(check_string)
        pass

def main():
    credential_data, credential_dict  = credential_get()
    credential_check(credential_data)
    for credential in credential_dict:
        globals()[credential['name']]: object = connection(credential['product'], credential['host'], credential['port'], credential['user'], credential['password'], credential['database'], credential['local_environment'])
        print(f"credential {credential['name']}: {str(globals()[credential['name']])}")

if __name__ == '__main__':
    main()