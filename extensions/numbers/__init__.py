import discord
import os
from discord.ext import commands


def centena(num):
    string = ''
    if num == '100':
        return 'cem'
    c = int(num[0])
    d = int(num[1])
    u = int(num[2])
    cen = ['',
           'cento',
           'duzentos',
           'trezentos',
           'quatrocentos',
           'quinhentos',
           'seiscentos',
           'setecentos',
           'oitocentos',
           'novecentos']
    dez = ['',
           ['dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis', 'dezesete', 'dezoito', 'dezenove'],
           'vinte',
           'trinta',
           'quarenta',
           'cinquenta',
           'sessenta',
           'setenta',
           'oitenta',
           'noventa']
    uni = ['',
           'um',
           'dois',
           'três',
           'quatro',
           'cinco',
           'seis',
           'sete',
           'oito',
           'nove']
    string += cen[c]
    if string != '' and (d != 0 or u != 0):
        string += ' e '
    if d != 1:
        if d != 0:
            string += dez[d]
            if u != 0:
                string += ' e '
                string += uni[u]
        else:
            string += uni[u]
    else:
        string += dez[1][u]
    return string


def retornaLhao(lhao, plural):
    string = ''
    ilhao = int(lhao)  # Para garantir a "inteiricidade" de lhão
    slhao = str(lhao)  # Para garantir a "stringuicidade" de lhão
    if ilhao in range(1, 11):
        lista = ['',
                 'mi',
                 'bi',
                 'tri',
                 'quadri',
                 'quinti',
                 'sexti',
                 'septi',
                 'octi',
                 'noni',
                 'deci']
        string = lista[ilhao]
    else:
        if len(slhao) < 3:
            slhao = formataTrinca(slhao)
        u = int(slhao[2])
        d = int(slhao[1])
        c = int(slhao[0])
        uni = ['', 'un', 'duo', 'tre', 'quattuor', 'quin', 'sex', 'septen', 'octo', 'noven']
        dez = ['', 'deci', 'viginti', 'triginti', 'quadraginti', 'quinquaginti', 'sexaginti',
               'septuaginti', 'octoginti', 'nonaginti']
        cen = ['', 'centi', 'ducenti', 'trescenti', 'quadrigenti', 'quingenti', 'sescenti',
               'septingenti', 'octingenti', 'nongenti']
        string += uni[u]
        if c == 0:
            string += dez[d]
        elif d == 0:
            string += cen[c]
        else:
            aux = dez[d]
            ni = aux.rfind('i')
            string += aux[0:ni] + 'a'
            string += cen[c]
    if plural:
        string += 'lhões'
    else:
        string += 'lhão'
    return string


def formataTrinca(trinca):
    inteiro = False
    if type(trinca) is int:
        trinca = str(trinca)
        inteiro = True
    if len(trinca) == 2:
        trinca += '0'
    else:
        trinca += '00'
    trinca = trinca[::-1]
    if not inteiro:
        return trinca
    else:
        return int(trinca)


def por_extenso(num):
    string = ''
    y = str(num)
    tamanho = len(y)
    i = tamanho
    divisivel = tamanho % 3
    listaS = []
    while True:
        if i > 0:
            trinca = y[i-3:i]
            #trinca = trinca[::-1]
            listaS.append(trinca)
            i -= 3
        elif divisivel != 0:
            listaS.remove('')
            trinca = y[0:3+i]
            trinca = trinca[::-1]
            listaS.append(trinca)

            break
        else:
            break
    tamanho = len(listaS)
    # ajeita para que todos elementos da lista tenham tamanho 3
    if len(listaS[tamanho - 1]) < 3:
        teste = listaS[tamanho - 1]
        if len(teste) == 2:
            teste += '0'
        else:
            teste += '00'
        teste = teste[::-1]
        listaS[tamanho - 1] = teste
    lista = listaS[::-1]
    i = tamanho
    for trinca in lista:
        plural = True
        if trinca == '001':
            plural = False
        strinca = centena(trinca)
        if strinca != '':
            if i != 2:
                string += strinca
            if i >= 3:
                string += f' {retornaLhao(i-2, plural)} '
            elif i == 2:
                if trinca != '001':
                    string += strinca + ' '
                string += 'mil '
        i -= 1

    return string


path = os.path.realpath('monopoly.py')
path = path[0:path.rfind('/')]
pastaProjeto = path


class Numeros(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Eventos
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog numeros está pronta')

    # Comandos
    @commands.command()
    async def extenso(self, ctx, *, param):
        global pastaProjeto
        param.strip()
        param = param.split(' ')
        if len(param) > 1:
            await ctx.send(f'O número tem que ser colado!')
        else:
            try:
                num = int(param[0])
            except:
                await ctx.send(f'O parâmetro não é um número inteiro válido!')
                return
            string = por_extenso(num)
            if len(string) < 2000:
                await ctx.send(string)
            else:
                path = pastaProjeto + '/txt/numeros/temp.txt'
                a = open(path, 'wt+')
                a.write(string)
                a.close()
                file = discord.File(path, filename='temp.txt')
                await ctx.send(file=file)


def setup(client):
    client.add_cog(Numeros(client))
