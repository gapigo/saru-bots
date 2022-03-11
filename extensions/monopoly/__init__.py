import random
import discord
import os
import math
from time import sleep
from operator import itemgetter
from discord.ext import commands
from PIL import Image, ImageOps

def inicializar():
    global quantoGanhaAoPassarNoInicio, dinheiroInicial, jogo, casas, atual, numJogadores, inicioJogada
    global mverifica, desistencia, finalizacao, idProximoAVotarFinalização, pastaProjeto, jogoRolando, desistente
    global desistentes, habilitarDevedor, ultimoAJogar, casaInicio, tempoDados, perdedores, escolhidas, vendaInfo
    global contaM, estacionamentoUnico, ultimoAReceberEstacionamento

    # para devs
    casaInicio = 0

    path = os.path.realpath('monopoly.py')
    path = path[0:path.rfind('/')]
    pastaProjeto = path

    inicializaCasas()
    quantoGanhaAoPassarNoInicio = 2  # 2M
    dinheiroInicial = 10.5           # 10.5 M Em Milhões
    tempoDados = 1.5

    jogo = dict()
    desistentes = dict()
    perdedores = dict()
    profile = dict()

    #  posse['Botinha'] = 0 // Número de casas em "botinha"
    for i in range(0, len(escolhidas)):
        ecor, enome, eid = escolhidas[i].split(',')
        '''
        profile['id'] = int(eid)
        profile['nome'] = enome
        profile['casa'] = 0
        profile['dinheiro'] = dinheiroInicial
        profile['totalganho'] = 0
        profile['hipotecados'] = []
        profile['posses'] = []
        cartoes = {'cadeia': False, 'estacionamento': False}
        profile['cartoes'] = cartoes'''
        jogo[f'{ecor}'] = {'id': int(eid),
                           'nome': enome,
                           'casa': casaInicio,
                           'dinheiro': dinheiroInicial,
                           'totalganho': 0,
                           'dado':0,
                           'hipotecados': [],
                           'posses': [],
                           'cartoes': {'cadeia': False,
                                       'estacionamento': False,
                                       'ender': False},
                           'comando': None,
                           'pcomando': '', # parâmetros de comando (quanto deve pagar)
                           'status': 'livre'}  # 'preso' quando está na cadeia
                                               # 'devedor' quando está devendo
                                               # 'devedor medio' quando está devendo mas pode hipotecar
                                               # 'devedor grave' quando está com dinheiro negativo
                                               # 'pagador' para quando ele já pagou a dívida
                                               # 'sorte' para "sorte do guardião e 'sorteq' para sorte quitada
                                               # 'caixa' para caixa lazarenta e 'caixaq' para caixa quitada
                                               # 'comprador' para não deixar o jogador que já comprou comprar novamente
                                               # 'vá para cadeia' para indicar que o jogador está preste a ir para cadeia se der '.m ok'
                                               # 'usou' para indicar que o jogador usou algum cartão
                                               # 'perdedor' para somente se o jogador perder o jogo na sorte ou caixa
                                               # 'escolhendo' para escolher a posse para deletar casas
                                               # 'oi' para verificar se o jogador escreveu .m oi ou se aceitou perder
        # PARA 'comando':
        # 'comando pagar' para pagamentos de caixa e sorte
        # 'comando jogar' para jogar de caixa e sorte
        # 'comando escolher 1' para escolher op 1 de caixa e sorte

    # Define o atual a jogar
    ecor, enome, eid = escolhidas[0].split(',')
    atual = [ecor, 0]

    imagemInicial()

    # players que respondem sim ou não em .m
    desistente = ''

    # players salvos na memória
    ultimoAJogar = ''
    ultimoAReceberEstacionamento = ''

    # tupla Venda info = (bool, string, float, int, string) = (verificador, cliente, valor, item, vendedor)
    vendaInfo = (False, '', 0, 0, '')

    # verificadores
    inicioJogada = True
    mverifica = False
    desistencia = False
    finalizacao = False
    jogoRolando = True
    idProximoAVotarFinalização = 0
    habilitarDevedor = False
    estacionamentoUnico = True

    # contador de quantos .m foram dados
    contaM = 0


def analisaNumJogadores(num):
        try:
            jogadores = int(num)
        except:
            return (False, 'Informação inválida! Digite um número inteiro de 2-4 para escolher o número de jogadores')
        else:
            if jogadores < 2 or jogadores > 4:
                return (False, 'Só podem jogar 2-4 jogadores!')
            else:
                return (True, f'Jogo setado para {jogadores} jogadores.')


def analisaCor(cor):
    global escolhidas
    while True:
        try:
            string = str(cor)
        except:
            return 'invalido'
        else:
            if cor in 'amarelovermelhoverdeazulbluegreenyellowredamarelavermelha':
                escolhidasString = ''
                for escolha in escolhidas:
                    corescolha, nome, id = escolha.split(',')
                    escolhidasString += corescolha
                if cor in escolhidasString:
                    return 'escolhida'
                else:
                    if cor.lower() in 'amareloyellowamarela':
                        return 'amarelo'
                    elif cor.lower() in 'vermelhovermelhared':
                        return 'vermelho'
                    elif cor.lower() in 'azulblue':
                        return 'azul'
                    elif cor.lower() in 'greenverde':
                        return 'verde'
            else:
                return 'invalido'


def analisaAcoes(jogador, inicio=False, dado=0):
    global jogo, casas, atual, habilitarDevedor, inicioJogada, estacionamentoUnico
    opcoes = []
    if inicioJogada is True:
        if jogador == atual[0]:
            opcoes.append('jogar')
    print('183', end=' ')
    casa = jogo[jogador]['casa']
    dinheiro = jogo[jogador]['dinheiro']
    dono = casas[casa][1]  # Dono recebe a string que indica o dono da casa
    tipo = casas[casa][2]
    # Verifica se não tem que quebrar o tipo da casa para realizar ordem de casa antiga
    if jogo[jogador]['comando'] is not None:
        if jogo[jogador]['comando'] == 'pagar1':
            tipo = 'sorte'
            if jogo[jogador]["status"] != 'pagador':
                jogo[jogador]['status'] = 'devedor'
    if dono is not None:
        preso = (jogo[dono]['status'] == 'preso')
    print('190', end=' ')
    if inicioJogada is False:
        if tipo == 'lote':  # Revela o tipo da casa
            print('193', end=' ')
            # Verifica se tem dono
            if casas[casa][1] is not None:  # Se a variável string de casas não está vazia (então há dono)
                # Verifica se o dono é o jogador
                if dono == jogador:
                    if casas[casa][3] < 5 and not (jogo[jogador]['status'] == 'comprador'):  # Se o lote não tiver hotel
                        if jogo[jogador] == 'devedor grave':
                            ""
                        else:
                            if dinheiro > casas[casa][4][1]:
                                comprar = ('comprar', casa, casas[casa][4][1], 'mais casas')
                                opcoes.append(comprar)
                # Verifica se o lote não está hipotecado
                elif casa not in jogo[dono]['hipotecados']:
                    # Verifica se o lote tem casas
                    if casas[casa][3] == 0:
                        tamanhoGrupo = len(casas[casa][5])  # Armazena o tamanho do grupo do lote, pode ser 2 ou 3
                        # Verifica se o aluguel padrão será dobrado ou não
                        numPosse1 = casas[casa][5][0]  # número da casa 1 do grupo
                        numPosse2 = casas[casa][5][1]  # número da casa 1 do grupo
                        verPosse1 = False  # variável que procura a posse da casa 1
                        verPosse2 = False  # variável que procura a posse da casa 2
                        if tamanhoGrupo == 3:
                            numPosse3 = casas[casa][5][2]
                            verPosse3 = False
                        aluguelDobrado = False  # variável que armazena se a condição do aluguel dobrado é válida
                        for posse in jogo[dono]['posses']:
                            if posse == numPosse1:
                                verPosse1 = True  # Se o dono tem a casa 1, é marcado True
                            if posse == numPosse2:
                                verPosse2 = True  # Se o dono tem a casa 2, é marcado True
                            if tamanhoGrupo == 3:  # Acontece somente se o tamanho do grupo for 3
                                if posse == numPosse3:
                                    verPosse3 = True
                                if verPosse1 and verPosse2 and verPosse3:
                                    aluguelDobrado = True
                                    break
                            else:
                                if verPosse1 and verPosse2:
                                    aluguelDobrado = True
                                    break
                        if aluguelDobrado:
                            if (jogo[jogador]["status"] != 'pagador') and not preso:
                                pagar = ('pagar', casas[casa][4][2] * 2, dono)
                                jogo[jogador]["status"] = 'devedor'
                                opcoes.append(pagar)
                        else:
                            if (jogo[jogador]["status"] != 'pagador') and not preso:
                                pagar = ('pagar', casas[casa][4][2], dono)
                                jogo[jogador]["status"] = 'devedor'
                                opcoes.append(pagar)
                    else:
                        if (jogo[jogador]["status"] != 'pagador') and not preso:
                            numCasas = casas[casa][3]  # Número de casas do lote
                            pagar = ('pagar', casas[casa][4][numCasas + 2], dono)
                            jogo[jogador]["status"] = 'devedor'
                            opcoes.append(pagar)
            # Se não tiver oferece
            elif not (jogo[jogador]['status'] == 'comprador'):
                if jogo[jogador] == 'devedor grave':
                    ""
                else:
                    if dinheiro > casas[casa][4][0]:
                        comprar = ('comprar', casa, casas[casa][4][0], 'posse')
                        opcoes.append(comprar)
        elif tipo == 'meme':
            print('259', end=' ')
            # Se não tiver dono
            if (casas[casa][1] is None) and not (jogo[jogador]['status'] == 'comprador'):
                if jogo[jogador] == 'devedor grave':
                    ""
                else:
                    if dinheiro > casas[casa][3]:
                        comprar = ('comprar', casa, casas[casa][3], 'posse')
                        opcoes.append(comprar)
            else:
                print('270', end=' ')
                if casas[casa][1] != jogador:
                    if jogo[jogador]["status"] != 'pagador':
                        dono = casas[casa][1]
                        contador = 0
                        # Conta quantos "MEMES" o jogador possui
                        for posse in jogo[dono]['posses']:
                            for i in range(0, 4):
                                if posse == casas[casa][4][i]:
                                    contador += 1
                        if contador != 0 and not preso:
                            valor = 0.25 * (2 ** (contador - 1))
                            pagar = ('pagar', valor, dono)
                            jogo[jogador]["status"] = 'devedor'
                            opcoes.append(pagar)
        elif tipo == 'caixa':
            print('290', end=' ')
            if jogo[jogador]['status'] == 'pagador':
                jogo[jogador]['comando'] = None
                jogo[jogador]['pcomando'] = None
            elif jogo[jogador]['status'] == 'caixaq':
                'nada'
            elif jogo[jogador]['status'] == 'escolhendo':
                opcoes.append('escolher')
            elif jogo[jogador]['comando'] is None:
                jogo[jogador]['status'] = 'caixa'
                opcoes.append('caixa')
            else:
                if jogo[jogador]['comando'] == 'pagar':
                    pagar = jogo[jogador]['pcomando']
                    opcoes.append(pagar)
                elif jogo[jogador]['comando'] == 'jogar':
                    opcoes.append('jogar')
                elif jogo[jogador]['comando'] == 'escolha':
                    opcoes.append('escolha')
        elif tipo == 'sorte':
            print('310', end=f' status = {jogo[jogador]["status"]} ')
            if jogo[jogador]['status'] == 'pagador':
                jogo[jogador]['comando'] = None
                jogo[jogador]['pcomando'] = None
                print('314', end=' ')
            elif jogo[jogador]['status'] == 'sorteq' or jogo[jogador]['status'] == 'pagador':
                print('316', end=' ')
            elif jogo[jogador]['status'] == 'escolhendo':
                opcoes.append('escolher')
                print('319', end=' ')
            elif jogo[jogador]['comando'] is None:
                jogo[jogador]['status'] = 'sorte'
                opcoes.append('sorte')
                print('323', end=' ')
            else:
                print('325', end=' ')
                if jogo[jogador]['comando'] in 'pagar1':
                    print('327', end=' ')
                    pagar = jogo[jogador]['pcomando']
                    jogo[jogador]['status'] = 'devedor'
                    opcoes.append(pagar)
                    print('331', end=' ')
                elif jogo[jogador]['comando'] == 'jogar':
                    pagar = jogo[jogador]['pcomando']
                    opcoes.append('pagar')
                elif jogo[jogador]['comando'] == 'escolha':
                    opcoes.append('escolha')
        elif tipo == 'monstro':
            #  Se a casa não tem dono e o jogador não comprou já naquela vez
            if (dono is None) and jogo[jogador]['status'] != 'comprador':
                if jogo[jogador]['status'] == 'devedor grave':
                    ""
                else:
                    if dinheiro > casas[casa][3]:
                        comprar = ('comprar', casa, casas[casa][3], 'posse')
                        opcoes.append(comprar)
            else:
                # Se o dono não é o jogador
                dado = jogo[jogador]["dado"]
                if dono != jogador:
                    if jogo[jogador]["status"] != 'pagador':
                        contador = 0
                        for posse in jogo[dono]['posses']:
                            for i in range(0, 2):
                                if posse == casas[casa][4][i]:
                                    contador += 1
                        pagar = ''
                        if contador == 1 and not preso:
                            pagar = ('pagar', dado * 4 * 0.01, dono)
                            jogo[jogador]["status"] = 'devedor'
                        elif contador == 2 and not preso:
                            pagar = ('pagar', dado * 10 * 0.01, dono)
                            jogo[jogador]["status"] = 'devedor'
                        if contador != 0:
                            opcoes.append(pagar)
        elif tipo == 'taxa':
            if jogo[jogador]["status"] != 'pagador':
                if casa == 4:
                    pagar = ('pagar', 2, 'banco')
                    jogo[jogador]["status"] = 'devedor'
                elif casa == 38:
                    pagar = ('pagar', 1, 'banco')
                    jogo[jogador]["status"] = 'devedor'
                opcoes.append(pagar)
        elif tipo == 'vá para cadeia':
            if jogo[jogador]['status'] != 'usou':
                jogo[jogador]['status'] = 'vá para cadeia'
        elif tipo == 'inicio':
            jogo[jogador]['status'] = 'livre'

    if len(jogo[jogador]['posses']) != 0:
        if jogador == atual[0]:
            opcoes.append('hipotecar')
    if len(jogo[jogador]['hipotecados']) != 0:
        if jogador == atual[0]:
            opcoes.append('desipotecar')
    if jogo[jogador]['cartoes']['ender']:
        if 'usar' not in opcoes:
            opcoes.append('usar')
        if 'vender' not in opcoes:
            opcoes.append('vender')
    if tipo == 'estacionamento' and not jogo[jogador]['cartoes']['estacionamento']:
        if not jogo[jogador]['cartoes']['estacionamento']:
            opcoes.append('estacionamento')
            if 'vender' not in opcoes and jogo[jogador]['cartoes']['estacionamento']:
                opcoes.append('vender')
    elif jogo[jogador]['cartoes']['estacionamento']:
        if len(opcoes) > 0:
            if type(opcoes[0]) == tuple:
                if opcoes[0][0] == 'pagar':
                    if 'usar' not in opcoes:
                        opcoes.append('usar')
        if 'vender' not in opcoes:
            opcoes.append('vender')
    if jogo[jogador]['cartoes']['cadeia'] is True:
        if tipo == 'vá para cadeia':
            if 'usar' not in opcoes:
                opcoes.append('usar')
        elif jogo[jogador]['status'] == 'preso':
            if 'usar' not in opcoes:
                opcoes.append('usar')
        if 'vender' not in opcoes:
            opcoes.append('vender')
    opcoesBasicas = ['desistir', 'finalizar', 'grana', 'info', 'posses']
    for op in opcoesBasicas:
        opcoes.append(op)

    if jogador == atual[0]:
        if jogo[jogador]['status'] != 'devedor':
            if jogo[jogador]['status'] != 'caixa':
                if jogo[jogador]['status'] != 'sorte':
                    if jogo[jogador]['status'] != 'escolhendo':
                        if inicioJogada is False:
                            opcoes.append('ok')
    return opcoes


def arredondaDinheiro():
    global jogo
    for jogadores in jogo.keys():
        jogo[jogadores]['dinheiro'] = round(jogo[jogadores]['dinheiro'], 4)


