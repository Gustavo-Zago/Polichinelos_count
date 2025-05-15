import PySimpleGUI as sg
import mysql.connector
import subprocess

def conectar_ao_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='feira',
            user='root',
            port='3307',
            password=''
        )
        if conexao.is_connected():
            return conexao
    except Exception as erro:
        print('Erro ao conectar ao banco de dados:', erro)
    return None

class TelaPython:
    def __init__(self, conexao):
        self.conexao = conexao

        # Obtenha as dimensões da tela
        screen_width, screen_height = sg.Window.get_screen_size()

        # Paleta de cores suaves "TanBlue"
        sg.theme('TanBlue')
        # Layout
        layout = [
            [sg.Text('', size=(30, 1))],  # Espaço em branco para centralizar verticalmente
            [sg.Text('Cadastro de Usuário', size=(30, 1), justification='center', font=('Helvetica', 40), background_color='lightgray')],
            [sg.Text('', size=(30, 10))],  # Espaço em branco para centralizar verticalmente
            [sg.Text('', size=(5, 1)), sg.Text('Nome:', justification='center', size=(15, 1), font=('Helvetica', 20), background_color='lightgray'), sg.Input(size=(40, 1), key='Nome')],
            [sg.Text('', size=(5, 1)), sg.Text('Instagram:', justification='center', size=(15, 1), font=('Helvetica', 20), background_color='lightgray'), sg.Input(size=(40, 1), key='Insta')],
            [sg.Text('', size=(20, 1))],  # Espaço em branco para centralizar verticalmente
            [sg.Button('Cadastrar', size=(20, 1), button_color=('white', 'green'))]  # Cor do botão verde
        ]

        # Crie a janela com tamanho total
        self.janela = sg.Window("Cadastro de Usuário", layout=layout, element_justification='c', size=(screen_width, screen_height))

    def iniciar(self):
        while True:
            verificacao = 0
            evento, valores = self.janela.read()
            if evento == sg.WIN_CLOSED:
                break
            if evento == 'Cadastrar':
                nome = valores['Nome'].strip().upper()
                insta = valores['Insta'].strip()
                if nome and insta:
                    try:
                        if self.conexao:
                            cursor = self.conexao.cursor()
                            cursor.execute('INSERT INTO Usuarios(nome, insta) VALUES (%s, %s)', (nome, insta))
                            self.conexao.commit()
                            sg.popup('Cadastro realizado com sucesso!', title='Sucesso', background_color='lightgreen')
                            verificacao = 1
                            if verificacao == 1:
                                subprocess.Popen(['python', 'contador.py'])
                            break  # Encerra o loop após o cadastro bem-sucedido
                    except mysql.connector.Error as erro:
                        print(f'Erro ao inserir dados no banco: {erro}')
                        sg.popup_error('Erro ao cadastrar usuário', title='Erro', background_color='lightcoral')
                else:
                    sg.popup_error('Preencha todos os campos', title='Erro', background_color='lightcoral')

if __name__ == "__main__":
    conexao = conectar_ao_banco()
    if conexao:
        tela = TelaPython(conexao)
        tela.iniciar()
        conexao.close()
