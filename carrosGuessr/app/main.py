import os
import sys
import json
import random
from PyQt5.QtCore import QTimer
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

        self.todos_os_carros = self.carregarCarros()
        self.carros_disponiveis = []
        self.resetar_carros()

        self.carroAtual = None
        self.dica_index = 0
        self.tentativa = 1

        self.novoCarro()

    def carregarCarros(self):
        caminhoArquivo = os.path.join(BASE_DIR, "..", "db", "dadosCarGuessr.json")
        try:
            with open(caminhoArquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                print(f"Dados carregados: {type(dados)}")
                if isinstance(dados, dict) and 'carros' in dados:
                    print(f"Carros encontrados: {len(dados['carros'])}")
                    return dados['carros']
                elif isinstance(dados, list):
                    print(f"Lista de carros carregada: {len(dados)}")
                    return dados
                else:
                    print("Formato inesperado! Retornando lista vazia.")
                    return []
        except Exception as e:
            print(f"Erro carregando JSON: {e}")
            return []

    def resetar_carros(self):
        self.carros_disponiveis = self.todos_os_carros.copy()
        random.shuffle(self.carros_disponiveis)
        print(f"Total de carros disponíveis: {len(self.carros_disponiveis)}")

    def buscarCarroAleatorio(self):
        if not self.carros_disponiveis:
            print("Todos os carros foram usados! Resetando lista...")
            self.resetar_carros()
        return self.carros_disponiveis.pop()

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
            caminho_imagem = os.path.join(BASE_DIR, self.carroAtual['imagem'])
            pixmap = QPixmap(caminho_imagem)
            if not pixmap.isNull():
                self.imagemCarro.setPixmap(pixmap)
                self.imagemCarro.setScaledContents(True)
            else:
                print(f"Erro ao carregar imagem: {caminho_imagem}")
        else:
            print("Não foi possível carregar carro.")

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
        if tentativa == self.carroAtual['modelo']:
            self.acertouErrou.setText('ACERTOUUUU !!!')
            QTimer.singleShot(2000, self.prepararNovoCarro)
        elif tentativa == '':
            self.tentativas.setText('Escreva algo!')
            self.acertouErrou.setText('Nem tentou...')
            QTimer.singleShot(2000, lambda: self.acertouErrou.setText(''))
        else:
            self.tentativas.setText(f"Tentativas: {self.tentativa}")
            self.acertouErrou.setText('Errou...')
            QTimer.singleShot(2000, lambda: self.acertouErrou.setText(''))
            self.tentativa += 1

    def prepararNovoCarro(self):
        self.tentativa = 1
        self.acertouErrou.setText('')
        self.novoCarro()

    def desistirImediatamente(self):
        print(f"O carro era: {self.carroAtual['modelo']}")
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