def caixa(num, jogador):
    global jogo, casas

    # (casa, valor, cobrador, status, item, exige outro comando, string)
    # (jogo[jogador]["casa"], 0, None, 'livre', 0, None, '')
    casa = jogo[jogador]['casa']
    valor = 0
    cobrador = None
    status = 'caixaq'
    item = 0
    comando = None
    string = ''
    if num == 1:
        valor = 0.5
        cobrador = 'banco'
        status = 'devedor'
        comando = 'pagar'
        string = f'Escreva **.m pagar** para pagar'
    elif num == 2:
        valor = 1
        cobrador = 'banco'
        status = 'devedor'
        comando = 'pagar'
        string += f'Escreva **.m pagar** para pagar'
    elif num == 3:
        item = 1
        string += f'Suas lolis foram classificadas como **anti-depressivo**, se quiser vendê-las use **.m vender**'
    elif num == 4:
        valor = 0.1
        string += f'suagrana\n'
    elif num == 5:
        valor = 0.1
        string += f'suagrana\n'
    elif num == 6:
        valor = 0.5
        cobrador = 'banco'
        status = 'devedor'
        comando = 'pagar'
        string += f'Escreva **.m pagar** para pagar'
    elif num == 7:
        valor = 0.2
        string += f'suagrana\n'
    elif num == 8:
        valor = 1
        string += f'suagrana\n'
    elif num == 9:
        valor = 0.5
        string += f'suagrana\n'
    elif num == 10:
        valor = 1
        string += f'suagrana\n'
    elif num == 11:
        valor = 2
        string += f'suagrana\n'
    elif num == 12:
        casa = 0
        valor = 2
        string += f'Você está no início. Como deu uma volta, recebeu **$2M**\n'
        string += f'suagrana\n'
    elif num == 13:
        valor = 1
        string += f'suagrana\n'
    elif num == 14:
        valor = .25
        string += f'suagrana\n'
    elif num == 15:
        valor = 0
        posses = jogo[jogador]["posses"]
        c = 0
        h = 0
        for posse in posses:
            tipo = casas[posse][2]
            if tipo == 'lote':
                numCasas = casas[posse][3]
                if numCasas == 5:
                    c += 4
                    h += 1
                    valor += 1.15 + 1.6
                else:
                    c += numCasas
                    valor += 0.4*numCasas
        string += f'Você tinha **{c} casas** e **{h} maçãs da apple**\n'
        if c == 0:
            string += f'As vezes ser fudido tem suas vantagens :estrategia:\n'
        else:
            cobrador = 'banco'
            status = 'devedor'
            comando = 'pagar'
            string += f'Por causa do maldito do albiney, você deve pagar **{formatarDinheiro(valor)}**\n'
            string += f'Escreva **.m pagar** para pagar'
    elif num == 16:
        posses = jogo[jogador]["posses"]
        temCasas = False
        for posse in posses:
            tipo = casas[posse][2]
            if tipo == 'lote':
                numCasas = casas[posse][3]
                if numCasas != 0:
                    temCasas = True
                    break
        if temCasas is False:
            string += f'Aparentemente, {jogo[jogador]["nome"]} não tem nenhuma posse que possui casas, então não precisa fazer nada! Não ser rico tem suas vantagens.. ( ͝° ͜ʖ͡°)'
        else:
            comando = 'escolha'
            status = 'escolhendo'
            jogo[jogador]["pcomando"] = 1
            string += 'Escreva **.m escolha** para deletar todas as casas de uma propriedade'
    elif num == 17:
        casa = 40
        status = 'preso'
        string += f'Você foi para o **CANTINHO DO DEPRESSOR**, se tiver um **anti-depressivo** pode sair usando **.m usar**'
    tupla = (casa, valor, cobrador, status, item, comando, string)
    return tupla


def encerraJogo():
    global verificaJogo, verificaComeco, jogoRolando, jogo, desistentes, perdedores, contaM
    verificaComeco = False
    verificaJogo = False
    jogoRolando = False
    string = '**TABELA DE INFORMAÇÕES!**\n\n'
    # nome = jogo[keys]['nome']
    jogadores = dict()
    for keys in jogo.keys():
        jogadores[keys] = jogo[keys]['totalganho']
    ranking = sorted(jogadores.items(), key=itemgetter(1), reverse=True)
    del jogadores
    i = 1
    for jogadores in ranking:
        cor = jogadores[0]
        string += f'**{i}º LUGAR**:\n{jogo[cor]["nome"]}, terminou com **{formatarDinheiro(jogo[cor]["dinheiro"])}, {len(jogo[cor]["posses"])} posses** e no **total fez {formatarDinheiro(jogo[cor]["totalganho"])}**\n\n'
        i += 1
    for perdedor in perdedores.keys():
        if perdedores[perdedor]['status'] != 'perdedor':
            string += f'**{i}º LUGAR**:\n{perdedores[perdedor]["nome"]}, terminou **NA MERDA** e no **total fez {formatarDinheiro(perdedores[perdedor]["totalganho"])}\n\n**'
        else:
            string += f'**{i}º LUGAR**:\n{perdedores[perdedor]["nome"]}, terminou com **{formatarDinheiro(perdedores[perdedor]["dinheiro"])}, {len(perdedores[perdedor]["posses"])} posses** e no **total fez {formatarDinheiro(perdedores[perdedor]["totalganho"])}**\n\n'
        i += 1
    if len(desistentes) == 1:
        string += 'DESISTENTE (não conta no pódio): \n'
    elif len(desistentes) > 1:
        string += 'DESISTENTES (não contam no pódio): \n'
    if len(desistentes) != 0:
        for desistente in desistentes.keys():
            string += f'{desistentes[desistente]["nome"]}, terminou com **{formatarDinheiro(desistentes[desistente]["dinheiro"])}, {len(desistentes[desistente]["posses"])} posses**,  e no **total fez {formatarDinheiro(desistentes[desistente]["totalganho"])}\n**'
    string += f'No total foram dados {contaM} comandos .m nesse jogo'
    string += '\n\nUM JOGO DE **gapigo**, ESPERO QUE TENHAM GOSTADO! =)'
    return string


def formatarDinheiro(dinheiro):
    if dinheiro >= 1:
        string = str(f'{dinheiro:.2f}')
        string = string[::-1]
        num = string.find('0')
        if num == 0:
            return f'${dinheiro}M'
        else:
            return f'${dinheiro:.2f}M'
    else:
        return f'${dinheiro*1000:.0f}k'


def hipoteca(jogador, casa, desipotecar=False):
    global jogo, casas
    if desipotecar is False:
        tipo = casas[casa][2]
        valor = 0
        if tipo == 'lote':
            valor = casas[casa][4][0]/2
        elif tipo == 'meme':
            valor = 1
        elif tipo == 'monstro':
            valor = 0.75
        for i in range(0, len(jogo[jogador]['posses'])):
            if jogo[jogador]['posses'][i] == casa:
                jogo[jogador]['hipotecados'].append(casa)
                del jogo[jogador]['posses'][i]
                tupla = ('receber', valor)
                transacao(tupla=tupla, jogador=jogador, hipotecar=True)
                break
    else:
        tipo = casas[casa][2]
        valor = 0
        if tipo == 'lote':
            valor = casas[casa][4][0] / 2
        elif tipo == 'meme':
            valor = 1
        elif tipo == 'monstro':
            valor = 0.75
        for i in range(0, len(jogo[jogador]['hipotecados'])):
            if jogo[jogador]['hipotecados'][i] == casa:
                jogo[jogador]['posses'].append(casa)
                del jogo[jogador]['hipotecados'][i]
                tupla = ('pagar', valor, 'banco')
                transacao(tupla, jogador)
                break


def imagemInicial():
    global pastaProjeto, jogo, casaInicio
    im1 = Image.open(pastaProjeto + '/imagens/monopoly/MONOPOLY.png')
    im2 = Image.open(pastaProjeto + '/imagens/monopoly/tabuleiro/peao/peoes.png')

    # limpa a game.png antiga e repõe com uma nova
    im1.save(f'{pastaProjeto}/imagens/monopoly/game.png')

    path = pastaProjeto + '/imagens/monopoly/tabuleiro/peao'
    jogadores = []
    for j in jogo.keys():
        jogadores.append(j)

    for jogador in jogadores:
        if jogador == 'verde':
            pattern = 'verde'
        elif jogador == 'amarelo':
            pattern = 'amarelo'
        elif jogador == 'azul':
            pattern = 'azul'
        elif jogador == 'vermelho':
            pattern = 'vermelho'

        mask = Image.open(f'{path}/{pattern}/{pattern} {casaInicio}.png').convert("1")
        im1 = Image.composite(im2, im1, mask)
        im1.save(f'{pastaProjeto}/imagens/monopoly/gamepeao.png')


def inicializaCasas():
    global casas
    casas = [['inicio', None, 'inicio'],  # 0
             ['Augusta', None, 'lote', 0, (0.6, 0.5, 0.02, 0.1, 0.3, 0.9, 1.6, 2.5), (1, 3)],  # 1
             ['Caixa Lazarenta', None, 'caixa'],  # 2
             ['Botinha', None, 'lote', 0, (0.6, 0.5, 0.02, 0.1, 0.3, 0.9, 1.6, 2.5), (1, 3)],  # 3
             ['Imposto', None, 'taxa'],  # 4
             ['Aparelho Computadorizado', None, 'meme', 2, (5, 15, 25, 35)],  # 5
             ['Rata', None, 'lote', 0, (1, 0.5, 0.06, 0.3, 0.9, 2.7, 4, 5.5), (6, 8, 9)],  # 6
             ['Sorte do Guardião', None, "sorte"],  # 7
             ['Cemitério de Boga', None, 'lote', 0, (1, 0.5, 0.06, 0.3, 0.9, 2.7, 4, 5.5), (6, 8, 9)],  # 8
             ['Cemitério de Guardião', None, 'lote', 0, (1.2, 0.5, 0.08, 0.4, 1, 3, 4.5, 6), (6, 8, 9)],  # 9
             ['Canto do Depresso - Apenas Visitante', None, 0],  # 10
             ['Não-Me-Toque', None,  'lote', 0, (1.4, 1, 0.1, 0.5, 1.5, 4.5, 6.25, 7.5), (11, 13, 14)],  # 11
             ['TOCUFOMI', None, 'monstro', 1.5, (12, 28)],  # 12
             ['Sumaré', None,  'lote', 0, (1.4, 1, 0.1, 0.5, 1.5, 4.5, 6.25, 7.5), (11, 13, 14)],  # 13
             ['The Floating Dead', None, 'lote', 0, (1.6, 1, 0.12, 0.6, 1.8, 5, 7, 9), (11, 13, 14)],  # 14
             ['CARPE DIEM', None,  'meme', 2, (5, 15, 25, 35)],  # 15
             ['Nárnia', None, 'lote', 0, (1.8, 1, 0.14, 0.7, 2, 5.5, 7.5, 9.5), (16, 18, 19)],  # 16
             ['Caixa Lazarenta', None, 'caixa'],  # 17
             ['Groelândia', None, 'lote', 0, (1.8, 1, 0.14, 0.7, 2, 5.5, 7.5, 9.5), (16, 18, 19)],  # 18
             ['Acre', None, 'lote', 0, (2, 1, 0.16, 0.8, 2.2, 6, 8, 10), (16, 18, 19)],  # 19
             ['Sugar Daddy', None, 'estacionamento'],  # 20
             ['Casa do Caralho', None, 'lote', 0, (2.2, 1.5, 0.18, 0.9, 2.5, 7, 8.75, 10.5), (21, 23, 24)],  # 21
             ['Sorte do Guardião', None, 'sorte'],  # 22
             ['Bank Heist', None, 'lote', 0, (2.2, 1.5, 0.18, 0.9, 2.5, 7, 8.75, 10.5), (21, 23, 24)],  # 23
             ['Orbital do Gapigo', None, 'lote', 0, (2.4, 1.5, 0.2, 1, 3, 7.5, 9.25, 11), (21, 23, 24)],  # 24
             ['CANCER CURATIVO', None, 'meme', 2, (5, 15, 25, 35)],  # 25
             ['Chernobyla', None, 'lote', 0, (2.6, 1.5, 0.22, 1.1, 3.3, 8, 9.75, 11.5), (26, 27, 29)],  # 26
             ['Caverna das Peranhas', None, 'lote', 0, (2.6, 1.5, 0.22, 1.1, 3.3, 8, 9.75, 11.5), (26, 27, 29)],  # 27
             ['CHUPACU', None, 'monstro', 1.5, (12, 28)],  # 28
             ['Universidade Enquedita', None, 'lote', 0, (2.8, 1.5, 0.24, 1.2, 3.6, 8.5, 10.25, 12), (26, 27, 29)],  # 29
             ['I Have Crippling Depression', None, 'vá para cadeia'],  # 30
             ['Refúgio do Nego Ney', None, 'lote', 0, (3, 2, 0.26, 1.3, 3.9, 9, 11, 12.75), (31, 32, 34)],  # 31
             ['Santuário do Dorime', None, 'lote', 0, (3, 2, 0.26, 1.3, 3.9, 9, 11, 12.75), (31, 32, 34)],  # 32
             ['Caixa Lazarenta', None, 'caixa'],  # 33
             ['Mansão do Ricardão', None, 'lote', 0, (3.2, 2, 0.28, 1.5, 4.5, 10, 12, 14), (31, 32, 34)],  # 34
             ['Cool de Curioso', 'amarelo', 'meme', 2, (5, 15, 25, 35)], #35
             ['Sorte do Guardião', None, 'sorte'],  # 36
             ['Inferno', None, 'lote', 0, (3.5, 2, 0.35, 1.75, 5, 11, 13, 15), (37, 39)],  # 37
             ['Coerção Estatal', None, 'taxa'],  # 38
             ['Buraco Negro', None, 'lote', 0, (4, 2, 0.5, 2, 6, 14, 17, 20), (37, 39)],  # 39
             ['Cantinho do Depresso', None, 'cadeia']]  # 40
    # NOME DA CASA, DE QUEM É, CASAS
    # nome lote, de quem, tipo, casas, [custo compra, custo cada casa, aluguel base, 1 casa,..., 4 casas, hotel]


def jogar(jogador):
    global jogo, quantoGanhaAoPassarNoInicio
    casa = jogo[jogador]['casa']
    passouPeloInicio = False
    dado = random.randint(1, 6)
    if dado + casa >= 40:
        casa -= 40
        transacao(('receber', quantoGanhaAoPassarNoInicio), jogador)
        passouPeloInicio = True
    jogo[jogador]['casa'] = casa + dado
    inicioJogada = False
    dado = (dado, passouPeloInicio)
    return dado


def modificaCasas(jogador, casa):
    global pastaProjeto, jogo, casas
    im1 = Image.open(pastaProjeto + '/imagens/monopoly/game.png')
    im2 = Image.open(pastaProjeto + f'/imagens/monopoly/casas/{jogador}.png')
    im3 = Image.open(pastaProjeto + '/imagens/monopoly/gamepeao.png')
    mask = Image.open(pastaProjeto + f'/imagens/monopoly/casas/patterns/{casa} {casas[casa][3]}.png').convert('1')
    im1 = Image.composite(im2, im1, mask)
    im1.save(pastaProjeto + '/imagens/monopoly/game.png')

    # Agora modifica a gamepeao.png
    mask = Image.open(pastaProjeto + '/imagens/monopoly/maskgame.png').convert('1')
    im3 = Image.composite(im3, im1, mask)  # atualiza a gamepeao com as casas da game
    im3.save(pastaProjeto + '/imagens/monopoly/gamepeao.png')


def modificaGamepeao(jogador, casaAntiga):
    global pastaProjeto, jogo
    im1 = Image.open(pastaProjeto + '/imagens/monopoly/gamepeao.png')
    im2 = Image.open(pastaProjeto + '/imagens/monopoly/tabuleiro/peao/peoes.png')
    im3 = Image.open(pastaProjeto + '/imagens/monopoly/game.png')

    path = pastaProjeto + '/imagens/monopoly/tabuleiro/peao'

    # APAGA A CASA ANTIGA DO JOGADOR!
    mask = Image.open(f'{path}/{jogador}/{jogador} {casaAntiga}.png').convert("1")
    im1 = Image.composite(im3, im1, mask)  # apaga a casa antiga do jogador
    im1.save(f'{pastaProjeto}/imagens/monopoly/gamepeao.png')

    # MODIFICA A IMAGEM "gamepeao.png" PARA CASA ATUAL DO JOGADOR
    mask = Image.open(f'{path}/{jogador}/{jogador} {jogo[jogador]["casa"]}.png').convert("1")
    im1 = Image.composite(im2, im1, mask)
    im1.save(f'{pastaProjeto}/imagens/monopoly/gamepeao.png')


def passaAtual():
    global atual, escolhidas
    # RESETA O LOOP DE JOGADORES SE JÁ CHEGOU NO FIM
    ultimoAJogar = atual[0]
    if atual[1] + 1 == numJogadores:
        atual[1] = 0
        ecor, enome, eid = escolhidas[atual[1]].split(',')
        atual[0] = ecor
    # TROCA A VEZ DO JOGADOR
    else:
        atual[1] += 1
        ecor, enome, eid = escolhidas[atual[1]].split(',')
        atual[0] = ecor
    string = f'É a vez de {enome} de cor **{ecor.upper()}**'
    return string


def retiraJogador(jogador, cobrador, caixa=False):
    global jogo, casas, perdedores, atual, escolhidas
    if cobrador == 'banco':
        if caixa == False:
            jogo[jogador]['dinheiro'] = 0
    else:
        jogo[cobrador]['dinheiro'] += jogo[jogador]['dinheiro']
        jogo[cobrador]['totalganho'] += jogo[jogador]['dinheiro']
        jogo[jogador]['dinheiro'] = 0
    if caixa is True:
        jogo[jogador]['status'] = 'perdedor'
    perdedores[jogador] = jogo[jogador]
    del jogo[jogador]
    del escolhidas[atual[1]]
    if len(jogo) == 1:
        return True
    else:
        return False


