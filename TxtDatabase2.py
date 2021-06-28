import ast
from typing import TextIO, Any


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
        self.__database = open(self.path, "r+")
        self.__lines = self.__database.readlines()
        self.__variables = {}

        for var in self.__lines:
            data = var.split(":")
            self.__variables[data[0]] = Variable(data[2], self.__lines.index(var), data[1])

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


    def get_variable(self, name):
        try:
            return self.__variables[name]
        except KeyError:
            print("variable not founded")
            return None

    def get_all_variables(self, method):
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

    def set_variable(self, name, var_type, new_value):
        index = self.__variable_index(name)
        new_data = ""
        iteration = 0

        self.__clear_db()
        self.__database = open(self.path, "w")

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

        self.__database.write(new_data)
        self.__database.close()

        self.__init()

    def new_variable(self, name, var_type, value):
        if len(self.__lines) != 0:
            self.__database.write(f"\n{name}:{var_type}:{value}")
        else:
            self.__database.write(f"{name}:{var_type}:{value}")

        self.__init()

    def delete_variable(self, name):
        index = self.__variable_index(name)
        new_data = ""
        iteration = 0

        self.__clear_db()
        self.__database = open(self.path, "w")

        for variable in self.__lines:
            if iteration + 1 != len(self.__lines):
                if iteration != index:
                    new_data += variable + "\n"
            else:
                if iteration != index:
                    new_data += variable

            iteration += 1

        self.__database.write(new_data)
        self.__database.close()

        self.__init()

    # endregion
