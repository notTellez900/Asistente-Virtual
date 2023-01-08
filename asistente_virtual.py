import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

"""
Descargar voces: 
https://support.microsoft.com/es-es/topic/descargar-idiomas-y-voces-para-lector-inmersivo-el-modo-lectura-y-lectura-en-voz-alta-4c83a8d8-7486-42f7-8e46-2b0fdf753130
"""

"""
# Visualizar las voces que tengas instaladas en el PC
    engine = pyttsx3.init()
    for voz in engine.getProperty('voices'):
        print(voz)
"""


# Escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # Almacenar el recognizer en una variable
    recog = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:

        # Tiempo espera antes de que empiece a escuchar
        recog.pause_threshold = 0.8

        # Informar que comenzo la grabación
        print("Ya puedes hablar")

        # Guardar lo que escuche como audio
        audio = recog.listen(origen)

        try:
            # Buscar en google lo que se haya escuchado
            pedido = recog.recognize_google(audio, language="es_co")
            # Prueba de que pudo ingresar
            print('Dijiste: ' + pedido)
            # devolver pedido
            return pedido
        # en caso de que no comprenda lo dicho
        except sr.UnknownValueError:
            # Prueba de que no comprendió el audio
            print('Ups, no entendí')
            # Devolver error
            return "Sigo esperando"
        # En caso de no resolver el pedido
        except sr.RequestError:
            # Prueba de que no comprendió el audio
            print('Ups, no hay servicio')
            # Devolver error
            return "Sigo esperando"
        # Error inesperado
        except:
            # Prueba de que no comprendió el audio
            print('Ups, algo ha salido mal')
            # Devolver error
            return "Sigo esperando"


# Id de las voces que tienes instaladas / idiomas
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar el dia de la semana
def pedir_dia():
    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear una variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario de los nombres dias
    calendario = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }

    # Decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# Informar hora
def pedir_hora():
    # Crear variable condatos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos'
    print(hora)
    # Decir la hora
    hablar(hora)


# Saludo inicial
def saludo_inicial():
    # Identificar si es dia, tarde o noche
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 18:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'
    # Decir el saludo
    hablar(f'{momento}, soy Elena, tu asistinte personal. Por favor, dime en que te puedo ayudar.')


# Funcion central del asistente
def pedir_cosas():
    # Activar el saludo inicial
    saludo_inicial()

    # Siga siempre esperando a que pidamos cosas
    comenzar = True

    while comenzar:
        # Activar el microfono y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en ello')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            # Establecer el lenguaje
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {
                'apple': 'APPL',
                'amazon': 'AMZN',
                'google': 'GOOGL'
            }
            try:
                accion_buscada = cartera[accion]
                # Buscar el Ticker que haya encontrado
                accion_buscada = yf.Ticker(accion_buscada)
                # Info trae un diccionario con muchos datos
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón pero no la he encontrado')
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break


pedir_cosas()