def thumbCasa(casa, thumbCompraCasa = False):
    global pastaProjeto
    path = pastaProjeto
    if thumbCompraCasa is False:
        path += '/imagens/monopoly/gamepeao.png'
    else:
        path += '/imagens/monopoly/game.png'
    imagem = Image.open(path)
    imagem2 = Image.open(path)
    virar90 = Image.ROTATE_90
    virar270 = Image.ROTATE_270
    endereços1 = [
        0, 1300, 1304, 1500, 1500,
        1, 1178, 1304, 1300, 1498,
        2, 1054, 1305, 1177, 1498,
        3, 931, 1304, 1054, 1498,
        4, 809, 1304, 931, 1498,
        5, 685, 1304, 809, 1498,
        6, 562, 1304, 685, 1498,
        7, 439, 1304, 562, 1498,
        8, 317, 1304, 439, 1498,
        9, 194, 1304, 317, 1498,
        10, 0, 1304, 194, 1498,
    ]
    endereços2 = [20, 0, 0, 195, 195,
              21, 194, 0, 316, 197,
              22, 316, 0, 438, 197,
              23, 438, 0, 562, 197,
              24, 562, 0, 685, 197,
              25, 685, 0, 808, 197,
              26, 808, 0, 931, 197,
              27, 931, 0, 1054, 197,
              28, 1054, 0, 1177, 197,
              29, 1177, 0, 1300, 197,
              30, 1300, 0, 1500, 197]

    proporção = 5
    if casa in range(0, 11):
        for j in range(0, len(endereços1)):
            if endereços1[j] == casa:
                imagem2 = imagem.crop((endereços1[j+1], endereços1[j+2], endereços1[j+3], endereços1[j+4]))
                size = imagem2.size
                size = (size[0]*proporção, size[1]*proporção)
                imagem2 = ImageOps.fit(imagem2, size)
                break
    elif casa in range(11, 20):
        imagem = imagem.transpose(virar90)
        casaCorrespondente = casa - 10
        for j in range(0, len(endereços1)):
            if endereços1[j] == casaCorrespondente:
                imagem2 = imagem.crop((endereços1[j+1], endereços1[j+2], endereços1[j+3], endereços1[j+4]))
                size = imagem2.size
                size = (size[0] * proporção, size[1] * proporção)
                imagem2 = ImageOps.fit(imagem2, size)
                break
    elif casa in range(31, 40):
        imagem = imagem.transpose(virar270)
        casaCorrespondente = casa - 30
        for j in range(0, len(endereços1)):
            if endereços1[j] == casaCorrespondente:
                imagem2 = imagem.crop((endereços1[j + 1], endereços1[j + 2], endereços1[j + 3], endereços1[j + 4]))
                size = imagem2.size
                size = (size[0] * proporção, size[1] * proporção)
                imagem2 = ImageOps.fit(imagem2, size)
                break
    elif casa in range(20, 31):
        for j in range(0, len(endereços2)):
            if endereços2[j] == casa:
                imagem2 = imagem.crop((endereços2[j + 1], endereços2[j + 2], endereços2[j + 3], endereços2[j + 4]))
                size = imagem2.size
                size = (size[0] * proporção, size[1] * proporção)
                imagem2 = ImageOps.fit(imagem2, size)
                break
    elif casa == 40:
        imagem2 = imagem.crop((53, 1304, 192, 1445))
        size = imagem2.size
        size = (size[0] * proporção, size[1] * proporção)
        imagem2 = ImageOps.fit(imagem2, size)
    imagem2.save(pastaProjeto + '/imagens/monopoly/temp/thumbAtual.png')

    ponta = "SÓ A PONTA\n…………………...„„-~^^~„-„„_\n………………„-^*'' : : „'' : : : : *-„\n…………..„-* : : :„„--/ : : : : : : : " \
            "'\n…………./ : : „-* . .| : : : : : : : : '|\n……….../ : „-* . . . | : : : : : : : : |\n………...\„-* . . . . " \
            ".| : : : : : : : :'|\n……….../ . . . . . . '| : : : : : : : :|\n……..../ . . . . . . . .'\ : : : : : : : " \
            "|\n……../ . . . . . . . . . .\ : : : : : : :|\n……./ . . . . . . . . . . . '\ : : : : : /\n….../ . . . . . " \
            ". . . . . . . . *-„„„„-*'\n….'/ . . . . . . . . . . . . . . '|\n…/ . . . . . . . ./ . . . . . . .|\n../ " \
            ". . . . . . . .'/ . . . . . . .' "

    rato = """                                                                                    .  ,
                                                                                 (\;/)
                                                                                 oo   \//,        _
                                                                             ,/_;~      \,     / '
                                                                            ¨'    (  (   \    !
                                                                                //  \   |__.'
_ /＼●__ /＼●__ /＼●__ /＼●__ /＼●_    '~  '~----''"""

    mensagens = ['Toma esses $2M\nAgora vê se para de cair em lugar que não era (╯‵□′)╯︵┴─┴',
                 'Lugar onde muitas mães foram acusadas de rodar a bolsinha ヽ(´Д`;)ﾉ',
                 'De **BOSTA PURA** à **gold**, reze antes de abrir (・ωｰ)～☆',
                 'É..\n**É... MENTIRA (　〇□〇）**',
                 'MALDITO ESTADO! CADÊ OS ANCAPS NESSA PORRA? (ノಠ益ಠ)ノ彡┻━┻',
                 'AMO TECLAR NO MEU APARELHO COMPUTADORIZADO... ( ဖ‿ဖ)_/\n\nPerai, tenho que **PAGAR QUANTO?** ゞ◎Д◎ヾ',
                 'Achas que tens o que é preciso para esmagares a minha rata? **CLICA AQUI**\n（￣ε￣ʃƪ）\n~~le scam\n(;ﾟдﾟ)',
                 'o gapigo fala: VAI SE BENZER GUARDIÃO!!! ＼(´◓Д◔`)／',
                 '"BIG, SE VOCÊ IR TAPETE DE MAG 7 VAI MORRER"\n"roger that"\n"ENTÃO SAI DAI IMBECIL"\n"Negattive"\n~~Big morre\n"IMBECIL!!!" (╬♛ 益♛ )',
                 'if eco is true:\n    buy **R8**\n    go **mid**\n    empty **ammunition** till **FUCKING DIE**\n\nif died:\n    say **BYATTTT! NEIN, NEIN, NEIN, NEIN, NEIN, NEIN!!!!!\n(◞≼◉ื≽◟ ;益;◞≼◉ื≽◟)Ψ',
                 'Cantinho da depressão, apenas visitantes\nApenas vendo como funciona a vida ( ･ω･)ﾉ',
                 'Prefeito de **não-me-toque** é afastado por assédio ಠ_ರೃ',
                 f'**TOCOFOMEEEEEEEEE\nCOM FOMEEEEEEEEEEEEEEE\nCOM A PORRAAAAA DE FOMEEEEEEEEEEE\n{"T" + "O" * 10 + " C" + "O"*10 + "M" + " FOM" + "E"*200}\n\nvítimas: (((ﾟДﾟДﾟДﾟ)))**',
                 'Dizem que o Acre é um estado\nTo começando a achar que é uma cidade Hm... :hm:\nAcho que o gleison lima concorda (￣ー￣)ｂ',
                 'A transformação secreta de São Paulo para lutar contra o Jiren\nDando leptospirose para ele\n\n**OUTSTANDING MOVE SÃO PAULO! (☉∀☉)**',
                 'eu sou o passaro Quetzalcoatlus\ne eu dubido vc nao fala\n\n        ***carpe diem***\n\npelos proximo 5 sem gundo\n⊹⋛⋋(◐⊝◑)⋌⋚⊹',
                 'lá foi achado o integrante honesto do PT\n\n\n- pera, você disse "hones..? **(ʘ言ʘ╬)??!!!**',
                 'cuidado com o guardião e suas caixas de pandora ༼つಠ益ಠ༽つ ─=≡ΣO))     ⊃゜Д゜）⊃',
                 'ʕʘ‿ʘʔ\n\n...\n\n(╬ﾟ◥益◤ﾟ) GROELÂNDIA SUA GRANDISSÍSMA FILHA DA PUTA, ESCUTA AQUI SEU TERRITÓRIO VERM... \n         - gapigo, 2018, definitivamente não em um de seus melhores momentos (︶︹︺)',
                 'basicamente um scam\n**EU POSSO EXPLICAR!**\nVeja bem: se você comprar, você tá comprando algo que não existe\nse você for obrigado a pagar, você tá pagando para nada, ou seja, sendo roubado que nem quando paga imposto ☜╮(´ิ∀´ิ☜╮)',
                 'Parabéns, você ganhou um sugar daddy para te sustentar\nNa próxima vez que você tiver que pagar algo, você terá a opção "USAR"\n\nPera, você ganhou o que? HMMMMMM **paitola**\n'
                        '( ͡ʘ╭͜ʖ╮͡ʘ) ( ͡⚆ ͜ʖ ͡⚆)  ( ͡☉ ͜ʖ ͡☉)   (つ ͡° ͜ʖ ͡°)つ',
                 ponta,
                 'ᕕ༼✿•̀︿•́༽ᕗ -> sorte do guardião quando ele começa uma partida de CSGO',
                 'O CARA BOTOU UMA MÁSCARA!!! (ʘ言ʘ╬)\n**CHAMA BULLDOZER!!!!** ┻━┻彡(┛◉Д◉)┛彡┻━┻',
                 'basicamente o real motivo do gapigo ter dropado o warframe (゜Д゜*)（´皿｀；）',
                 '**so o nuevo canser\ncurativo esijo dinero**',
                 'E o qu  ée ess? (ʘдʘ╬)\nVOC ACH QU ISS É NORMALA? (ಠ⌣ಠ)\nOlha iss áqui gent (ಠ ∩ಠ)\nParace a Chernobyle (╬ಠ益ಠ)\n_(´ཀ`」 ∠)_ blé',
                 'PERANHAS...(ﾟДﾟ;)\n\n**PERANHAS EVERYWHEREE!!!!! 三ᕕ(◉Д◉ )ᕗ**',
                 'Cuidado com o Chupa Cu de goianinha,\nele pode aparecer a qualquer hora em qualq..\nPERA... que molhadinho é esse na minha bunda? ⑉ႣỏႣ⑉\n\n...\n\n **CORRE LADRÃO! 三ᕕ(◉Д◉ )ᕗ**',
                 'TENHO CARA DE ENQUEDITA MEU\nPORRA MEU\nTODO DIA ISSO MEU\nSÓ PORQUE SO CANHOTO MEU\nTODO DIAS ESSES ENQUEDITA\nMATA ESSES ENQUEDITA LOGO\nE ME DEXA SE CANHOTO EM PAZ MEU\nPORA MEU\nTODO DIA\nTODO DIA\nNUM E POSSIVEL MEU\nTODO DIA ENQUEDITA FAZENDO MERDA MEU\nACABA LOGO COM ESSES FIOS DA PUTA MEU\n	- honestamente, zezoia, 2020 （πーπ)',
                 'É meu chapa, parece que você ganhou a famosa,\nA TEMIDA,\nA QUE O GUARDIÃO SEMPRE FALA\n...\n**YOU GAINED CRIPPLING DEPRESSION (；´∩｀；)**',
                 'ele que criou o coronga virus\nÉ o capeta reencarnado, ele cuspiu fogo e incendiou a Austrália\nEle atirou de lança-chamas pro céu e pegou na Amazônia e fez as queimadas dos últimos 20 anos\nEle deu um peido e criou a radiação de Chernobyl\no terremoto do japão foi uma tentativa homofobica de nego ney de eliminar os niponicos do mundo\nÉ ele que forçou as mulheres na 2ª guerra a trabalhar mais de 24 horas por dia\nEle que criou o fascismo e ensinou Mussolini\nele ensinou hitler a queimar judeu apenas pq gostava do aroma\nEle que ensinou os espartanos a atacar os defeituosos no fundo do poço só pra fazer a famosa "sopa de macaco"\n\n**  - Guardião e gapigo comentando as atrocidades do maligno Nego Ney 屮(ఠ𐤃ఠ)屮**',
                 f'**DORIMEEE** :musical_note:\nINTERINO ADAPARE\n**DORIME**\nAMENO, AMENO\nLATIRE\nLATIREMO\n**DORIME**\n{rato}',
                 "Rolando pra ver se dá sorte...\n(ﾟ∀ﾟ)( ﾟ∀)(　ﾟ)(　　)(ﾟ　)(∀ﾟ )(ﾟ∀ﾟ)",
                 'ears: U got that\neyes: Anime\nbrain: Ricardo\nMind: Moto Moto\nHands: meme\nhotel: trivago\nme: got that\ngapigo:   ┬┴┬┴┤͜ʖ ͡°) olá meu chapa├┬┴┬┴',
                 'oq q ele fes\n\n**- ELE COME** conta **COOL**rente **DE CURIOSO**',
                 "༼;´༎ຶ ༎ຶ༽ -> sanidade mental do guardião após a sorte dele dar um alô\n**(´༎ຶ༎ຶ) -> guardião não podendo discordar**",
                 '(（ლ ^ิ౪^ิ）ლ) - Posso ir já?\n((ಠ ∩ಠ)) - Não\n(（ლ ^ิ౪^ิ）ლ) - Mas é minha casa\n((ಠ ∩ಠ)) - Já disse que não\n(（ლ ^ิ౪^ิ）ლ) - Onde vou ficar então?\n -(ლಠ益ಠ)ლ) **SEI LÁ SEU FILHO DA PUTA, SÓ SEI QUE VOCÊ NÃO MORREU ENTÃO NÃO VAI PRA LÁ**\n\n - Guardião conversando com a Morte',
                 'Parece difícil para a maioria das pessoas entender **princípios econômicos básicos** e as repercussões óbvias do uso da coerção estatal no mercado. Eu acho tudo isso muito simples, basta entendermos que **a coerção não muda os princípios econômicos**, ela apenas **interfere nos seus resultados, normalmente para pior**.\n\nOs princípios econômicos fundamentais que precisamos ter em mente quando vemos o **governo intervindo no mercado através da coerção** são poucos, listo abaixo alguns:\n\n1. Gastos\n**Governo não cria valor algum**, para ele poder trocar os valores que não possui por aqueles que ele deseja, **precisará, antes, subtrair valor** já criado de quem os criou. **Isso só é possível com o uso da coerção**. Quando o governo se intromete na economia é apenas uma **infernal máquina de redistribuição violenta de recursos**. **Suga o valor existente no mercado**, retém parte para si e **distribui para aqueles que ele pretende favorecer com privilégios**. Parece difícil para a maioria das pessoas entender princípios econômicos básicos e as **repercussões óbvias do uso da coerção estatal no mercado**. Eu acho tudo isso muito simples, basta entendermos que **a coerção** não muda os princípios econômicos, ela **apenas interfere nos seus resultados, normalmente para pior**.\n\nOs princípios econômicos fundamentais que precisamos ter em mente quando vemos o governo intervindo no mercado através da coerção são poucos, listo abaixo alguns:\n\n2. Tributação\n**Sempre que o governo decidir gastar, não adianta espernear, ele terá que tributar**. **Cada centavo** despendido pelo governo **será retirado de alguém**, queira essa pessoa ou não. Ou vocês não sabem **o significado de coerção?** Governos não tributam porque não têm mais o que fazer, **governos tributam para gastar**. E tem **mais, governos** podem seguir gastando mesmo quando não conseguem **mais tributar.** (´・＿・`)',
                 'Quem diria que visitar o cu dos outros é tão caro? (*´Д｀)=з',
                 'I GAINED CRIPPLING DEPRESSOR DPS DESSA ♿(；´∩｀；)'
                 ]

    return mensagens[casa]


def transacao(tupla=(), jogador='', hipotecar=False):
    global casas, jogo

    #  receber ('receber', dinheiro)
    if tupla[0] == 'receber':
        jogo[jogador]['dinheiro'] += tupla[1]
        if not hipotecar:
            jogo[jogador]['totalganho'] += tupla[1]
    #  pagar ('pagar', preço, cobrador)
    elif tupla[0] == 'pagar':
        if tupla[2].lower() != 'todos':
            jogo[jogador]['dinheiro'] -= tupla[1]
            if tupla[2].lower() not in 'banco':
                jogo[tupla[2]]['dinheiro'] += tupla[1]
                jogo[tupla[2]]['totalganho'] += tupla[1]
        else:
            numAdversários = (len(jogo) - 1)
            jogo[jogador]['dinheiro'] -= tupla[1]*numAdversários
            for jogadores in jogo.keys():
                if jogadores != jogador:
                    jogo[jogadores]['dinheiro'] += tupla[1]
                    jogo[jogadores]['totalganho'] += tupla[1]
    # comprar ('comprar', casa, preço, opção)
    elif tupla[0] == 'comprar':
        if tupla[3].lower() in 'posse':
            jogo[jogador]['dinheiro'] -= tupla[2]
            jogo[jogador]['posses'].append(tupla[1])
            casas[tupla[1]][1] = jogador
        elif tupla[3] == 'mais casas':
            jogo[jogador]['dinheiro'] -= tupla[2]
            casas[tupla[1]][3] += 1


