class Data:
    def __init__(self, pathAmbiente, pathSinaisVitais):
        self.pathAmbiente = pathAmbiente
        self.pathSinaisVitais = pathSinaisVitais
        self.ambiente = {}
        self.sinaisVitais = []
        self.loadAmbiente()
        self.loadSinaisVitais()


    def loadAmbiente(self):
        with open(self.pathAmbiente, "r") as file:
            for line in file:
                line = line.replace("\n", "")
                parameter, *variables = line.split(" ")

                variable = None

                if parameter == "Te" or parameter == "Ts" or parameter == "Xmax" or parameter == "Ymax":
                    variable = int(variables[0])

                elif parameter == "Base":
                    x, y = variables[0].split(",")
                    variable = [int(x), int(y)]

                elif parameter == "Vitimas" or parameter == "Paredes":
                    variable = []
                    for position in variables:
                        x, y = position.split(",")
                        variable.append([int(x), int(y)])

                else:
                    raise Exception("Parâmetro inválido")

                self.ambiente[parameter] = variable
        print(self.ambiente)

    def loadSinaisVitais(self):
        with open(self.pathSinaisVitais, "r") as file:
            for line in file:
                line = line.replace("\n", "").split(" ")
                variables = [float(x) if i>0 else int(x) for i,x in enumerate(line)]

                self.sinaisVitais.append(variables)
        print(self.sinaisVitais)

    def getTe(self):
        return self.ambiente["Te"]

    def getTs(self):
        return self.ambiente["Ts"]

    def getBase(self):
        return self.ambiente["Base"]

    def getXMax(self):
        return self.ambiente["Xmax"]

    def getYMax(self):
        return self.ambiente["Ymax"]

    def getVitimas(self):
        return self.ambiente["Vitimas"]

    def getParedes(self):
        return self.ambiente["Paredes"]

    def getSinaisVitais(self, vitima):
        return self.sinaisVitais[vitima]

    
