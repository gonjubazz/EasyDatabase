import ast


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


class DataBase:
    def __init__(self, database_path):
        self.path = database_path
        self.init()

    def init(self):
        self.database = open(self.path, mode="r+")
        self.NonFilteredVariables = self.database.read().split("\n")
        self.Variables = {}

        for variable in self.NonFilteredVariables:
            data = variable.split(":")
            self.Variables[data[0]] = Variable(data[2], self.NonFilteredVariables.index(variable), data[1])

    def get_variable(self, name):
        try:
            return self.Variables[name]
        except KeyError:
            return None

    def set_variable(self, name, var_type, new_value):
        index = self.Variables[name].index
        self.database.seek(0)

        new_data = ""

        iteration = 0
        for variable in self.NonFilteredVariables:
            if iteration + 1 != len(self.NonFilteredVariables):
                if iteration == index:
                    new_data += f"{name}:{var_type}:{new_value}\n"
                else:
                    new_data += self.NonFilteredVariables[iteration] + "\n"
            else:
                if iteration == index:
                    new_data += f"{name}:{var_type}:{new_value}"
                else:
                    new_data += self.NonFilteredVariables[iteration]

            iteration += 1

        self.database.write(new_data)
        self.database.close()

        self.init()

    def new_variable(self, name, var_type, value):
        self.database.write(f"\n{name}:{var_type}:{value}")

        self.init()

    def delete_variable(self, name):
        index = self.Variables[name].index
        self.database.seek(0)

        new_data = ""

        iteration = 0
        for variable in self.NonFilteredVariables:
            if iteration + 1 != len(self.NonFilteredVariables):
                if iteration == index:
                    pass
                else:
                    new_data += self.NonFilteredVariables[iteration] + "\n"
            else:
                if iteration == index:
                    pass
                else:
                    new_data += self.NonFilteredVariables[iteration]

            iteration += 1

        self.database.write(new_data)
        self.database.close()

        self.init()