def sorte(num, jogador):
    global jogo, casas, inicioJogada

    # (casa, valor, cobrador, status, item, exige outro comando, string)
    # (jogo[jogador]["casa"], 0, None, 'livre', 0, None, '')
    casa = jogo[jogador]['casa']
    valor = 0
    cobrador = None
    status = 'sorteq'
    item = 0
    comando = None
    string = ''
    if num == 1:
        casa = 39
        string = f'Você foi até o buraco negro'
    elif num == 2:
        valor = 2
        casa = 0
        string += 'Você recebeu **$2M** por passar pelo **ponto de partida**\n'
        string += f'suagrana\n'
    elif num == 3:
        valor = 0.5
        string += f'suagrana\n'
    elif num == 4 or num == 14:
        # sortes = (7, 22, 36)
        # memes = (5, 15, 25, 35)
        if casa == 36:
            tupla = ('receber', 2)
            transacao(tupla, jogador)
            string += 'Você passou pelo ponto de início, então recebeu **$2M**\n'
        if casa == 7:
            casa = 15
            meme = 'CARPE DIEM'
        elif casa == 22:
            casa = 25
            meme = 'CANCER CURATIVO'
        elif casa == 36:
            casa = 5
            meme = 'APARELHO COMPUTADORIZADO'
        string += f'Você foi de **sorte de guardião** para **{meme}**\n'

        # SE TEM DONO
        if casas[casa][1] != jogador and casas[casa][1] != None:
            dono = casas[casa][1]
            cobrador = dono
            contador = 0
            preso = (jogo[dono]['status'] == 'preso')
            comando = 'pagar1'
            # Conta quantos "MEMES" o jogador possui
            for posse in jogo[dono]['posses']:
                for i in range(0, 4):
                    if posse == casas[casa][4][i]:
                        contador += 1
            if contador != 0 and not preso:
                valor = 0.25 * (2 ** (contador - 1))
                valor *= 2
                jogo[jogador]['pcomando'] = ('pagar', valor, dono)
    elif num == 5:
        valor = 0
        posses = jogo[jogador]["posses"]
        c = 0
        h = 0
        for posse in posses:
            tipo = casas[posse][2]
            if tipo == 'lote':
                numCasas = casas[posse][3]
                if numCasas == 5:
                    c += 4
                    h += 1
                    valor += 1 + 1.6
                else:
                    c += numCasas
                    valor += 0.25 * numCasas
        string += f'Você tinha **{c} casas** e **{h} maçãs da apple**\n'
        if c == 0:
            string += f'As vezes ser fudido tem suas vantagens :estrategia:\n'
        else:
            cobrador = 'banco'
            status = 'devedor'
            comando = 'pagar'
            string += f'Por causa da maldita eleição enquedita, você deve pagar **{formatarDinheiro(valor)}**\n'
            string += f'Escreva **.m pagar** para pagar'
    elif num == 6:
        # sortes = (7, 22, 36)
        # monstro = (12, 28)
        if casa == 36:
            tupla = ('receber', 2)
            transacao(tupla, jogador)
            string += 'Você passou pelo ponto de início, então recebeu **$2M**\n'
        if casa == 7:
            casa = 12
            monstro = 'TOCUFOMI'
        elif casa == 22:
            casa = 28
            monstro = 'CHUPA CU'
        elif casa == 36:
            casa = 12
            monstro = 'TOCUFOMI'
        string += f'Você foi de **sorte de guardião** para **{monstro}**\n'

        # SE TEM DONO
        if casas[casa][1] != jogador and casas[casa][1] != None:
            comando = 'jogar'
            cobrador = casas[casa][1]
            inicioJogada = True
            jogo[jogador]['pcomando'] = ('pagar1', 0.2, cobrador)
            string += f'**{monstro}** é propriedade de {jogo[cobrador]["nome"]}!\n' \
                      f'Role os dados com **.m jogar** e o produto do valor dado por **$200k** deve ser pago a ele com **.m pagar**'
    elif num == 7:
        casa = 40
        status = 'preso'
        string += f'Você foi para o **CANTINHO DO DEPRESSOR**, se tiver um **anti-depressivo** pode sair usando **.m usar**'
    elif num == 8:
        item = 1
        string += f'Os **memes do guardião** são classificados como **anti-depressivo**, se quiser vendê-los use **.m vender**'
    elif num == 9:
        valor = 0.15
        cobrador = 'banco'
        status = 'devedor'
        comando = 'pagar'
        string += f'Escreva **.m pagar** para pagar'
    elif num == 10:
        valor = 1.5
        string += f'suagrana\n'
    elif num == 11:
        casa -= 3
        string += f'Você caiu em **{casas[casa][0]}**'
    elif num == 12:
        if casa == 36 or casa == 22:
            tupla = ('receber', 2)
            transacao(tupla, jogador)
            string += 'Você passou pelo ponto de início, então recebeu **$2M**\n'
            string += 'suagrana\n'
        casa = 11
        string += f'Você caiu em **{casas[casa][0]}**'
    elif num == 13:
        if casa == 36:
            tupla = ('receber', 2)
            transacao(tupla, jogador)
            string += 'Você passou pelo ponto de início, então recebeu **$2M**\n'
            string += 'suagrana\n'
        casa = 24
        string += f'Você caiu em **{casas[casa][0]}**'
    elif num == 15:
        valor = 0.5
        cobrador = 'todos'
        status = 'devedor'
        comando = 'pagar'
        string += f'Escreva **.m pagar** para pagar'
    elif num == 16:
        tupla = ('receber', 2)
        transacao(tupla, jogador)
        string += 'Você passou pelo ponto de início, então recebeu **$2M**\n'
        string += 'suagrana\n'
        comando = 'jogar'
        cobrador = casas[casa][1]
        inicioJogada = True
        jogo[jogador]['pcomando'] = 'receber1'
        string += 'Escreva **.m jogar** para receber'
        inicioJogada = True
    elif num == 17:
        string += '**AMENO**'
    elif num == 18:
        status = 'oi'
        string += 'oi'
    elif num == 19:
        # sortes = (7, 22, 36)
        if casa == 36:
            tupla = ('receber', 2)
            transacao(tupla, jogador)
            string += 'Você passou pelo ponto de início, então recebeu **$2M**\n'
        if casa == 7:
            foi = 1
            para = 2
            casa = 22
        elif casa == 22:
            foi = 2
            para = 3
            casa = 36
        elif casa == 36:
            foi = 3
            para = 1
            casa = 7
        string += f'Você foi de **sorte de guardião {foi}** para **sorte de guardião {para}**'
    tupla = (casa, valor, cobrador, status, item, comando, string)
    return tupla


def voceCaiu(jogador, casa):
    global jogo, casas
    if casa != 40:
        string = f'{jogo[jogador]["nome"]}, você caiu na casa **{casas[casa][0]}**, '
    # Se a casa não tem dono
    disponiveis = analisaAcoes(jogador, False)
    if type(disponiveis[0]) is tuple:
        tupla = disponiveis[0]
        disponiveis[0] = tupla[0]
    # SE A CASA NÃO TEM DONO, OU O DONO É O JOGADOR
    if casas[casa][1] is None or casas[casa][1] == jogador:
        tipo = casas[casa][2]
        if tipo == 'estacionamento':
            string += f'Que te fornece um sugar daddy para pagar qualquer pagamento que você quiser com **.m usar**'
        elif tipo == 'caixa':
            string += f'que exige que você abra uma **CAIXA LAZARENTA**. Abra-a com **.m caixa**'
        elif tipo == 'sorte':
            string += f'que exige que você abra uma **SORTE DO GUARDIÃO**, honrando assim o mestre zezoiado. Abra-a com **.m sorte**'
        elif tipo == 'taxa':
            preço = tupla[1]
            if casa == 4:
                string += f'que te obriga a **PAGAR UM FODENDO IMPOSTO DE {formatarDinheiro(preço)}**. Ajude a causa anarco capitalista visitando o canal do Raphael Lima do ideias radicais.'
            elif casa == 38:
                string += f'que te coage a **PAGAR UM IMPOSTO DE {formatarDinheiro(preço)}**. Depois acham a ideia de Anarco capitalismo errada.'
        elif tipo == 'vá para cadeia':
            string += f'que te mandará para o **CANTINHO DO DEPRESSO**.\n' \
                      f'Se você não tem anti-depressivo, dê **.m ok** para passar a vez e quando for a sua vez, escolha dois' \
                      f' números com **.m jogar (num1) (num2)** entre 1 e 6\nExemplo: **.m jogar 3 5**\n\n' \
                      f'Se você tiver cartão, tente **.usar anti-depressivo**\n' \
                      f'Se alguém tiver, tente negociar com **.vender**'
        elif tipo == 'cadeia':
            string += f'É {jogo[jogador]["nome"]}... Essa vida de depressivo não é fácil não. (╥_╥) ( ͡ຈ ͜ʖ ͡ຈ).'
        else:
            if disponiveis[0] == 'comprar':
                if casas[casa][1] == jogador:
                    numCasas = casas[casa][3]
                    if numCasas in range(1, 4):
                        string += f'que **já era sua** e tem **opções** de **colocar mais casas** por {formatarDinheiro(casas[casa][4][1])}. Se você quiser colocar, dê um **.m comprar**'
                    elif numCasas != 5:
                        string += f'que **já era sua** e tem **opções** de **colocar MAÇÃ DA APPLE** por {formatarDinheiro(casas[casa][4][1])}. Se você quiser colocar, dê um **.m comprar**'
                else:
                    string += f'que **não tem dono**. Como você tem dinheiro, você tem a **opção de comprá-la** por **{formatarDinheiro(tupla[2])}** com o **.m comprar**'
            else:
                if casas[casa][1] is None:
                    string += 'que **não tem dono**. Entretanto, **você não tem o dinheiro suficiente** para comprá-la, então esta opção não está disponível.'
                elif tipo == 'lote':
                    string += f'que **já era sua** e como **já tem o limite máximo de casas** você não pode comprar mais nada'
                elif casas[casa][1] == jogador:
                    string += f'que **já era sua**.'
    else:  # Toda casa com dono é obrigado a cair aqui, pois todo dono deve receber
        dono = casas[casa][1]
        tipo = casas[casa][2]
        string += f'que é propriedade de {jogo[dono]["nome"]}. '
        hipotecado = False
        for hipotecados in jogo[dono]['hipotecados']:
            if casa == hipotecados:
                hipotecado = True
        preso = (jogo[dono]['status'] == 'preso')
        if hipotecado:
            string += f'No entanto, ela está hipotecada no momento. Então você não terá que pagar nada!'
        elif preso:
            string += f'Todavia, {jogo[dono]["nome"]} está muito depresso para te cobrar agora. Então {jogo[jogador]["nome"]} não terá que pagar nada!'
        else:
            preço = tupla[1]
            if tipo == 'lote':
                preçoCasa = casas[casa][4][2]
                numCasas = casas[casa][3]
                if numCasas == 0:
                    if preçoCasa == preço:
                        string += f'Esta propriedade **não tem casas**, então você **pagará o valor do aluguel** de **{formatarDinheiro(preço)}**.'
                    else:
                        string += f'Esta propriedade **não tem casas**, entretanto, o jogador possui **todas as propriedades da mesma cor**, então você tem que **pagar o dobro do aluguel comum**, totalizando **{formatarDinheiro(preço)}**.'
                else:
                    if numCasas in range(1, 5):
                        string += f'Esta propriedade tem **{numCasas} casas**, então você terá que **pagar mais que o normal**. O valor para esta propriedade **com {numCasas} casas** é de **{formatarDinheiro(preço)}**'
                    else:
                        string += f'Esta propriedade tem a **MAÇÃ DA APPLE** mais **4 casas**, então você **pagará CARO para caralho**, o valor será de **{formatarDinheiro(preço)}**'
            elif tipo == 'meme':
                preçoCasa = casas[casa][3]
                outrosMemes = preço/preçoCasa
                if outrosMemes == 1:
                    string += f'Como {jogo[dono]["nome"]} **só tem esse MEME SUECO** você pagará o valor nominal de **{formatarDinheiro(preço)}**'
                else:
                    string += f'Como {jogo[dono]["nome"]} **tem mais {outrosMemes*8:.0f} MEMES SUECOS** você pagará o valor de **{formatarDinheiro(preço)}**'
            elif tipo == 'monstro':
                contador = 0
                for posse in jogo[dono]['posses']:
                    for i in range(0, 2):
                        if posse == casas[casa][4][i]:
                            contador += 1
                pagar = ''
                if contador == 1:
                    string += f'Como {jogo[dono]["nome"]} **tem somente {casas[casa][0]}** você **pagará o valor do dado jogado multiplicado por 40k**. Resultando em **{formatarDinheiro(preço)}**'
                elif contador == 2:
                    if casas[casa][4][0] == casa:
                        outraCasa = casas[casa][4][1]
                    else:
                        outraCasa = casas[casa][4][0]
                    string += f'Como {jogo[dono]["nome"]} **tem {casas[casa][0]} e {casas[outraCasa][0]}** você **pagará o valor do dado jogado multiplicado por 100k**. Resultando em **{formatarDinheiro(preço)}**'
    return string


'''
    Verificadores globais
'''

verificaComeco = False
verificaJogo = False
jogoRolando = False


