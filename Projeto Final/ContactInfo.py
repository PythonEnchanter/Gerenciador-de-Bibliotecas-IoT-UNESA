class cellphoneNumber:
    def __init__(self, cellphoneNumber):
        self.cellphoneNumber = int(str(cellphoneNumber)[2:])
        self.ddd = int(str(cellphoneNumber)[:2])

        full_number = f"({self.ddd}) {self.cellphoneNumber}"

    def getDDD(self):
        return self.ddd

    def getCellphoneNumber(self):
        return self.cellphoneNumber

    def ligar(self):
        #faz uma ligação para o número em questão
        pass

    def sms(self, mensagem):
        #envia a mensagem por sms
        pass

    def whatsapp_msg(self, message):
        #envia a mensagem por whatsapp
        pass

class enderecoEmail:
    def __init__(self, email):
        self.email = email

    def mala_direta(self, mensagem):
        #nvia a mensagem por email
        pass