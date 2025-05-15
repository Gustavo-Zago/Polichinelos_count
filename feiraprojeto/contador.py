import cv2
import mediapipe as mp
import math
import PySimpleGUI as sg
import mysql.connector
import time

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
        print('Erro ao conectar ao banco de dados')
    return None

class TelaPython:
    def __init__(self, conexao):
        self.conexao = conexao

        screen_width, screen_height = sg.Window.get_screen_size()

        # Paleta de cores suaves "TanBlue"
        sg.theme('TanBlue')
        # Layout
        layout = [
            [sg.Text('', size=(30, 1))],  # Espaço em branco para centralizar verticalmente
            [sg.Text('Dados Usuario', size=(30, 1), justification='center', font=('Helvetica', 40), background_color='lightgray')],
            [sg.Text('', size=(30, 10))],  # Espaço em branco para centralizar verticalmente
            [sg.Text('', size=(5, 1)), sg.Text('Nome:', justification='center', size=(15, 1), font=('Helvetica', 20), background_color='lightgray'), sg.Input(size=(40, 1), key='Nome')],
            [sg.Text('', size=(20, 1))],  # Espaço em branco para centralizar verticalmente
            [sg.Button('Enviar', size=(20, 1), button_color=('white', 'green'))]  # Cor do botão verde
        ]

        # Crie a janela com tamanho total
        self.janela = sg.Window("Dados Usuario", layout=layout, element_justification='c', size=(screen_width, screen_height))

    def iniciar(self):
        evento, valores = self.janela.read()
        if evento == 'Enviar':
            global nome
            nome = valores['Nome']
            print(f'Nome: {nome}')

if __name__ == "__main__":
    conexao = conectar_ao_banco()
    if conexao:
        tela = TelaPython(conexao)
        tela.iniciar()

# Configuração do vídeo
video_width, video_height = 1366, 768
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
video.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)

pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.3, min_detection_confidence=0.3)
draw = mp.solutions.drawing_utils
cont = 0
check = True
point_counted = False  # Flag para controlar se um ponto já foi contabilizado

# Crie uma janela OpenCV em tela cheia
cv2.namedWindow("Polichinelos", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Polichinelos", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

tempo_desejado = 30

# Obtenha o tempo de início
tempo_inicio = time.time()
while True:
    success, img = video.read()
    if not success:
        print("O vídeo chegou ao fim ou não pode ser aberto.")
        break  # Saia do loop se o vídeo terminar ou não puder ser aberto

    videoRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Pose.process(videoRGB)

    # Verifique se results.pose_landmarks não é None antes de acessar a propriedade 'landmark'
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark 

        h, w, _ = img.shape
        pdy = (landmarks[pose.PoseLandmark.RIGHT_FOOT_INDEX].y * h)
        pdx = (landmarks[pose.PoseLandmark.RIGHT_FOOT_INDEX].x * w)
        pey = (landmarks[pose.PoseLandmark.LEFT_FOOT_INDEX].y * h)
        pex = (landmarks[pose.PoseLandmark.LEFT_FOOT_INDEX].x * w)
        mdy = (landmarks[pose.PoseLandmark.RIGHT_INDEX].y * h)
        mdx = (landmarks[pose.PoseLandmark.RIGHT_INDEX].x * w)
        mey = (landmarks[pose.PoseLandmark.LEFT_INDEX].y * h)
        mex = (landmarks[pose.PoseLandmark.LEFT_INDEX].x * w)

        distm = math.hypot(mdx - mex, mdy - mey)
        distp = math.hypot(pdx - pex, pdy - pey)


        if distm <= 150 and distp >= 150 and not point_counted: 
            print("contou")
            cont += 1
            point_counted = True

        if distm > 150 and distp < 150:
            point_counted = False
        texto = f'QTD:{cont}'
        cv2.putText(img, texto, (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        
        # Calculate elapsed time
        tempo_decorrido = time.time() - tempo_inicio
        minutos = int(tempo_decorrido // 60)
        segundos = int(tempo_decorrido % 60)
        texto_tempo = f'T:{minutos:02d}:{segundos:02d}'  # Formato T:MM:SS
        cv2.putText(img, texto_tempo, (40, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)


    cv2.imshow('Polichinelos', img)
    key = cv2.waitKey(1)
    if tempo_decorrido >= tempo_desejado or key == 27:
        break

# Encerre a captura de vídeo e feche a janela
video.release()
cv2.destroyAllWindows()
print(f'CONTADOR:{cont}')

def iniciar(conexao, cont):
    try:
        if conexao:
            comandosql = conexao.cursor()
            comandosql.execute(f'SELECT id FROM Usuarios WHERE nome = "{nome.upper()}";')
            resultado = comandosql.fetchone()
            resultado = str(resultado).replace(",","")
            resultado = str(resultado).replace("(","")
            resultado = str(resultado).replace(")","")
            print(f'ID:{resultado}')
            comandosql.execute(f'SELECT COUNT(*) FROM polichinelo WHERE idusuario = "{int(resultado)}";')
            contsalt = comandosql.fetchone()
            contsalt = str(contsalt).replace(",","")
            contsalt = str(contsalt).replace("(","")
            contsalt = str(contsalt).replace(")","")
            contsalt = int(contsalt)
            if(contsalt < 1):
                comandosql.execute(f'INSERT INTO polichinelo(idusuario, contpol) values({int(resultado)}, {cont});')
                conexao.commit()
            else:
                comandosql.execute(f'select contpol from polichinelo where idusuario = "{int(resultado)}" ')
                v1 = comandosql.fetchone()
                v1 = str(v1).replace(",","")
                v1 = str(v1).replace("(","")
                v1 = str(v1).replace(")","")
                if(int(v1) >= cont):
                    comandosql.execute(f'UPDATE polichinelo SET contpol = {int(v1)} WHERE idusuario = "{int(resultado)}";')
                    conexao.commit()
                else:
                    comandosql.execute(f'UPDATE polichinelo SET contpol = {cont} WHERE idusuario = "{int(resultado)}";')
                    conexao.commit()

    except Exception as erro:
        print('Erro ao inserir dados no banco')

if __name__ == "__main__":
    conexao = conectar_ao_banco()
    if conexao:
        iniciar(conexao, cont)
        conexao.close()

    sg.theme('TanBlue')  # Define o tema
    layout = [
        [sg.Text(f'Parabéns, {nome.upper()}, pela sua pontuação de: {cont} polichinelos', font=('Helvetica', 20))],
        [sg.Button('OK')]
    ]

    janela_mensagem = sg.Window('Pontuação', layout, element_justification='c')

    while True:
        evento, valores = janela_mensagem.read()
        if evento == sg.WIN_CLOSED or evento == 'OK':
            break

        janela_mensagem.close()