class Monopoly(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Eventos
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog Monopoly está pronta')

    def verificadorComeco(ctx):
        global verificaComeco
        if verificaComeco:
            return True
        else:
            return False

    def verificaJogo(ctx):
        global verificaJogo
        if verificaJogo:
            return True
        else:
            return False


    @commands.command(aliases=['começarMonopoly', 'comecarmonopoly', 'começarmonopoly', 'cm'])
    async def comecarMonopoly(self, ctx, numJogador):
        global verificaComeco, numJogadores, escolhidas, jogoRolando
        if jogoRolando is True:
            await ctx.send(f'Já tem um jogo rolando, {ctx.author.mention}!\nEncerre este jogo para começar outro.')
        else:
            tupla = analisaNumJogadores(numJogador)
            verifica = tupla[0]
            string = tupla[1]
            if verifica:
                await ctx.send(string + f'Inicializando jogo...')

                escolhidas = []
                numJogadores = int(numJogador)
                verificaComeco = True

                string = f'Cores disponíveis: Vermelho, Amarelo, Azul, Verde\n' \
                         f'Digite ".escolher (cor)" para setar uma cor!'
                await ctx.send(string)
            else:
                await ctx.send(string)
        #inicializar()


    @commands.command(aliases=['es'])
    @commands.check(verificadorComeco)
    async def escolher(self, ctx, cor):
        global escolhidas, numJogadores, verificaComeco, verificaJogo, pastaProjeto, jogoRolando
        if jogoRolando is True:
            await ctx.send(f'Já tem um jogo rolando, {ctx.author.mention}!\nEncerre este jogo, comece outro e ai você poderá escolher uma cor.')
        else:
            jáescolheu = False
            for escolhida in escolhidas:
                escolhacor, escolhanome, escolhaid = escolhida.split(',')
                id = int(escolhaid)
                if id == ctx.author.id:
                    jáescolheu = True
            if jáescolheu:
                await ctx.send(f'{escolhanome}, você já escolheu **{escolhacor.title()}**. Se quiser escolher outra tente .comecarMonopoly')
            else:
                await ctx.send(f'Analisando {cor}...')
                analise = analisaCor(cor)
                if analise == 'invalido':
                    await ctx.send('Cor inválida! Digite uma válida')
                elif analise == 'escolhida':
                    await ctx.send('Cor já escolhida!')
                else:
                    string = f'{analise},{ctx.author.mention},{ctx.author.id}'
                    escolhidas.append(string)
                    tamanho = len(escolhidas)
                    cor, nome, id = escolhidas[tamanho-1].split(',')
                    await ctx.send(f'A cor **{cor.upper()}** agora está setada a {nome}')
                    if numJogadores == tamanho:
                        await ctx.send(f'Todos já escolheram, sorteando ordem de jogo...')
                        random.shuffle(escolhidas)

                        string = ''
                        for i in range(0, numJogadores):
                            ecor, enome, eid = escolhidas[i].split(',')
                            string += f'{enome} de cor **{ecor.upper()}** será o **{i + 1}º a jogar**\n\n'
                        verificaJogo = True
                        string += f'Digite **".m opções"** para ver as **opções disponíveis** para você jogar'

                        await ctx.send(string)
                        inicializar()
                        path = pastaProjeto + '/imagens/monopoly/gamepeao.png'
                        file = discord.File(path, filename="thumbAtual.png")
                        await ctx.send(file=file)

                        ecor, enome, eid = escolhidas[0].split(',')
                        await ctx.send(f'É a vez de {enome} de cor **{ecor.upper()}**')


    @commands.command()
    @commands.check(verificaJogo)
    async def m(self, ctx, *, parâmetro):
        global atual, jogo, escolhidas, inicioJogada, mverifica, desistencia, finalizacao, idProximoAVotarFinalização
        global pastaProjeto, casas, numJogadores, desistente, desistentes, habilitarDevedor, ultimoAJogar, tempoDados
        global perdedores, vendaInfo, contaM, estacionamentoUnico, ultimoAReceberEstacionamento
        nãoEntendi = False
        jogador = ''
        for membro, valor in jogo.items():
            if jogo[membro]['id'] == ctx.author.id:
                jogador = membro
                break
        if jogador != '':
            parâmetro = parâmetro.strip().lower()
            parâmetroOriginal = parâmetro
            parâmetro = parâmetroOriginal.split(' ')
            parâmetro = parâmetro[0]
            parâmetro = parâmetro.replace(' ', '')
            arredondaDinheiro()
            if finalizacao is False:
                opçõesDoAtual = 'usarcartãousarcartaodispotecardesipotecardeshipotecarjogardadosrolardadosroletardadosnessabucetaroletaressabucetaroletarnessabucetajogarnessabucetajogarnessecaraiocompraradquirirpurchaseokpassarvezprontopagarpagamentoimposto'
                ''' JOGADOR DA VEZ, OPÇÕES DELE: '''
                if jogador == atual[0]:
                    # Para entender o motivo, olhar imagem 'sorte18'
                    if jogo[jogador]['status'] == 'oi':
                        if parâmetro not in 'oimeuchapaolámeuchapaolameuchapa':
                            acabou = retiraJogador(jogador, 'banco', True)
                            if acabou is True:
                                string = encerraJogo()
                                await ctx.send(string)
                            else:
                                await ctx.send(f'**{perdedores[jogador]["nome"]} não faz mais parte do jogo!**')
                        else:
                            jogo[jogador]['status'] = 'sorteq'
                    else:
                        disponiveis = analisaAcoes(jogador, jogo[jogador]['dado'])
                        if parâmetro in 'jogojoagrjogaarjogardadosrolardadosroletardadosnessabucetaroletaressabucetaroletarnessabucetajogarnessabucetajogarnessecaraio':
                            if inicioJogada is True:
                                if jogo[jogador]['status'] == 'preso':
                                    if parâmetro == parâmetroOriginal:
                                        await ctx.send('Você está com **depressão**, para sair escreva **.m jogar (num1) (num2)** sendo num1 e num2 número de 1 a 6\nExemplo: .m jogar 1 6\n\nApós a jogada, o computador irá escolher 1 número de 1 a 6 totalmente aleatório, se um dos seus números for igual você sai da depressão')
                                    else:
                                        params = parâmetroOriginal.split(' ')
                                        del params[0]
                                        if len(params) == 2:
                                            if params[0].isnumeric() and params[1].isnumeric():
                                                num1 = int(params[0])
                                                num2 = int(params[1])
                                                if num1 in range(1, 7):
                                                    if num2 in range(1, 7):
                                                        num = random.randint(1, 6)
                                                        await ctx.send('**Sorteando número aleatório... **')
                                                        sleep(tempoDados)
                                                        await ctx.send(f'Os número sorteado foi: **{num}**')
                                                        if num1 == num or num2 == num:
                                                            await ctx.send(f'**FIRMARMANT!**, {jogo[jogador]["nome"]} encontrou a luz do fim do túnel e venceu a depressor \( ﾟヮﾟ)/')
                                                            jogo[jogador]['casa'] = 10
                                                            jogo[jogador]['status'] = "livre"
                                                            inicioJogada = False
                                                        else:
                                                            await ctx.send(f'{jogo[jogador]["nome"]} ainda é **sad boy (´༎ຶ༎ຶ)** :sangue:')
                                                            inicioJogada = False
                                                    else:
                                                        await ctx.send('O segundo número digitado não está no intervalo de 1 a 6')
                                                else:
                                                    await ctx.send('O primeiro número digitado não está no intervalo de 1 a 6')
                                            else:
                                                await ctx.send('Um ou mais números não estão escritos no formato inteiro legível\nO formato inteiro legível são números como: 1, 3, 6\nLeve em conta também que os números tem que estar necessariamente entre 1 e 6')
                                        else:
                                            await ctx.send('Você passou mais que dois parâmetros permitidos em .m jogar')
                                elif jogo[jogador]['comando'] == 'jogar':
                                    dados = random.randint(1, 6)
                                    await ctx.send('Rolando dados, por favor aguarde...')
                                    sleep(tempoDados)
                                    await ctx.send(f'O dado deu {dados}')
                                    if type(jogo[jogador]["pcomando"]) == tuple:
                                        opc = jogo[jogador]["pcomando"][0]
                                        if opc == 'pagar1':
                                            produto = jogo[jogador]['pcomando'][1]
                                            cobrador = jogo[jogador]['pcomando'][2]
                                            jogo[jogador]["pcomando"] = ('pagar', dados * produto, cobrador)
                                            valorDevido = dados*produto
                                            await ctx.send(f'Multiplicando {dados} por 200K você deve **{formatarDinheiro(valorDevido)}** a {jogo[cobrador]["nome"]}\n'
                                                           f'Escreva **.m pagar** para pagar')
                                    else:
                                        if jogo[jogador]['pcomando'] == 'receber1':
                                            if dados == 6:
                                                tupla = ('receber', 1)
                                                transacao(tupla, jogador)
                                                await ctx.send(f'Você ficou em **1º lugar na competição** e recebeu **$1M**\nSua grana: **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')
                                            elif dados == 5:
                                                tupla = ('receber', 1)
                                                transacao(tupla, jogador)
                                                await ctx.send(f'Você ficou em **2º lugar na competição** e recebeu **$500k**\nSua grana: **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')
                                            elif dados == 4:
                                                tupla = ('receber', 1)
                                                transacao(tupla, jogador)
                                                await ctx.send(f'Você ficou em **3º lugar na competição** e recebeu **$250k**\nSua grana: **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')
                                            else:
                                                await ctx.send(f'Você não foi amante o suficiente na competição dos **amantes de teclar no aparelho computadorizado**')
                                            jogo[jogador]['status'] == 'sorteq'
                                        inicioJogada = False
                                else:
                                    inicioJogada = False
                                    casaAntiga = jogo[jogador]["casa"]
                                    tupla = jogar(jogador)
                                    passouPeloInicio = tupla[1]
                                    jogo[jogador]['dado'] = tupla[0]

                                    acoes = analisaAcoes(jogador, jogo[jogador]['dado'])
                                    #  troca o status do jogador se ele é obrigado a pagar algo
                                    try:
                                        tupla = acoes[0][0][1]
                                        if tupla[0] == 'pagar':
                                            jogo[jogador]['status'] = 'devedor'
                                    except:
                                        ''' :except'''

                                    # Lerdeia o tempo de propósito para dar uma gracinha
                                    await ctx.send('Jogando dado, por favor aguarde...')
                                    sleep(tempoDados)
                                    await ctx.send(f'O dado deu {jogo[jogador]["dado"]}')

                                    # ENVIA A IMAGEM DO TABULEIRO PARA TODOS
                                    modificaGamepeao(jogador, casaAntiga)

                                    path = f'{pastaProjeto}/imagens/monopoly/gamepeao.png'
                                    file = discord.File(path, filename='gamepeao.png')
                                    await ctx.send(file=file)

                                    # ENVIA A THUMB DA CASA DA ONDE O JOGADOR CAIU COM UMA MENSAGEM PERSONALIZADA
                                    mensagem = thumbCasa(jogo[jogador]['casa'])
                                    path = pastaProjeto
                                    path += '/imagens/monopoly/temp/thumbAtual.png'
                                    file = discord.File(path, filename="thumbAtual.png")
                                    await ctx.send(mensagem)
                                    await ctx.send(file=file)

                                    if passouPeloInicio is True:
                                        await ctx.send(f'Como {jogo[jogador]["nome"]} passou pelo início, ele recebeu $2M')

                                    string = voceCaiu(jogador, jogo[jogador]["casa"])
                                    await ctx.send(string)

                                    # Analisa se o que o jogador pegou para pagar vai fazer ele perder
                                    if jogo[jogador]['status'] == 'devedor':
                                        preço = acoes[0][1]
                                        cobrador = acoes[0][2]
                                        semPosses = False
                                        valorTotal = 0
                                        for posse in jogo[jogador]['posses']:
                                            if casas[posse][2] == 'lote':
                                                valorTotal += (casas[posse][4][0] / 2)
                                            else:
                                                valorTotal += (casas[posse][3] / 2)
                                        if valorTotal < preço:
                                            for i in range(0, len(jogo[jogador]['posses'])):
                                                posse = jogo[jogador]['posses'][i]
                                                casas[posse][1] = None
                                            jogo[jogador]['dinheiro'] += valorTotal
                                        if len(jogo[jogador]['posses']) == 0:
                                            semPosses = True
                                        if not habilitarDevedor:
                                            if jogo[jogador]['dinheiro'] < preço and semPosses:
                                                restoDinheiro = jogo[jogador]["dinheiro"]
                                                finalizarJogo = retiraJogador(jogador, cobrador)
                                                if cobrador == 'banco':
                                                    await ctx.send(f'Infelizmente você não tem posses e nem dinheiro para pagar o **banco**, **{perdedores[jogador]["nome"]}, VOCÊ PERDEU, TODO RESTO DO SEU DINHEIRO ({formatarDinheiro(restoDinheiro)}) FOI DADO A ELE E VOCÊ FOI RETIRADO DO JOGO**')
                                                else:
                                                    await ctx.send(f'Infelizmente você não tem posses e nem dinheiro para pagar {jogo[cobrador]["nome"]}, **{perdedores[jogador]["nome"]}, VOCÊ PERDEU, TODO RESTO DO SEU DINHEIRO ({formatarDinheiro(restoDinheiro)}) FOI DADO A ELE E VOCÊ FOI RETIRADO DO JOGO**')
                                                if finalizarJogo:
                                                    for jogador in jogo.keys():
                                                        await ctx.send(f'Como só sobrou {jogo[jogador]["nome"]}, **O JOGO FOI FINALIZADO**')
                                                    string = encerraJogo()
                                                    await ctx.send(string)
                                                    return
                                                else:
                                                    string = passaAtual()
                                                    await ctx.send(string)

                                    # ENDER PEARL GANHARIA
                                    randomico = random.randint(1, 5000)
                                    if randomico == 2000:
                                        jogo[jogador]['cartoes']['ender'] = True
                                        await ctx.send(f'**  PAREM TODOS!!!\n\nO {jogo[jogador]["nome"]} ganhou uma ender pearl. Agora quando quiser poderá usá-la para se transportar a uma casa aleatória')

                                    # ESTACIONAMENTO GANHARIA
                                    if 'estacionamento' in acoes:
                                        string = ''
                                        jogo[jogador]['cartoes']['estacionamento'] = True
                                        acoes.remove('estacionamento')
                                        if ultimoAReceberEstacionamento != '' and estacionamentoUnico:
                                            ucor = ultimoAReceberEstacionamento
                                            string += f'Devido a isso, {jogo[ucor]["nome"]} perdeu seu sugar daddy. Porque em tempos de crise o papai só pode sustentar um bebê por vez.'
                                            jogo[ucor]['cartoes']['estacionamento'] = False
                                            ultimoAReceberEstacionamento = jogador
                                            await ctx.send(string)
                                        else:
                                            ultimoAReceberEstacionamento = jogador
                                    # STRING QUE PÕE NA TELA AS OPÇÕES
                                    string = ''
                                    for i in range(0, len(acoes)):
                                        palavra = acoes[i]
                                        try:
                                            palavra = palavra.title()
                                        except:
                                            palavra = palavra[0]
                                        finally:
                                            if i + 1 == len(acoes):
                                                string += f'{palavra.title()}.'
                                            else:
                                                string += f'{palavra.title()}, '

                                    await ctx.send(f'Suas opções são: {string}')
                            else:
                                await ctx.send('Você já jogou! Se quiser passar a vez escreva **.m ok**')
                        elif parâmetro in 'cmcompraradquirirpurchasecmoprabuy' and parâmetro not in "op":
                            # Caso o jogador não possa comprar
                            try:
                                opcao = disponiveis[0][0][1]
                                opcao = disponiveis[0][0]
                            except:
                                await ctx.send(f'Você não pode comprar nada, {jogo[jogador]["nome"]}')
                            else:
                                # ANALISA SE O JOGADOR ESTÁ COMPRANDO FORA DA OPÇÃO DE COMPRA
                                if opcao in 'comprar':
                                    # SE A OPÇÃO DE COMPRA É COMPRAR UMA NOVA POSSE
                                    if disponiveis[0][3] == 'posse':
                                        dinheiroAnterior = jogo[jogador]['dinheiro']
                                        transacao(disponiveis[0], jogador)
                                        casa = jogo[jogador]['casa']
                                        await ctx.send(f'Você comprou **{casas[casa][0]}**\nDinheiro de antes: **{formatarDinheiro(dinheiroAnterior)}**\nDinheiro de agora: **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')
                                        file = discord.File(pastaProjeto + f'/imagens/monopoly/thumbs/{casa}.png', filename=f'{casa}.png')
                                        await ctx.send(file=file)

                                    elif disponiveis[0][3] == 'mais casas':
                                        dinheiroAnterior = jogo[jogador]['dinheiro']
                                        transacao(disponiveis[0], jogador)
                                        casa = disponiveis[0][1]
                                        string = ''
                                        if casas[casa][3] == 1:
                                            string = 'a primeira casa'
                                        elif casas[casa][3] == 2:
                                            string = 'a segunda casa'
                                        elif casas[casa][3] == 3:
                                            string = 'a terceira casa'
                                        elif casas[casa][3] == 4:
                                            string = 'a quarta casa'
                                        elif casas[casa][3] == 5:
                                            string = 'A MACA DA APPLE'
                                        await ctx.send(f'Você comprou **{string}** para sua propriedade "**{casas[casa][0]}**", agora quem cair nela estará fodido\nDinheiro de antes: **{formatarDinheiro(dinheiroAnterior)}**\nDinheiro de agora: **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')
                                        modificaCasas(jogador, casa)
                                        mensagem = thumbCasa(casa=casa, thumbCompraCasa=True)
                                        file = discord.File(pastaProjeto + '/imagens/monopoly/temp/thumbAtual.png', filename='thumbAtual.png')
                                        await ctx.send(file=file)
                                        if casas[casa][3] == 5:
                                            file = discord.File(pastaProjeto + f'/imagens/monopoly/casas/apple {jogador}.jpg', filename=f'apple {jogador}.jpg')
                                            await ctx.send(file=file)
                                    jogo[jogador]['status'] = 'comprador'
                                else:
                                    await ctx.send(f'Você não pode comprar nada, {jogo[jogador]["nome"]}')
                        elif parâmetro in 'pagarpagamentoimpostopay' and parâmetro not in 'opos':
                            try:
                                opcao = disponiveis[0][0][1]
                                opcao = disponiveis[0][0]
                            except:
                                await ctx.send(f'Você tem nada para pagar, {jogo[jogador]["nome"]}')
                            else:
                                # ANALISA SE O JOGADOR ESTÁ COMPRANDO FORA DA HORA DE PAGAR
                                if opcao in 'pagar':
                                    tupla = disponiveis[0]
                                    preço = tupla[1]
                                    cobrador = tupla[2]
                                    if cobrador in 'banco':
                                        cobrador = 'o banco'
                                    preço = float(preço)
                                    if preço > jogo[jogador]['dinheiro']:
                                        if habilitarDevedor:
                                            transacao(tupla, jogador)
                                            await ctx.send(
                                                f'{jogo[jogador]["nome"]} pagou {formatarDinheiro(preço)} para **{cobrador}** e ficou mais pobre ainda.\n\n{jogo[jogador]["nome"]}, sua grana atual é: {jogo[jogador]["dinheiro"]}')
                                        else:
                                            await ctx.send(f'{jogo[jogador]["nome"]} você não tem dinheiro suficiente para pagar. Mas ainda pode hipotecar algo, tente **.m hipotecar** para ver opções')
                                            jogo[jogador]['status'] = 'devedor'
                                    else:
                                        transacao(tupla, jogador)
                                        if cobrador not in 'o bancotodos':
                                            await ctx.send(f'{jogo[jogador]["nome"]} pagou {formatarDinheiro(preço)} para **{jogo[cobrador]["nome"]}**\n\n{jogo[jogador]["nome"]}, sua grana atual é: {formatarDinheiro(jogo[jogador]["dinheiro"])}')
                                        else:
                                            await ctx.send(f'{jogo[jogador]["nome"]} pagou {formatarDinheiro(preço)} para **{cobrador}**\n\n{jogo[jogador]["nome"]}, sua grana atual é: {formatarDinheiro(jogo[jogador]["dinheiro"])}')
                                        jogo[jogador]['status'] = 'pagador'
                                else:
                                    await ctx.send(f'Você tem nada para pagar, {jogo[jogador]["nome"]}')
                        elif parâmetro in 'hipotecar':
                            if 'hipotecar' not in disponiveis:
                                await ctx.send(f'Você não tem nada para hipotecar, {jogo[jogador]["nome"]}!')
                            else:
                                if parâmetroOriginal == parâmetro:  # Se o jogador só escrever .m hip
                                    string = f'{jogo[jogador]["nome"]}, suas posses disponíveis para hipoteca são: \n'
                                    for posse in jogo[jogador]['posses']:
                                        tipo = casas[posse][2]
                                        if tipo == 'lote':
                                            valor = casas[posse][4][0]/2
                                        elif tipo == 'meme':
                                            valor = 1
                                        elif tipo == 'monstro':
                                            valor = 0.75
                                        string += f'**Nº{posse}** - **{casas[posse][0]}** - valor da hipoteca: **{formatarDinheiro(valor)}**\n'
                                    await ctx.send(string)
                                else:
                                    parâmetroOriginal = parâmetroOriginal.split(' ')
                                    del parâmetroOriginal[0]
                                    parâmetroOriginal = ' '.join(parâmetroOriginal)
                                    carta = parâmetroOriginal.replace(' ', '')
                                    try:
                                        carta = int(carta)
                                    except:
                                        lista = ['01augusta',
                                                 '03botinha',
                                                 '05amoteclarnomeuaparelhocomputadorizadoadoroteclarnomeuaparelhocomputadorizado',
                                                 '06rata',
                                                 '08cemitériodebogacemiteriodebogacemitériodebigcemiteriodebig',
                                                 '09cemiteriodeguardiaocemitériodeguardiãocemitériodeguardiaocemiteriodeguardiãocemiteriodezezoiacemitériodezezoiacemiteriodesequoiacemitériodesequoiacemiteriodesequóiacemitériodesequóiacemiteriodecardiamcemitériodecardiam',
                                                 '11não-me-toquenãometoquenaometoque',
                                                 '12tocufomiiiiiiiiiiiiitocufomeestoucufomitocomfomitocomfometôcomfometocomfomitocufomeeeeeeeeeeeee',
                                                 '13sumarésumarecidadedebogcidadedoboga',
                                                 '14thefloatingdeadsãopaulosaopaulocidadedogapigocidadedoguardião',
                                                 '15carpediem',
                                                 '16nárnianarnia',
                                                 '18groelândiagroelandia',
                                                 '19acre',
                                                 '21casadocaralhocasadokrlcasadocrlcasadocaraiocasadukrlcasaducrl',
                                                 '23bankheist',
                                                 '24orbitaldogapigo',
                                                 '25cancercurativocâncercurativoquemçacurativocancercuratifocamcercurativo',
                                                 '26chernobylachernobilachernobylchernobil',
                                                 '27cavernadasperanhascavernadaspiranhas',
                                                 '28chupacu',
                                                 '29universidadeesquerdistauniversidadeenqueditauniversidadedosenqueditasuniversidadedosesquerdistasuniversidadedeenqueditauniversidadedeesquerdista',
                                                 '31refúgiodonegoneyrefugiodonegoneyrefujiodonegoneyrefúgiodonegoneirefugiodonegoney',
                                                 '32santuáriododorimesantuariododorime',
                                                 '34mansãodoricardãomansaodoricardaomansãodoricardaomansaodoricardãomansãodoricardomilosmansaodoricardomilos',
                                                 '35cooldecuriosocudecurioso',
                                                 '37infernocasadozezoiacasadoguardião',
                                                 '39buraconegrocudobig']
                                        cartaAntigo = carta
                                        for string in lista:
                                            if carta in string:
                                                carta = int(string[0:2])
                                                break
                                        if carta == cartaAntigo:
                                            await ctx.send(f'A carta que você quer hipotecar não existe ou é inacessível, {jogo[jogador]["nome"]}')
                                            return
                                    finally:
                                        if carta in range(1, 41):
                                            if carta not in [2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38]:
                                                if carta not in jogo[jogador]['posses']:
                                                    await ctx.send(f'Você não pode hipotecar essa carta porque você não possui ela ou ela já está hipotecada, {jogo[jogador]["nome"]}')
                                                else:
                                                    tipo = casas[carta][2]
                                                    if tipo == 'lote':
                                                        valor = casas[carta][4][0]/2
                                                    elif tipo == 'meme':
                                                        valor = 1
                                                    elif tipo == 'monstro':
                                                        valor = 0.75
                                                    hipoteca(jogador, carta)
                                                    file = discord.File(
                                                        pastaProjeto + f'/imagens/monopoly/thumbs/{carta}.png')
                                                    await ctx.send(file=file)
                                                    await ctx.send(f'**{casas[carta][0]}** foi hipotecada, você ganhou **{formatarDinheiro(valor)}**')
                                            else:
                                                await ctx.send(f'A carta é inacessível, {jogo[jogador]["nome"]}')
                                        else:
                                            await ctx.send(f'A carta não existe, {jogo[jogador]["nome"]}')
                        elif parâmetro in 'dispotecardesipotecardeshipotecar':
                            if 'desipotecar' not in disponiveis:
                                await ctx.send(f'Você não tem nada para desipotecar, {jogo[jogador]["nome"]}!')
                            else:
                                if parâmetroOriginal == parâmetro:  # Se o jogador só escrever .m desip ou deship
                                    string = f'{jogo[jogador]["nome"]}, suas hipotecas disponíveis para desipotecar são: \n'
                                    for posse in jogo[jogador]['hipotecados']:
                                        tipo = casas[posse][2]
                                        if tipo == 'lote':
                                            valor = casas[posse][4][0]
                                        elif tipo == 'meme':
                                            valor = 1
                                        elif tipo == 'monstro':
                                            valor = 0.75
                                        string += f'**Nº{posse}** - **{casas[posse][0]}** - valor retornado na desipoteca: **{formatarDinheiro(valor)}**\n'
                                    await ctx.send(string)
                                else:
                                    parâmetroOriginal = parâmetroOriginal.split(' ')
                                    del parâmetroOriginal[0]
                                    parâmetroOriginal = ' '.join(parâmetroOriginal)
                                    carta = parâmetroOriginal.replace(' ', '')
                                    try:
                                        carta = int(carta)
                                    except:
                                        lista = ['01augusta',
                                                 '03botinha',
                                                 '05amoteclarnomeuaparelhocomputadorizadoadoroteclarnomeuaparelhocomputadorizado',
                                                 '06rata',
                                                 '08cemitériodebogacemiteriodebogacemitériodebigcemiteriodebig',
                                                 '09cemiteriodeguardiaocemitériodeguardiãocemitériodeguardiaocemiteriodeguardiãocemiteriodezezoiacemitériodezezoiacemiteriodesequoiacemitériodesequoiacemiteriodesequóiacemitériodesequóiacemiteriodecardiamcemitériodecardiam',
                                                 '11não-me-toquenãometoquenaometoque',
                                                 '12tocufomiiiiiiiiiiiiitocufomeestoucufomitocomfomitocomfometôcomfometocomfomitocufomeeeeeeeeeeeee',
                                                 '13sumarésumarecidadedebogcidadedoboga',
                                                 '14thefloatingdeadsãopaulosaopaulocidadedogapigocidadedoguardião',
                                                 '15carpediem',
                                                 '16nárnianarnia',
                                                 '18groelândiagroelandia',
                                                 '19acre',
                                                 '21casadocaralhocasadokrlcasadocrlcasadocaraiocasadukrlcasaducrl',
                                                 '23bankheist',
                                                 '24orbitaldogapigo',
                                                 '25cancercurativocâncercurativoquemçacurativocancercuratifocamcercurativo',
                                                 '26chernobylachernobilachernobylchernobil',
                                                 '27cavernadasperanhascavernadaspiranhas',
                                                 '28chupacu',
                                                 '29universidadeesquerdistauniversidadeenqueditauniversidadedosenqueditasuniversidadedosesquerdistasuniversidadedeenqueditauniversidadedeesquerdista',
                                                 '31refúgiodonegoneyrefugiodonegoneyrefujiodonegoneyrefúgiodonegoneirefugiodonegoney',
                                                 '32santuáriododorimesantuariododorime',
                                                 '34mansãodoricardãomansaodoricardaomansãodoricardaomansaodoricardãomansãodoricardomilosmansaodoricardomilos',
                                                 '35cooldecuriosocudecurioso',
                                                 '37infernocasadozezoiacasadoguardião',
                                                 '39buraconegrocudobig']
                                        cartaAntigo = carta
                                        for string in lista:
                                            if carta in string:
                                                carta = int(string[0:2])
                                                break
                                        if carta == cartaAntigo:
                                            await ctx.send(f'A carta que você quer desipotecar não existe ou é inacessível, {jogo[jogador]["nome"]}')
                                            return
                                    finally:
                                        if carta in range(1, 41):
                                            if carta not in [2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38]:
                                                if carta not in jogo[jogador]['hipotecados']:
                                                    await ctx.send(f'Você não pode desipotecar essa casa porque você não tem essa carta hipotecada, {jogo[jogador]["nome"]}')
                                                else:
                                                    tipo = casas[carta][2]
                                                    valor = 0
                                                    if tipo == 'lote':
                                                        valor = casas[carta][4][0]
                                                    elif tipo == 'meme':
                                                        valor = 1
                                                    elif tipo == 'monstro':
                                                        valor = 0.75
                                                    if jogo[jogador]['dinheiro'] >= valor:
                                                        hipoteca(jogador, carta, True)
                                                        file = discord.File(
                                                            pastaProjeto + f'/imagens/monopoly/thumbs/{carta}.png')
                                                        await ctx.send(file=file)
                                                        await ctx.send(f'**{casas[carta][0]}** foi desipotecada, você pagou **{formatarDinheiro(valor)}** na desipoteca.\nSeu dinheiro atual: {formatarDinheiro(jogo[jogador]["dinheiro"])}')
                                                    else:
                                                        await ctx.send(f'{jogo[jogador]["nome"]}, você precisa de **{formatarDinheiro(valor)}** para desipotecar **{casas[carta][0]}** e você só tem **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')
                                            else:
                                                await ctx.send(f'A carta é inacessível, {jogo[jogador]["nome"]}')
                                        else:
                                            await ctx.send(f'A carta não existe, {jogo[jogador]["nome"]}')
                        elif parâmetro in 'usarcartãousarcartao':
                            if 'usar' in disponiveis:
                                if parâmetro == parâmetroOriginal:
                                    string = f'**SEUS OBJETOS DE USO DISPONÍVEIS, {jogo[jogador]["nome"]}:\n'
                                    string += '\nCód - OBJETO               - FUNÇÃO\n'
                                    if jogo[jogador]['cartoes']['cadeia'] is True:
                                        string += 'Nº1 - Anti-depressivo - Te tira da depressão"\n'
                                    if jogo[jogador]['cartoes']['estacionamento'] is True:
                                        string += 'Nº2 - Sugar Daddy     - Paga para você o que você quiser"\n'
                                    if jogo[jogador]['cartoes']['ender'] is True:
                                        string += 'Nº3 - Ender Pearl        - Te teleporta para onde você quiser\n'
                                    await ctx.send(string)
                                else:
                                    params = parâmetroOriginal.split(' ')
                                    del params[0]
                                    param = ''
                                    for p in params:
                                        param += p
                                    if 'ender' in param or 'enderpearl' in param:
                                        ender = jogo[jogador]['cartoes']['ender']
                                        if not ender:
                                            await ctx.send('Você não pode usar a ender pearl porque não a tem!!!!')
                                        else:
                                            params = parâmetroOriginal
                                            params = parâmetroOriginal.split(' ')
                                            if 'ender' in param and 'pearl' not in param:
                                                del params[0]
                                                del params[0]
                                            elif 'ender' in param and 'pearl' in param:
                                                del params[0]
                                                del params[0]
                                                del params[0]
                                            param = ''.join(params)
                                            try:
                                                achou = False
                                                x = int(params[0])
                                            except:
                                                lista = ['00inicioiníciocomeçocomecoreceba$2mreceba2m',
                                                         '01augusta',
                                                         '02caixalazarenta',
                                                         '03botinha',
                                                         '04impostoérouboimpostoeroubo',
                                                         '05amoteclarnomeuaparelhocomputadorizadoadoroteclarnomeuaparelhocomputadorizado',
                                                         '06rata',
                                                         '07sortedoguardião',
                                                         '08cemitériodebogacemiteriodebogacemitériodebigcemiteriodebig',
                                                         '09cemiteriodeguardiaocemitériodeguardiãocemitériodeguardiaocemiteriodeguardiãocemiteriodezezoiacemitériodezezoiacemiteriodesequoiacemitériodesequoiacemiteriodesequóiacemitériodesequóiacemiteriodecardiamcemitériodecardiam',
                                                         '11não-me-toquenãometoquenaometoque',
                                                         '12tocufomiiiiiiiiiiiiitocufomeestoucufomitocomfomitocomfometôcomfometocomfomitocufomeeeeeeeeeeeee',
                                                         '13sumarésumarecidadedebogcidadedoboga',
                                                         '14thefloatingdeadsãopaulosaopaulocidadedogapigocidadedoguardião',
                                                         '15carpediem',
                                                         '16nárnianarnia',
                                                         '17cofre',
                                                         '18groelândiagroelandia',
                                                         '19acre',
                                                         '20sugardaddy',
                                                         '21casadocaralhocasadokrlcasadocrlcasadocaraiocasadukrlcasaducrl',
                                                         '23bankheist',
                                                         '24orbitaldogapigo',
                                                         '25cancercurativocâncercurativoquemçacurativocancercuratifocamcercurativo',
                                                         '26chernobylachernobilachernobylchernobil',
                                                         '27cavernadasperanhascavernadaspiranhas',
                                                         '28chupacu',
                                                         '29universidadeesquerdistauniversidadeenqueditauniversidadedosenqueditasuniversidadedosesquerdistasuniversidadedeenqueditauniversidadedeesquerdista',
                                                         '30ihavecripplingdepression',
                                                         '31refúgiodonegoneyrefugiodonegoneyrefujiodonegoneyrefúgiodonegoneirefugiodonegoney',
                                                         '32santuáriododorimesantuariododorime',
                                                         '33caixadepandora',
                                                         '34mansãodoricardãomansaodoricardaomansãodoricardaomansaodoricardãomansãodoricardomilosmansaodoricardomilos',
                                                         '35cooldecuriosocudecurioso',
                                                         '36sortedezezoiasortedasequoiasortedesequoia',
                                                         '37infernocasadozezoiacasadoguardião',
                                                         '38coerçãoestatalcoercaoestatal'
                                                         '39buraconegrocudobig']
                                                for string in lista:
                                                    if param in string:
                                                        param = int(string[0:2])
                                                        achou = True
                                                        break
                                            else:
                                                param = int(params[0])
                                                if param in range(0, 40):
                                                    achou = True
                                            finally:
                                                if jogo[jogador]['status'] == 'comprador':
                                                    await ctx.send('Não é possível usar a ender pearl, porque você já comprou algo esse turno!')
                                                elif achou is True:
                                                    jogo[jogador]['status'] = 'livre'
                                                    jogo[jogador]['casa'] = param
                                                    jogo[jogador]['cartoes']['ender'] = False
                                                    await ctx.send(f'{jogo[jogador]["nome"]} foi teleportado a **{casas[param][0]}**')
                                                    thumbCasa(param)
                                                    path = pastaProjeto + '/imagens/monopoly/temp/thumbAtual.png'
                                                    file = discord.File(path, filename='thumbAtual.png')
                                                    await ctx.send(file=file)
                                                else:
                                                    await ctx.send('Não foi possível entender a casa para teleportar com a ender pearl!')
                                    else:
                                        if len(params) == 1 or len(params) == 2:
                                            try:
                                                param = int(param)
                                            except:
                                                param = param.strip().lower().replace(' ', '')
                                                lista = ['1antidepressivoanti-depressivoantidepressorantidepressãoad',
                                                         '2sugardaddysugardadaysugar-daddysugarbabysugardadysugardasy']
                                                achou = False
                                                for string in lista:
                                                    if param in string:
                                                        param = int(string[0])
                                                        achou = True
                                                        break
                                                if not achou:
                                                    await ctx.send('Este objeto não existe ou não foi possível entender o objeto corretamente')
                                            finally:
                                                cadeia = jogo[jogador]['cartoes']['cadeia']
                                                estacionamento = jogo[jogador]['cartoes']['estacionamento']
                                                if param == 1 and cadeia:
                                                    await ctx.send(f'{jogo[jogador]["nome"]} usou o seu anti-depresivo para escapar da depressão!')
                                                    casaJogador = jogo[jogador]["casa"]
                                                    if casaJogador == 30:
                                                        jogo[jogador]["status"] = 'usou'
                                                    elif casaJogador == 40:
                                                        jogo[jogador]["status"] = 'livre'
                                                        jogo[jogador]['casa'] = 10
                                                    jogo[jogador]['cartoes']['cadeia'] = False
                                                elif param == 2 and estacionamento:
                                                    if jogo[jogador]['status'] == 'devedor':
                                                        await ctx.send(f'{jogo[jogador]["nome"]} usou o seu sugar daddy para o bancar')
                                                        jogo[jogador]['status'] = 'pagador'
                                                        tupla = disponiveis[0]
                                                        valor = tupla[1]
                                                        cobrador = tupla[2]
                                                        tupla = ('receber', valor)
                                                        if cobrador != 'banco':
                                                            transacao(tupla, cobrador)
                                                        jogo[jogador]['cartoes']['estacionamento'] = False
                                                    else:
                                                        await ctx.send('O sugar daddy só pode ser usado para bancar despesas de pagamento')

                                                else:
                                                    await ctx.send('Você não tem o OBJETO que você quis usar')
                                        else:
                                            await ctx.send('O comando **.m usar** para antidepressivo ou sugar daddy aceita até 2 parâmetros após ele somente (separados por espaço) após ele\n**Exemplo: .m usar sugar daddy\nOu **.m usar anti depressivo**')
                            else:
                                await ctx.send(f'Você não tem OBJETOS DE USO para usar, {jogo[jogador]["nome"]}.')
                        elif parâmetro in 'caixacofrecaiaxcxia':
                            if 'caixa' in disponiveis:
                                await ctx.send('Abrindo caixa, por favor aguarde...')
                                sleep(tempoDados)
                                num = random.randint(1, 2000000)
                                if num != 2000:
                                    num = random.randint(1, 17)
                                    path = pastaProjeto + f'/imagens/monopoly/cofre/cofre{num}.png'
                                    file = discord.File(path, filename=f'cofre{num}.png')
                                    await ctx.send(file=file)
                                    tupla = caixa(num, jogador)

                                    # tupla = (casa, valor, cobrador, status, item, comando, string)
                                    casa = tupla[0]
                                    valor = tupla[1]
                                    cobrador = tupla[2]
                                    status = tupla[3]
                                    item = tupla[4]
                                    comando = tupla[5]
                                    string = tupla[6]

                                    casaAntiga = jogo[jogador]["casa"]
                                    jogo[jogador]["casa"] = casa
                                    if casa != casaAntiga:
                                        modificaGamepeao(jogador, casaAntiga)
                                        mensagem = thumbCasa(jogo[jogador]['casa'])
                                    if cobrador is None:
                                        if valor != 0:
                                            tupla2 = ('receber', valor)
                                            transacao(tupla2, jogador)
                                    jogo[jogador]["status"] = status
                                    if item != 0:
                                        if item == 1:
                                            jogo[jogador]['cartoes']['cadeia'] = True
                                        elif item == 2:
                                            jogo[jogador]['cartoes']['estacionamento'] = True
                                        elif item == 3:
                                            jogo[jogador]['cartoes']['ender'] = True
                                    jogo[jogador]['comando'] = comando
                                    if comando == 'pagar':
                                        jogo[jogador]['comando'] = 'pagar'
                                        tupla2 = ('pagar', valor, cobrador)
                                        jogo[jogador]['pcomando'] = tupla2
                                    if comando is not None:
                                        disponiveis = analisaAcoes(jogador)
                                    string = string.replace('suagrana', f'Sua grana atual é **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')

                                    await ctx.send(string)
                                    # Envia foto da casa atual do jogador com opções caso a sua case mude
                                    if casa != casaAntiga:
                                        file = discord.File(pastaProjeto + '/imagens/monopoly/temp/thumbAtual.png', filename='thumbAtual.png')
                                        sleep(tempoDados)
                                        await ctx.send(file=file)
                                        lista = analisaAcoes(jogador)
                                        if type(lista[0]) is tuple:
                                            string = f'{lista[0][0].title()}, '
                                            for i in range(1, len(lista)):
                                                palavra = lista[i]
                                                if i + 1 == len(lista):
                                                    string += f'{palavra.title()}.'
                                                else:
                                                    string += f'{palavra.title()}, '
                                        else:
                                            string = ''
                                            for i in range(0, len(lista)):
                                                palavra = lista[i]
                                                if i + 1 == len(lista):
                                                    string += f'{palavra.title()}.'
                                                else:
                                                    string += f'{palavra.title()}, '
                                        await ctx.send(f'Suas opções são: {string}')

                                else:
                                    path = pastaProjeto + '/imagens/monopoly/cofre/perder.png'
                                    file = discord.File(path, filename='perder.png')
                                    await ctx.send(file=file)
                                    await ctx.send('**MEU DEUS\n\nMEU DEUS\n\nAQUI É O GAPIGO PROGRAMANDO\n'
                                                   'NÃO ACREDITO... VOCÊ TIROU ISSO? MEEEEEE... BORA SE BENZER**')
                                    acabarJogo = retiraJogador(jogador, 'banco', True)
                                    if acabarJogo is True:
                                        await ctx.send('**O JOGO ESTÁ SENDO ENCERRADO POR FALTA DE JOGADORES**')
                                        string = encerraJogo()
                                        await ctx.send(string)
                                    return
                            else:
                                await ctx.send(f'Você não pode abrir uma **CAIXA LAZARENTA** agora {jogo[jogador]["nome"]}')
                        elif parâmetro in 'sorte':
                            if 'sorte' in disponiveis:
                                await ctx.send('Abrindo sorte secoial, por favor aguarde...')
                                sleep(tempoDados)
                                num = random.randint(1, 2000000)
                                if num != 2000:
                                    num = random.randint(1, 19)
                                    path = pastaProjeto + f'/imagens/monopoly/sorte/sorte{num}.png'
                                    file = discord.File(path, filename=f'sorte{num}.png')
                                    await ctx.send(file=file)
                                    casaAntiga = jogo[jogador]["casa"]
                                    tupla = sorte(num, jogador)

                                    # tupla = (casa, valor, cobrador, status, item, comando, string)
                                    casa = tupla[0]
                                    valor = tupla[1]
                                    cobrador = tupla[2]
                                    status = tupla[3]
                                    item = tupla[4]
                                    comando = tupla[5]
                                    string = tupla[6]

                                    jogo[jogador]["casa"] = casa
                                    if casa != casaAntiga:
                                        modificaGamepeao(jogador, casaAntiga)
                                        mensagem = thumbCasa(jogo[jogador]['casa'])

                                    if cobrador is None:
                                        if valor != 0:
                                            tupla2 = ('receber', valor)
                                            transacao(tupla2, jogador)
                                    jogo[jogador]["status"] = status
                                    if item != 0:
                                        if item == 1:
                                            jogo[jogador]['cartoes']['cadeia'] = True
                                        elif item == 2:
                                            jogo[jogador]['cartoes']['estacionamento'] = True
                                        elif item == 3:
                                            jogo[jogador]['cartoes']['ender'] = True
                                    jogo[jogador]['comando'] = comando
                                    if comando is not None:
                                        if comando in 'pagar1':
                                            if comando == 'pagar1':
                                                jogo[jogador]['comando'] = 'pagar1'
                                            else:
                                                jogo[jogador]['comando'] = 'pagar'
                                            tupla2 = ('pagar', valor, cobrador)
                                            jogo[jogador]['pcomando'] = tupla2
                                        disponiveis = analisaAcoes(jogador)
                                    string = string.replace('suagrana', f'Sua grana atual é **{formatarDinheiro(jogo[jogador]["dinheiro"])}**')
                                    await ctx.send(string)
                                    # Envia foto da casa atual do jogador com opções caso a sua case mude
                                    if casa != casaAntiga:
                                        file = discord.File(pastaProjeto + '/imagens/monopoly/temp/thumbAtual.png', filename='thumbAtual.png')
                                        sleep(tempoDados)
                                        await ctx.send(file=file)
                                        lista = analisaAcoes(jogador)
                                        if type(lista[0]) is tuple:
                                            string = f'{lista[0][0].title()}, '
                                            for i in range(1, len(lista)):
                                                palavra = lista[i]
                                                if i + 1 == len(lista):
                                                    string += f'{palavra.title()}.'
                                                else:
                                                    string += f'{palavra.title()}, '
                                        else:
                                            string = ''
                                            for i in range(0, len(lista)):
                                                palavra = lista[i]
                                                if i + 1 == len(lista):
                                                    string += f'{palavra.title()}.'
                                                else:
                                                    string += f'{palavra.title()}, '
                                        await ctx.send(f'Suas opções são: {string}')
                                else:
                                    path = pastaProjeto + '/imagens/monopoly/sorte/perder.png'
                                    file = discord.File(path, filename='perder.png')
                                    await ctx.send(file=file)
                                    await ctx.send('**MEU DEUS\n\nMEU DEUS\n\nAQUI É O GAPIGO PROGRAMANDO\n'
                                                   'NÃO ACREDITO... VOCÊ TIROU ISSO? MEEEEEE... BORA SE BENZER**')
                                    acabarJogo = retiraJogador(jogador, 'banco', True)
                                    if acabarJogo is True:
                                        await ctx.send('**O JOGO ESTÁ SENDO ENCERRADO POR FALTA DE JOGADORES**')
                                        string = encerraJogo()
                                        await ctx.send(string)
                                    return
                            else:
                                await ctx.send(
                                    f'Você não pode abrir uma **SORTE DO GUARDIÃO** agora {jogo[jogador]["nome"]}')
                        elif parâmetro in 'escolhaescolher':
                            if 'escolher' in disponiveis:
                                if jogo[jogador]["pcomando"] == 1:
                                    if parâmetro == parâmetroOriginal:
                                        string = f'** PROPRIEDADES DE {jogo[jogador]["nome"]} DISPONÍVEIS PARA DELEÇÃO PREMIADA:**\n'
                                        for posse in jogo[jogador]['posses']:
                                            tipo = casas[posse][2]
                                            if tipo == 'lote':
                                                numCasas = casas[posse][3]
                                                if numCasas != 0:
                                                    if numCasas != 5:
                                                        string += f'Nº{posse} - **{casas[posse][0]}** | Casas: **{numCasas}**\n'
                                                    else:
                                                        string += f'Nº{posse} - **{casas[posse][0]}** | Casas: **{numCasas} + MACA DA APPLE**\n'
                                        string += 'escreva **.m escolher <propriedade>** para escolher a propriedade que perderá todas as casas'
                                        await ctx.send(string)
                                    else:
                                        params = parâmetroOriginal.split(' ')
                                        del params[0]
                                        param = ''.join(params)
                                        lista = ['01augusta',
                                                 '03botinha',
                                                 '06rata',
                                                 '08cemitériodebogacemiteriodebogacemitériodebigcemiteriodebig',
                                                 '09cemiteriodeguardiaocemitériodeguardiãocemitériodeguardiaocemiteriodeguardiãocemiteriodezezoiacemitériodezezoiacemiteriodesequoiacemitériodesequoiacemiteriodesequóiacemitériodesequóiacemiteriodecardiamcemitériodecardiam',
                                                 '11não-me-toquenãometoquenaometoque',
                                                 '13sumarésumarecidadedebogcidadedoboga',
                                                 '14thefloatingdeadsãopaulosaopaulocidadedogapigocidadedoguardião',
                                                 '16nárnianarnia',
                                                 '18groelândiagroelandia',
                                                 '19acre',
                                                 '21casadocaralhocasadokrlcasadocrlcasadocaraiocasadukrlcasaducrl',
                                                 '23bankheist',
                                                 '24orbitaldogapigo',
                                                 '26chernobylachernobilachernobylchernobil',
                                                 '27cavernadasperanhascavernadaspiranhas',
                                                 '29universidadeesquerdistauniversidadeenqueditauniversidadedosenqueditasuniversidadedosesquerdistasuniversidadedeenqueditauniversidadedeesquerdista',
                                                 '31refúgiodonegoneyrefugiodonegoneyrefujiodonegoneyrefúgiodonegoneirefugiodonegoney',
                                                 '32santuáriododorimesantuariododorime',
                                                 '34mansãodoricardãomansaodoricardaomansãodoricardaomansaodoricardãomansãodoricardomilosmansaodoricardomilos',
                                                 '37infernocasadozezoiacasadoguardião',
                                                 '39buraconegrocudobig']
                                        achou = False
                                        for string in lista:
                                            if param in string:
                                                param = int(string[0:2])
                                                achou = True
                                                break
                                        if achou is True:
                                            casas[param][3] = 0
                                            await ctx.send(f'As casas de **{casas[param][0]}** foram deletadas... ༶ඬ༝ඬ༶\n\n\nDELETAR, DELETAR, DELETAAAAR ψ（((ლಠ益ಠ)ლ))）ψ')
                                            thumbCasa(param, True)
                                            path = pastaProjeto + '/imagens/monopoly/temp/thumbAtual.png'
                                            file = discord.File(path, filename='thumbAtual.png')
                                            await ctx.send(file=file)
                                            jogo[jogador]['status'] = 'caixaq'
                                        else:
                                            await ctx.send(f'A propriedade digitada é inválida, suas casas não foram deletadas e ainda encontra-se pendente o comando **.m escolher**')
                            else:
                                await ctx.send(f'Você não tem nada para escolher {jogo[jogador]["nome"]}!')
                        elif parâmetro in 'okpassarvezpronto':
                            if 'ok' in disponiveis:
                                if not inicioJogada:
                                    if jogo[jogador]['status'] == 'pagador':
                                        jogo[jogador]['status'] = 'livre'
                                    elif jogo[jogador]['status'] == 'vá para cadeia':
                                        jogo[jogador]['status'] = 'preso'
                                        jogo[jogador]['casa'] = 40
                                        await ctx.send(f'**{jogo[jogador]["nome"]} pegou DEPRESSOR**')
                                    elif jogo[jogador]['status'] == 'usou':
                                        jogo[jogador]['status'] == 'livre'
                                    elif jogo[jogador]['status'] == 'sorteq':
                                        jogo[jogador]['status'] == 'livre'
                                    elif jogo[jogador]['status'] == 'caixaq':
                                        jogo[jogador]['status'] == 'livre'
                                    elif jogo[jogador]['comando'] != None:
                                        jogo[jogador]['comando'] = None
                                        jogo[jogador]['pcomando'] = None
                                    # RESETA O LOOP DE JOGADORES SE JÁ CHEGOU NO FIM
                                    ultimoAJogar = atual[0]
                                    if atual[1] + 1 == numJogadores:
                                        atual[1] = 0
                                        ecor, enome, eid = escolhidas[atual[1]].split(',')
                                        atual[0] = ecor
                                    # TROCA A VEZ DO JOGADOR
                                    else:
                                        try:
                                            atual[1] += 1
                                            ecor, enome, eid = escolhidas[atual[1]].split(',')
                                            atual[0] = ecor
                                        except:
                                            atual[1] = 0
                                            ecor, enome, eid = escolhidas[atual[1]].split(',')
                                            atual[0] = ecor
                                    await ctx.send(f'É a vez de {enome} de cor **{ecor.upper()}**')
                                    if jogo[jogador]['status'] == 'comprador':
                                        jogo[jogador]['status'] = 'livre'
                                    inicioJogada = True
                                else:
                                    await ctx.send('Você é obrigado a **.m jogar** na sua vez')
                            else:
                                status = jogo[jogador]['status']
                                status.strip().lower()
                                if status in 'devedor':
                                    await ctx.send('Você não pode dar **.m ok** pois está com pagamento pendente, tente **.m pagar**')
                                elif status in 'sorte':
                                    await ctx.send('Você não pode dar **.m ok** pois está na casa **Sorte do Guardião**, tente **.m sorte**')
                                elif status in 'caixa':
                                    await ctx.send('Você não pode dar **.m ok** pois está na casa **Caixa Lazarenta**, tente **.m caixa**')
                                elif status in 'escolhendo':
                                    await ctx.send('Você não pode dar **.m ok** pois tem que escolher uma propriedade para perder as casas. Escolha com **.m escolher**')
                                elif 'jogar' in disponiveis:
                                    await ctx.send(
                                        'Você não pode dar **.m ok** pois ainda não jogou, tente **.m jogar**')
                        else:
                            nãoEntendi = True
                        # Analisa se o que o jogador pegou para pagar vai fazer ele perder
                        if jogo[jogador]['status'] == 'devedor':
                            preço = disponiveis[0][1]
                            if type(preço) is float:
                                cobrador = disponiveis[0][2]
                                semPosses = False
                                if len(jogo[jogador]['posses']) == 0:
                                    semPosses = True
                                if not habilitarDevedor:
                                    if jogo[jogador]['dinheiro'] < preço and semPosses:
                                        restoDinheiro = jogo[jogador]["dinheiro"]
                                        finalizarJogo = retiraJogador(jogador, cobrador)
                                        if cobrador == 'banco':
                                            await ctx.send(
                                                f'Infelizmente você não tem posses e nem dinheiro para pagar o **banco**, **{perdedores[jogador]["nome"]}, VOCÊ PERDEU, TODO RESTO DO SEU DINHEIRO ({formatarDinheiro(restoDinheiro)}) FOI DADO A ELE E VOCÊ FOI RETIRADO DO JOGO**')
                                        else:
                                            await ctx.send(
                                                f'Infelizmente você não tem posses e nem dinheiro para pagar {jogo[cobrador]["nome"]}, **{perdedores[jogador]["nome"]}, VOCÊ PERDEU, TODO RESTO DO SEU DINHEIRO ({formatarDinheiro(restoDinheiro)}) FOI DADO A ELE E VOCÊ FOI RETIRADO DO JOGO**')
                                        if finalizarJogo:
                                            for jogador in jogo.keys():
                                                await ctx.send(
                                                    f'Como só sobrou {jogo[jogador]["nome"]}, **O JOGO FOI FINALIZADO**')
                                            string = encerraJogo()
                                            await ctx.send(string)
                                            return
                                        else:
                                            string = passaAtual()
                                            await ctx.send(string)

                ''' JOGADOR QUALQUER QUE ESTÁ NO JOGO '''
                if parâmetro in opçõesDoAtual and atual[0] != jogador and parâmetro not in 'op' and parâmetro not in 'pos':
                    if jogador == ultimoAJogar:
                        ultimoAJogar = ''
                    else:
                        if parâmetro in 'jogar':
                            parâmetro = 'jogar'
                        await ctx.send(f'Você não pode **{parâmetro}** porque não é sua vez, {jogo[jogador]["nome"]}')
                elif parâmetro in 'opçõesopcoesoptions':
                    lista = analisaAcoes(jogador=jogador, inicio=inicioJogada)

                    if type(lista[0]) is tuple:
                        string = f'{lista[0][0].title()}, '
                        for i in range(1, len(lista)):
                            palavra = lista[i]
                            if i + 1 == len(lista):
                                string += f'{palavra.title()}.'
                            else:
                                string += f'{palavra.title()}, '
                    else:
                        string = ''
                        for i in range(0, len(lista)):
                            palavra = lista[i]
                            if i + 1 == len(lista):
                                string += f'{palavra.title()}.'
                            else:
                                string += f'{palavra.title()}, '

                    await ctx.send(f'Suas opções são: {string}')
                elif parâmetro in 'granagrnaa':
                    await ctx.send(f'Você tem **{formatarDinheiro(jogo[jogador]["dinheiro"])}**, {ctx.author.mention}')
                elif parâmetro in 'finalizarterminarjogofinalizarjogo' and parâmetro not in 'jogo':
                    await ctx.send(f'Para finalizar um jogo, todos os jogadores têm que estar de acordo!')
                    finalizacao = True
                    ecor, enome, eid = escolhidas[0].split(',')
                    idProximoAVotarFinalização = int(eid)
                elif parâmetro in 'informaçãosabersobremostrarcarta':
                    parâmetroOriginal = parâmetroOriginal.split(' ')
                    del parâmetroOriginal[0]
                    parâmetroOriginal = ' '.join(parâmetroOriginal)
                    carta = parâmetroOriginal.replace(' ', '')
                    try:
                        carta = int(carta)
                    except:
                        lista = ['01augusta',
                                 '03botinha',
                                 '05amoteclarnomeuaparelhocomputadorizadoadoroteclarnomeuaparelhocomputadorizado',
                                 '06rata',
                                 '08cemitériodebogacemiteriodebogacemitériodebigcemiteriodebig',
                                 '09cemiteriodeguardiaocemitériodeguardiãocemitériodeguardiaocemiteriodeguardiãocemiteriodezezoiacemitériodezezoiacemiteriodesequoiacemitériodesequoiacemiteriodesequóiacemitériodesequóiacemiteriodecardiamcemitériodecardiam',
                                 '11não-me-toquenãometoquenaometoque',
                                 '12tocufomiiiiiiiiiiiiitocufomeestoucufomitocomfomitocomfometôcomfometocomfomitocufomeeeeeeeeeeeee',
                                 '13sumarésumarecidadedebogcidadedoboga',
                                 '14thefloatingdeadsãopaulosaopaulocidadedogapigocidadedoguardião',
                                 '15carpediem',
                                 '16nárnianarnia',
                                 '18groelândiagroelandia',
                                 '19acre',
                                 '21casadocaralhocasadokrlcasadocrlcasadocaraiocasadukrlcasaducrl',
                                 '23bankheist',
                                 '24orbitaldogapigo',
                                 '25cancercurativocâncercurativoquemçacurativocancercuratifocamcercurativo',
                                 '26chernobylachernobilachernobylchernobil',
                                 '27cavernadasperanhascavernadaspiranhas',
                                 '28chupacu',
                                 '29universidadeesquerdistauniversidadeenqueditauniversidadedosenqueditasuniversidadedosesquerdistasuniversidadedeenqueditauniversidadedeesquerdista',
                                 '31refúgiodonegoneyrefugiodonegoneyrefujiodonegoneyrefúgiodonegoneirefugiodonegoney',
                                 '32santuáriododorimesantuariododorime',
                                 '34mansãodoricardãomansaodoricardaomansãodoricardaomansaodoricardãomansãodoricardomilosmansaodoricardomilos',
                                 '35cooldecuriosocudecurioso',
                                 '37infernocasadozezoiacasadoguardião',
                                 '39buraconegrocudobig']
                        cartaAntigo = carta
                        for string in lista:
                            if carta in string:
                                carta = int(string[0:2])
                                break
                        if carta == cartaAntigo:
                            await ctx.send(f'A carta que você quer não existe ou é inacessível, {jogo[jogador]["nome"]}')
                        else:
                            file = discord.File(pastaProjeto + f'/imagens/monopoly/thumbs/{carta}.png')
                            await ctx.send(file=file)
                    else:
                        if carta in range(1, 41):
                            if carta not in [2, 4, 7, 10, 17, 20, 22, 30, 33, 36, 38]:
                                file = discord.File(pastaProjeto + f'/imagens/monopoly/thumbs/{carta}.png')
                                await ctx.send(file=file)
                            else:
                                await ctx.send(f'A carta é inacessível, {jogo[jogador]["nome"]}')
                        else:
                            await ctx.send(f'A carta não existe, {jogo[jogador]["nome"]}')
                elif parâmetro in 'possespropriedades' and parâmetro != "op":
                    if len(jogo[jogador]['posses']) == 0:
                        await ctx.send(f'Você não tem posses, {jogo[jogador]["nome"]}')
                    else:
                        string = f'Posses de {jogo[jogador]["nome"]}\n'
                        for posse in jogo[jogador]['posses']:
                            if casas[posse][2] == 'lote':
                                string += f'Nº{posse} - **{casas[posse][0]}** com {casas[posse][3]} casas\n'
                            else:
                                string += f'Nº{posse} - **{casas[posse][0]}**\n'
                        string += '\nPara saber mais digite **.m info [posse]**'
                        await ctx.send(string)
                elif parâmetro in 'desistirgiveupdesistênciadesistencia':
                    await ctx.send(
                        'Você tem certeza que quer desistir?\n**O SEU PERSONAGEM SERÁ APAGADO E VOCÊ NÃO PODERÁ VOLTAR NO JOGO!**\n(Responda com **".m sim"** ou **".m não"**')
                    desistencia = True
                    desistente = jogo[jogador]["id"]
                elif desistencia is True and desistente == jogo[jogador]["id"]:
                    if parâmetro in 'simyesclarotenhocerteza':
                        desistentes[jogador] = jogo[jogador]
                        desistente = jogador
                        if jogo[desistente]['status'] == 'devedor':
                            acoes = analisaAcoes(jogador)
                            tupla = acoes[0]
                            valor = tupla[1]
                            cobrador = tupla[2]
                            tupla = ('receber', valor)
                            transacao(cobrador, tupla)
                        for posses in jogo[jogador]['posses']:
                            casas[posses][1] = None
                        await ctx.send(f'**{jogo[jogador]["nome"]} não faz parte mais do jogo**')
                        for i in range(0, len(escolhidas)):
                            ecor, enome, eid = escolhidas[i].split(',')
                            if ecor == jogador:
                                del escolhidas[i]
                                break

                        del jogo[jogador]
                        desistencia = False
                        desistente = ''
                        if len(jogo) == 1:
                            await ctx.send(f'**PARTIDA ENCERRADA POR FALTA DE JOGADORES!**')
                            string = encerraJogo()
                            await ctx.send(string)
                        else:
                            string = passaAtual()
                            await ctx.send(string)
                    elif parâmetro in 'nãoqueronaononãotenho':
                        desistencia = False
                        desistente = ''
                        await ctx.send(f'**Desistência de {jogo[jogador]["nome"]} cancelada!**')
                    else:
                        desistencia = False
                        desistente = ''
                        await ctx.send(f'Não foi possível entender o que você quis dizer {jogo[jogador]["nome"]}, **sua desistência foi** automaticamente **cancelada**. Se quiser, tente de novo')
                elif parâmetro in 'vendercartãovendercartaovenda':
                    disponiveis = analisaAcoes(jogador)
                    if 'vender' in disponiveis:
                        if parâmetro == parâmetroOriginal:
                            string = f'**SEUS OBJETOS DE USO DISPONÍVEIS, {jogo[jogador]["nome"]}:\n'
                            string += '\nCód - OBJETO               - FUNÇÃO\n'
                            if jogo[jogador]['cartoes']['cadeia'] is True:
                                string += 'Nº1 - Anti-depressivo - Te tira da depressão"\n'
                            if jogo[jogador]['cartoes']['estacionamento'] is True:
                                string += 'Nº2 - Sugar Daddy     - Paga para você o que você quiser"\n'
                            if jogo[jogador]['cartoes']['ender'] is True:
                                string += 'Nº3 - Ender Pearl        - Te teleporta para onde você quiser\n'
                            string += '\nVenda com **.m vender @arroba 1.5 item** (arroba do jogador, preço em milhões)'
                            await ctx.send(string)
                        else:
                            params = parâmetroOriginal.split(' ')
                            del params[0]
                            if params[0].startswith('<@!') and params[0].endswith('>'):
                                cliente = params[0]
                                cliente = cliente.replace('!', '')
                                del params[0]
                                nomes = []
                                client = ''
                                for j in jogo.keys():
                                    nomes.append(jogo[j]["nome"])
                                    nome = jogo[j]["nome"]
                                    if nome == cliente:
                                        client = j
                                        break

                                if cliente == jogo[jogador]["nome"]:
                                    await ctx.send('Você não pode se marcar para se vender um item!!')
                                elif cliente not in nomes:
                                    await ctx.send('Jogador não faz parte do jogo!')
                                else:
                                    try:
                                        numFloat = params[0].replace(',', '.')
                                        valor = float(numFloat)
                                        del params[0]
                                    except:
                                        await ctx.send(
                                            'Sintaxe de comando errada! Não foi possível entender o valor de dinheiro a quem vender\n'
                                            'Você deve utilizar **.m vender** como demonstrado abaixo:\n'
                                            '**.m vender @arroba 1 item**\n'
                                            'No caso acima, o comando oferecerá para jogador arroba o item por 1 milhão')
                                    else:
                                        if len(params) == 0:
                                            await ctx.send(
                                                'Sintaxe de comando errada! Não foi dito o item a ser vendido\n'
                                                'Você deve utilizar **.m vender** como demonstrado abaixo:\n'
                                                '**.m vender @arroba 1 item**\n'
                                                'No caso acima, o comando oferecerá para jogador arroba o item por 1 milhão')
                                        else:
                                            lista = ['1antidepressivoanti-depressivoantidepressorantidepressãoad',
                                                     '2sugardaddysugardadaysugar-daddysugarbabysugardadysugardasy',
                                                     '3enderpearl']
                                            param = ''.join(params)
                                            param = param.strip().lower()
                                            achou = False
                                            for string in lista:
                                                if param in string:
                                                    param = int(string[0])
                                                    achou = True
                                                    break
                                            if achou is False:
                                                await ctx.send('Item não encontrado!!!')
                                            else:
                                                item = ''
                                                if param == 1 and jogo[jogador]['cartoes']['cadeia']:
                                                    item = 'Anti-Depressivo'
                                                elif param == 2 and jogo[jogador]['cartoes']['estacionamento']:
                                                    item = 'Sugar Daddy'
                                                elif param == 3 and jogo[jogador]['cartoes']['ender']:
                                                    item = 'Ender Pearl'
                                                else:
                                                    await ctx.send(
                                                        f'Você não tem esse item à venda {jogo[jogador]["nome"]}\n'
                                                        f'Se quiser conferir os items que têm disponíveis use **.m vender**')
                                                if item != '':
                                                    await ctx.send(
                                                        f'{jogo[jogador]["nome"]} fez uma proposta de venda a {jogo[client]["nome"]}:\n'
                                                        f'Uma unidade de **{item}** por **{formatarDinheiro(valor)}\n**'
                                                        f'Se você quer aceitar, {jogo[client]["nome"]}, responda com **.m sim**')
                                                    vendaInfo = (True, client, valor, param, jogador)
                            else:
                                await ctx.send(
                                    'Sintaxe de comando errada! Não foi possível ler o jogador a quem vender\n'
                                    'Você deve utilizar **.m vender** como demonstrado abaixo:\n'
                                    '**.m vender @arroba 1 item**\n'
                                    'No caso acima, o comando oferecerá para jogador arroba o item por 1 milhão')
                    else:
                        await ctx.send(f'Você não tem nada para vender, {jogo[jogador]["nome"]}')
                elif vendaInfo[0] is True and vendaInfo[1] == jogador:
                    valor = vendaInfo[2]
                    item = vendaInfo[3]
                    vendedor = vendaInfo[4]
                    if parâmetro in 'simyesclarotenhocerteza':
                        if jogo[jogador]["dinheiro"] < valor:
                            string = f'{jogo[jogador]["nome"]} não tem dinheiro para realizar a venda!\n'
                            string += f'**VENDA ENTRE {jogo[jogador]["nome"]} E {jogo[vendedor]["nome"]} CANCELADA!**'
                            await ctx.send(string)
                            vendaInfo = (False, '', 0, 0, '')
                        else:
                            if item == 1:
                                item = 'cadeia'
                                itemNome = 'Anti-Depressivo'
                            elif item == 2:
                                item = 'estacionamento'
                                itemNome = 'Sugar Daddy'
                            elif item == 3:
                                item = 'ender'
                                itemNome = 'Ender Pearl'
                            jogo[vendedor]['cartoes'][item] = False
                            tupla = ('pagar', valor, vendedor)
                            transacao(tupla, jogador)
                            jogo[jogador]['cartoes'][item] = True
                            vendaInfo = (False, '', 0, 0, '')
                            await ctx.send(f'**{itemNome}** vendido a {jogo[jogador]["nome"]}!')
                    elif parâmetro in 'nãoqueronaononãotenho':
                        await ctx.send(f'**VENDA ENTRE {jogo[jogador]["nome"]} E {jogo[vendedor]["nome"]} CANCELADA!**')
                        vendaInfo = (False, '', 0, 0, '')
                    else:
                        string = f'Não foi possível entender a resposta de {jogo[jogador]["nome"]} para venda\n'
                        string += f'**VENDA ENTRE {jogo[jogador]["nome"]} E {jogo[vendedor]["nome"]} CANCELADA!**'
                        await ctx.send(string)
                elif nãoEntendi is True:
                    await ctx.send(f'Opção não compreendida, tente novamente {jogo[jogador]["nome"]}')
                elif jogador != atual[0]:
                    await ctx.send(f'Opção não compreendida, tente novamente {jogo[jogador]["nome"]}')
            if finalizacao is True:
                if parâmetro not in 'finalizarterminarjogofinalizarjogosimyesclarotenhocertezanãoqueronaononãotenho':
                    await ctx.send(f'O console está em modo **FINALIZAÇÃO**, aguarde que todos tenham votado para poder escolher outra opção')
                    for escolha in escolhidas:
                        ecor, enome, eid = escolha.split(',')
                        eid = int(eid)
                        if eid == idProximoAVotarFinalização:
                            break
                    await ctx.send(f'{enome}, concorda em **FINALIZAR** o jogo?\n**.m sim** para **FINALIZAR**\n**.m não** para **CANCELAR**')
                else:
                    if parâmetro in 'finalizarterminarjogofinalizarjogo':
                        for i in range(0, len(escolhidas)):
                            ecor, enome, eid = escolhidas[i].split(',')
                            eid = int(eid)
                            if eid == idProximoAVotarFinalização:
                                break
                        await ctx.send(f'{enome}, concorda em **FINALIZAR** o jogo?\n**.m sim** para **FINALIZAR**\n**.m não** para **CANCELAR**')
                    else:
                        if jogo[jogador]['id'] == idProximoAVotarFinalização:
                            if parâmetro in 'simyesclarotenhocerteza':
                                ecor, enome, eid = escolhidas[(len(escolhidas))-1].split(',')
                                eid = int(eid)
                                if eid == idProximoAVotarFinalização:
                                    await ctx.send('**JOGO ENCERRADO!**')
                                    tabela = encerraJogo()
                                    await ctx.send(tabela)

                                else:
                                    for i in range(0, len(escolhidas)):
                                        ecor, enome, eid = escolhidas[i].split(',')
                                        eid = int(eid)
                                        if eid == idProximoAVotarFinalização:
                                            ecor, enome, eid = escolhidas[i+1].split(',')
                                            idProximoAVotarFinalização = int(eid)
                                            break
                                    await ctx.send(f'{enome}, concorda em **FINALIZAR** o jogo?\n**.m sim** para **FINALIZAR**\n**.m não** para **CANCELAR**')
                            elif parâmetro in 'nãoqueronaononãotenho':
                                finalizacao = False
                                idProximoAVotarFinalização = 0
                                await ctx.send(f'**FINALIZAÇÃO DE JOGO CANCELADA**')
                        else:
                            await ctx.send(f'Não é sua vez de votar, {ctx.author.mention}!')
        else:
            await ctx.send(f'{ctx.author.mention} você não está no jogo!')
        contaM += 1


def setup(client):
    client.add_cog(Monopoly(client))
