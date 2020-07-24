import requests
import re
import sys
import os
import threading
import urllib.request

def procura_anime (nome):

    html= requests.get("https://goyabu.com/?s="+ nome).text
    html= html.replace("\n", "")
    # print(html)

    return re.findall('''<div class="video-data"> <h4 class="video-title"><a href="(.*?)" title=.*?>(.*?)<\/a''', html)

def seleciona_anime (lista):
    os.system("cls")
    print("animes encontrados:\n")
    i=0
    for anime in lista:
        print("["+str(i)+"] =>"+anime[1])
        i+=1

    selecionado = int(input("selecione o seu anime: "))

    return lista[selecionado]

def pagina_anime (anime):    
    html = requests.get(anime[0]).text #anime[0]=link \\\ anime[1]= nome do anime
    html = html.replace("\n", "")
    
    
    links = re.findall('''<div class="video-data"><h4 class="video-title"><a href="(.*?)"''', html)

    print("numero de episódios: " + str(len(links)))

    n_inicial = int(input("numero inicial para começar a baixar: ")) -1
    n_final = int(input("numero final para começar a baixar: ")) #rever

    retorno = []
    i = n_inicial
    for l in links[n_inicial:n_final]:
        inserir = []
        inserir.append(l)
        inserir.append(i+1)
        retorno.append(inserir)
        i+=1

    return retorno

def THREADS (link, numero,anime):
    anime = anime.replace(":", "_")
    anime = anime.replace("/", "_")

    comando = '''powershell -Command "Invoke-WebRequest -Uri '''+link +''' -OutFile htmls\\''' + str(numero) +'''.html'''
    os.system(comando)
    try:
        arq = open("htmls\\"+str(numero)+".html", "r", encoding="utf8")
        leitura = arq.read().encode("UTF-8")
        arq.close()
    except erro:
        print(erro)
    

    leitura = str(leitura).replace("\n","")
    # link = re.findall('''{type: "video\/mp4", label: "SD", file: "(.*?)"''', leitura)
    link = re.findall('''file: "(.*?)"},],type: "video\/mp4"''', leitura)
    link = str(link[0])
    

    if link.find("file:") != -1:
        link = re.findall('''file:\s"(.*?)$''', link)
        link = str(link[0])
        print("arrumou")


    comando = '''mkdir videos\\"'''+ anime + '"'
    os.system(comando)

    urllib.request.urlretrieve(link, 'videos\\'+anime+'\\'+str(numero)+ '.mp4')

    print("fim" + str(numero))

def instanciar_threads(links, anime):
    threads = []

    for l in links:     
        t = threading.Thread(target=THREADS, args=(l[0],l[1],anime,))
        threads.append(t)

    for i in threads:
        i.start()

    for i in threads:
        i.join()

    print("fim")

def main (anime):
    anime = str(anime)
    os.system("cls")

    print("procurando anime: " + anime)

    lista_animes_encontrados = procura_anime(anime)
    anime_escolhido          = seleciona_anime(lista_animes_encontrados)
    links_downloads          = pagina_anime(anime_escolhido)
    instanciar_threads(links_downloads, anime_escolhido[1])
   


main(sys.argv[1])