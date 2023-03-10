import os
import sys
import speech_recognition as sr
import webbrowser as browser
import urllib.request
import json
import requests
from gtts import gTTS
from playsound import playsound
from datetime import datetime
from bs4 import BeautifulSoup
from requests import get
from translate import Translator


def cria_audio(audio, mensagem, lang='pt-br'):
    tts = gTTS(mensagem, lang=lang)
    tts.save(audio)
    playsound(audio)
    os.remove(audio)


def monitora_audio():
    recon = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print('Diga algo, estou te ouvindo')
            audio = recon.listen(source)
            try:
                mensagem = recon.recognize_google(audio, language='pt-br')
                mensagem = mensagem.lower()
                print('Você disse', mensagem)
                executa_comandos(mensagem)
                break
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
        return mensagem


def noticias():
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:5]:
        mensagem = item.title.text


def cotacao(moeda):
    requisicao = get(f'https://economia.awesomeapi.com.br/all/{moeda}-BRL')
    cotacao = requisicao.json()
    nome = cotacao[moeda]['name']
    data = cotacao[moeda]['create_date']
    valor = cotacao[moeda]['bid']
    cria_audio("cotacao.mp3", f"Cotação do {nome} em {data} é {valor}")


def filmes():
    token = "b53a4a821987202115204cfd1446daff"
    url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key={token}'
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    filmes = jsondata = json.loads(dados)['results']
    for filme in filmes[:5]:
        cria_audio("filmes.mp3", filme['title'], lang='en')


def clima(cidade):
    token = "3fe9143650b2adfae08da60ece18ce2d"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + token + "&q=" + cidade
    response = requests.get(complete_url)
    retorno = response.json()
    if retorno["cod"] == 200:
        valor = retorno["main"]
        current_temperature = valor["temp"]
        current_humidiy = valor["humidity"]
        tempo = retorno["weather"]
        weather_description = tempo[0]["description"]
        clima = (
            f"Em {cidade} a temperatura é de {str(int(current_temperature - 273.15))} graus celcius e humidade de {str(current_humidiy)} %")
        cria_audio("clima.mp3", clima)
    else:
        cria_audio(
            "erro.mp3", "Infelizmente não entendi, pode repetir por favor?")


def tradutor(traducao):
    if traducao == 'inglês':
        traduz = Translator(from_lang="pt-br", to_lang='english')
        cria_audio("traducao.mp3",
                   "O que você gostaria de traduzir para o inglês?")
        mensagem = monitora_audio()
        traduzido = traduz.translate(mensagem)
        cria_audio("traducao.mp3", f"A tradução de {mensagem} é")
        cria_audio("traducao_eng.mp3", traduzido, lang='en')
    elif traducao == 'português':
        traduz = Translator(from_lang="english", to_lang='pt-br')
        cria_audio("traducao.mp3",
                   "O que você gostaria de traduzir para o português?")
        mensagem = monitora_audio()
        traduzido = traduz.translate(mensagem)
        cria_audio("traducao.mp3", f"A tradução de")
        cria_audio("traducao_eng.mp3", mensagem, lang='en')
        cria_audio('traducao_port.mp3', f"é {traduzido}")


def executa_comandos(mensagem):

    # fechar assistente
    if 'fechar assistente' in mensagem:
        sys.exit()

    # hora atual
    elif 'horas' in mensagem:
        hora = datetime.now().strftime('%H:%M')
        frase = f"Agora são {hora}"
        cria_audio('horas.mp3', frase)

    # desligar o computador
    elif 'desligar computador' in mensagem and 'uma hora' in mensagem:
        os.system("shutdown -s -t 3600")
    elif 'desligar computador' in mensagem and 'meia hora' in mensagem:
        os.system("shutdown -s -t 1800")
    elif 'cancelar desligamento' in mensagem:
        os.system("shutdown -a")

    # pesquisa no google
    elif 'pesquisar' in mensagem and 'google' in mensagem:
        mensagem = mensagem.replace('pesquisar', '')
        mensagem = mensagem.replace('google', '')
        browser.open(f'https://google.com/search?q={mensagem}')

    # pesquisa no youtube
    elif 'pesquisar' in mensagem and 'youtube' in mensagem:
        mensagem = mensagem.replace('pesquisar', '')
        mensagem = mensagem.replace('youtube', '')
        browser.open(f'https://youtube.com/results?search_query={mensagem}')

    # spotify
    elif 'melhor' in mensagem and 'música' in mensagem:
        browser.open(
            'https://open.spotify.com/track/4qDT0BeJ7BjatrN9k8AvB4?si=3edaa18283464437')
    elif 'melhor' in mensagem and 'álbum' in mensagem:
        browser.open(
            'https://open.spotify.com/playlist/7BfGVZi5trQ8eAUNE8kM58?si=ed3e679f7d97493c')

    # notícias
    elif 'notícias' in mensagem:
        noticias()

    # cotação de moedas
    elif 'dólar' in mensagem:
        cotacao('USD')
    elif 'euro' in mensagem:
        cotacao('EUR')
    elif 'bitcoin' in mensagem:
        cotacao('BTC')

    # filmes
    elif 'filmes' in mensagem and 'populares' in mensagem:
        filmes()

    # clima
    elif 'clima' in mensagem:
        mensagem = mensagem.replace('clima', '')
        mensagem = mensagem.replace('em', '')
        clima(mensagem[2:])
    elif 'temperatura' in mensagem:
        mensagem = mensagem.replace('temperatura', '')
        mensagem = mensagem.replace('em', '')
        clima(mensagem[2:])

    # abrir programas do computador
    elif 'abrir' in mensagem and 'google chrome' in mensagem:
        os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")

    # tradutor
    elif 'traduzir' in mensagem and 'inglês' in mensagem:
        tradutor('inglês')
    elif 'traduzir' in mensagem and 'português' in mensagem:
        tradutor('português')

    # data
    elif 'data' in mensagem:
        ano = str(datetime.now().year)
        mes = str(datetime.now().month)
        dia = str(datetime.now().day)
        frase = ("Hoje é dia " + dia + "Do" + mes + "De" + ano)
        cria_audio('horas.mp3', frase)

    else:
        cria_audio(
            "erro.mp3", "Infelizmente não entendi, pode repetir por favor?")


def main():
    cria_audio(
        "ola.mp3", "Olá sou a Ana, sua assistente virtual! Como posso ajudar?")
    while True:
        monitora_audio()


main()
