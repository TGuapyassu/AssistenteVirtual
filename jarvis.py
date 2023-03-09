import pyttsx3
import datetime
import speech_recognition as sr

maquina = pyttsx3.init()


def falar(audio):
    voices = maquina.getProperty('voices')
    maquina.setProperty('voice', voices[0].id)
    maquina.say(audio)
    maquina.runAndWait()


def tempo():
    Tempo = datetime.datetime.now().strftime("%H:%M")
    falar("São " + Tempo)


def data():
    ano = str(datetime.datetime.now().year)
    mes = str(datetime.datetime.now().month)
    dia = str(datetime.datetime.now().day)
    falar("Hoje é dia " + dia + "Do" + mes + "De" + ano)


def bem_vindo():
    hora = datetime.datetime.now().hour
    if hora >= 6 and hora < 12:
        falar('Bom dia Tiago!')
    elif hora >= 12 and hora < 18:
        falar('Boa Tarde Tiago!')
    elif hora >= 18 and hora <= 24:
        falar('Boa Noite Tiago!')
    else:
        falar('Bom dia Tiago!')

    tempo()
    data()
    falar("Como posso ajudar Hoje?")


def microfone():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language='pt-BR')
        print(comando)

    except Exception as e:
        print(e)
        falar('Não Entendi, Repita Por Favor')

        return 'None'
    return comando


if __name__ == "__main__":
    bem_vindo()

    while True:
        print('Escutando...')
        comando = microfone().lower()

        if 'hora' in comando:
            tempo()

        elif 'data' in comando:
            data()

        else:
            falar('Não Entendi, Repita Por favor!')
