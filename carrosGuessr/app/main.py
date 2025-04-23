import os
import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
telaPrincipalUI = os.path.join(BASE_DIR, "..", "design", "telaPrincipal.ui")
carGuesserUI = os.path.join(BASE_DIR, "..", "design", "CarGuesser.ui")

db_config = {
    "host": "localhost",  
    "user": "root",       
    "password": "",      
    "database": "carguessr" 
}

def conectar_banco():
    try:
        connection = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

class TelaPrincipal(QMainWindow):
    def __init__(self, tela_anterior):
        super().__init__()
        loadUi(telaPrincipalUI, self)

        self.tela_anterior = tela_anterior
        self.voltar.clicked.connect(self.voltarla)
        self.connection = conectar_banco()
        self.carro_atual = None

        self.confirmar.clicked.connect(self.verificar_palpite)
        self.desistir.clicked.connect(self.desistirAgora)
        self.pushDica.clicked.connect(self.mostrar_dica)

        self.dica_index = 0
        self.novo_carro()

    def novo_carro(self):
        self.anoLabel.setText("")
        self.motorLabel.setText("")
        self.potenciaLabel.setText("")
        self.tracaoLabel.setText("")
        self.inputCarro.clear()
        self.dica_index = 0


        self.carro_atual = self.buscar_carro_aleatorio()

        if self.carro_atual:
            caminho_imagem = self.carro_atual['imagem']
            print(f"Caminho da imagem: {caminho_imagem}")
            pixmap = QPixmap(caminho_imagem)
            self.imagemCarro.setPixmap(pixmap)
            self.imagemCarro.setScaledContents(True)
        else:
            self.labelDica.setText("Não foi possível carregar o carro.")

    def buscar_carro_aleatorio(self):
        if not self.connection:
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM carros LIMIT 1")
                carro = cursor.fetchone()

                if carro:
                    return {
                        "nome": carro[1],    
                        "ano": carro[2],       
                        "motor": carro[3],   
                        "tracao": carro[4],    
                        "potencia": carro[5],     
                        "imagem": carro[6]       
                    }
                else:
                    return None
        except pymysql.MySQLError as e:
            print(f"Erro ao buscar carro no banco de dados: {e}")
            return None

    def verificar_palpite(self):
        palpite = self.inputCarro.text().strip().lower()
        print(palpite)
        nome_correto = self.carro_atual["nome"].lower()

        if palpite == nome_correto:
            self.tentativas.setText("✅ Acertou! Próximo carro...")
            self.novo_carro()
        else:
            self.tentativas.setText("❌ Errou! Tente novamente ou peça uma dica.")

    def mostrar_dica(self):
        if self.dica_index == 0:
            self.anoLabel.setText(f"🗓️ Ano: {self.carro_atual['ano']}")
        elif self.dica_index == 1:
            self.motorLabel.setText(f"🔧 Motor: {self.carro_atual['motor']}L")
        elif self.dica_index == 2:
            self.potenciaLabel.setText(f"🚀 Potência: {self.carro_atual['potencia']} CV")
        elif self.dica_index == 3:
            self.tracaoLabel.setText(f"🚗 Tração: {self.carro_atual['tracao']}")
        else:
            self.tentativas.setText("😅 Sem mais dicas...")
        
        self.dica_index += 1

    def desistirAgora(self):
        self.labelDica.setText(f"🚗 Era: {self.carro_atual['nome']}. Vamos pro próximo!")
        self.novo_carro()

    def voltarla(self):
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
