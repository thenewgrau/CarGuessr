import os
import sys
import json
import random
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
telaPrincipalUI = os.path.join(BASE_DIR, "..", "design", "telaPrincipal.ui")
carGuesserUI = os.path.join(BASE_DIR, "..", "design", "CarGuesser.ui")


class TelaPrincipal(QMainWindow):
    def __init__(self, tela_anterior):
        super().__init__()
        loadUi(telaPrincipalUI, self)

        self.tela_anterior = tela_anterior
        self.voltar.clicked.connect(self.voltarTelaInicial)
        self.pushDica.clicked.connect(self.mostrarDica)
        self.confirmar.clicked.connect(self.tentativaDoRuim)
        self.desistir.clicked.connect(self.desistirImediatamente)
        self.carroAtual = None

        self.dica_index = 0
        self.tentativa = 1
        self.novoCarro()

    def carregarCarros(self):
        caminhoArquivo = os.path.join(BASE_DIR, "..", "db", "dadosCarGuessr.json")
        
        try:
            with open(caminhoArquivo, 'r') as f:
                dados = json.load(f)
                # for carro in dados:
                #     print(f"Nome: {carro['modelo']}")
                #     print(f"Ano: {carro['ano']}")
                #     print(f"Motor: {carro['motor']}")
                #     print(f"Potência: {carro['potencia']}")
                #     print(f"Tração: {carro['tracao']}")
                #     print(f"Imagem: {carro['imagem']}")
                #     print("-" * 40)
                    
                return dados                
            
        except FileNotFoundError:
            print("Arquivo JSON não encontrado.")
            return []

    def buscarCarroAleatorio(self):
        carros = self.carregarCarros()
        if carros:
            carroAtual = random.choice(carros)
            print(carroAtual)
            print('-'*100)
            return carroAtual
        return None

    
    def novoCarro(self):
        self.anoLabel.setText("")
        self.motorLabel.setText("")
        self.potenciaLabel.setText("")
        self.tracaoLabel.setText("")
        self.labelAcabouDicas.setText("")
        self.inputCarro.clear()
        self.dica_index = 0

        self.carroAtual = self.buscarCarroAleatorio()

        if self.carroAtual:
            caminho_imagem = self.carroAtual['imagem']
            caminho_imagem_absoluto = os.path.join(BASE_DIR, caminho_imagem)
            pixmap = QPixmap(caminho_imagem_absoluto)
            
            if not pixmap.isNull():
                self.imagemCarro.setPixmap(pixmap)
                self.imagemCarro.setScaledContents(True)
            else:
                print(f"Erro ao carregar a imagem de carro: {caminho_imagem_absoluto}")
        else:
            print("Não foi possível carregar o carro.")

    def mostrarDica(self):
        if self.dica_index == 0:
            self.anoLabel.setText(f"🗓️ Ano: {self.carroAtual['ano']}")
        elif self.dica_index == 1:
            self.motorLabel.setText(f"🔧 Motor: {self.carroAtual['motor']}L")
        elif self.dica_index == 2:
            self.potenciaLabel.setText(f"🚀 Potência: {self.carroAtual['potencia']} CV")
        elif self.dica_index == 3:
            self.tracaoLabel.setText(f"🚗 Tração: {self.carroAtual['tracao']}")
        else:
            self.labelAcabouDicas.setText("😅 Sem mais dicas...")

        self.dica_index += 1

    def tentativaDoRuim(self):
        tentativa = self.inputCarro.text()
        print(tentativa)
        if tentativa == self.carroAtual['modelo']:
            print("acertou")
            self.acertouErrou.setText('ACERTOUUUU !!!') 
            time.sleep(2)
            self.tentativa = 1
            self.buscarCarroAleatorio()
            self.novoCarro()
        
        elif tentativa == '':
            self.tentativas.setText('Escreva algo!')
            self.acertouErrou.setText('Nem tentou...')

        elif tentativa != '' and tentativa != self.carroAtual['modelo']:
            self.tentativas.setText(f"Tentativas: {self.tentativa}")    
            self.tentativa += 1
            print('errou')
            self.acertouErrou.setText('Errou...')

    def desistirImediatamente(self):
        print(f"o carro passado era: {self.carroAtual['modelo']}")
        self.buscarCarroAleatorio()
        self.novoCarro()

    def voltarTelaInicial(self):
        self.hide()
        self.tela_anterior.show()

class CarGuesser(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(carGuesserUI, self)

        self.botaoJogar.clicked.connect(self.abrir_tela_principal)

    def abrir_tela_principal(self):
        self.hide()
        self.tela_principal = TelaPrincipal(self)
        self.tela_principal.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarGuesser() 
    window.show()
    sys.exit(app.exec_())
