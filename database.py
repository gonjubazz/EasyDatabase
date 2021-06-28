import ast
from typing import TextIO, Any
from cryptography.fernet import Fernet


#  region Encryption
def write_key():
    key = Fernet.generate_key()
    with open('crypto.key', 'wb') as key_file:
        key_file.write(key)


# write_key()
def load_key():
    return open('crypto.key', 'rb').read()


def encrypt(data, key):
    f = Fernet(key)

    encrypted_data = f.encrypt(data)
    return encrypted_data


def decrypt(data, key):
    f = Fernet(key)
    encrypted_data = data
    decrypted_data = f.decrypt(encrypted_data)

    return decrypted_data

print(decrypt(b"gAAAAABg2iA6m1iM44cB_tSDUoi2EO3bqlLCwmUzoXI5JPib5Gu6H6VFB-NUREoL2Lyd9dZc9Z7p_Ih74BErSbe7XdkG3NrClgqJpg0OrDIMgmHQ8pxfz08=gAAAAABg2ijPyGy4Se3zT7h1_IASmH8eSBmSOwZan-5XvZjntNGpVyau05y6KK4SLqD-gK1CuxCxwsk2Lt-iM5lZoMbHRftK0w==", key=load_key()))

#  endregion
key = load_key()


class Variable:
    def __init__(self, value, index, var_type):
        self.index = index
        self.type = var_type

        if var_type == "int":
            self.value = int(value)
        if var_type == "float":
            self.value = float(value)
        if var_type == "string":
            self.value = value
        if var_type == "bool":
            self.value = bool(value)
        if var_type == "list":
            self.value = ast.literal_eval(value)
        if var_type == "dict":
            self.value = ast.literal_eval(value)


class Database:
    __lines: list[str]
    __variables: dict[Any, Any]
    __database: TextIO

    def __init__(self, database_path):
        self.path = database_path
        self.__init()

    #  region Private functions
    def __init(self):
        self.__database = open(self.path, "rb")
        self.__lines = self.__database.readlines()
        print(decrypt(self.__lines[0], key).decode("utf-8"))
        self.__lines = decrypt(self.__lines[0], key).decode("utf-8").split("\r\n")
        self.__variables = {}

        for var in self.__lines:
            data = var.split(":")
            self.__variables[data[0]] = Variable(data[2], self.__lines.index(var), data[1])

        self.__database.close()

    def __variable_index(self, name):
        try:
            return self.__variables[str(name)].index
        except KeyError:
            print("variable not found")

    def __clear_db(self):
        self.__database.close()
        self.__database = open(self.path, "r")
        self.__database.readlines()
        self.__database.close()
        self.__database = open(self.path, "w").close()

    #  endregion
    #  region Public functions

    def get_variable(self, name: str) -> str:
        try:
            return self.__variables[name]
        except KeyError:
            return None

    def get_variables(self, method: str, from_: int, to: int) -> (str, int, int):
        if from_ == -1 and to == -1:
            if method == "full":
                return self.__variables
            if method == "values":
                values = []
                for var in self.__variables.values():
                    values.append(var.value)

                return values
            if method == "names":
                values = []
                for var in self.__variables.keys():
                    values.append(var)

                return values
        else:
            variables = []
            for key in self.__variables.keys():
                if from_ <= self.__variables[key].index <= to:
                    if method == "full":
                        variables.append(self.__variables[key])
                    if method == "values":
                        variables.append(self.__variables[key].value)
                    if method == "names":
                        variables.append(key)

            return variables

    def set_variable(self, name: str, var_type: str, new_value) -> (str, str):
        index = self.__variable_index(name)
        new_data = ""
        iteration = 0

        self.__clear_db()
        self.__database = open(self.path, "wb")

        for variable in self.__lines:
            if iteration + 1 != len(self.__lines):
                if iteration == index:
                    new_data += f"{name}:{var_type}:{new_value}\n"
                else:
                    new_data += variable + "\n"
            else:
                if iteration == index:
                    new_data += f"{name}:{var_type}:{new_value}"
                else:
                    new_data += variable

            iteration += 1

        self.__database.write(encrypt(new_data, key))
        self.__database.close()

        self.__init()

    def new_variable(self, name: str, var_type: str, value) -> (str, str):
        file = open(self.path, "rb")
        file_data = file.read()
        file.close()

        self.__database = open(self.path, "wb")

        if self.get_variable(name) is None:
            if len(self.__lines) != 0:
                print(file_data + encrypt(f"\n{name}:{var_type}:{value}".encode("utf-8"), key))
                self.__database.write(file_data + encrypt(f"\n{name}:{var_type}:{value}".encode("utf-8"), key))
            else:
                self.__database.write(file_data + encrypt(f"{name}:{var_type}:{value}".encode("utf-8"), key))

        self.__init()

    def delete_variable(self, name: str) -> str:
        index = self.__variable_index(name)
        new_data = ""
        iteration = 0

        self.__clear_db()
        self.__database = open(self.path, "wb")

        for variable in self.__lines:
            if iteration + 1 != len(self.__lines):
                if iteration != index:
                    new_data += variable + "\n"
            else:
                if iteration != index:
                    new_data += variable

            iteration += 1

        self.__database.write(encrypt(new_data, key))
        self.__database.close()

        self.__init()

    # endregion
