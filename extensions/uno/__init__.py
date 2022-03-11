import discord
import random
import os
from discord.ext import commands
from PIL import Image

# y de yellow, b de blue, r de red e g de green
# o número é o número que aparece na carta
# + significa comprar mais 2
# p significa proibido jogar
# s significa "switch" que altera o fluxo do jogo
# co significa coringa e c+ a maldita carta do mais 4
cartas = ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'y+', 'yp', 'ys',
          'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b+', 'bp', 'bs',
          'r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r+', 'rp', 'rs',
          'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g+', 'gp', 'gs',
          'co', 'c+']

def analisaCampeao():
    global jogo
    for jogadores in jogo:
        tamanho = len(jogo[jogadores]["cartas"])
        if tamanho == 0:
            return (True, jogadores)
    return (False, '')


def analisaCor(cor):
    lista = ['yellowamareloamarela',
             'greenverde',
             'blueazul',
             'redvermelhovermelha']
    for cores in lista:
        if cor in cores and cor != 'ver':
            cor = cores[0]
            return cor
    return ''


def analisaCompra(carta, jogador):
    global jogo
    maisquatro = False
    if carta == 'c+':
        maisquatro = True
    if maisquatro:
        for carta in jogo[jogador]['cartas']:
            if carta == 'c+':
                return True
    else:
        for carta in jogo[jogador]['cartas']:
            if carta[1] == '+':
                return True
    return False


def analisaJogada(carta, ultima):
    if carta == 'co' or carta == 'c+':
        return True
    elif carta[0] == ultima[0]:
        return True
    elif carta[1] == ultima[1]:
        return True
    else:
        return False


def analisaParam(params):
    tamanhoParams = len(params)
    if tamanhoParams in range(1, 4):
        param = ''.join(params)
        param = param.lower().strip().replace(' ', '')
        lista = ['y0a0amarelo0amareloamarela0amarelayellow0yellow',
                 'y1a1amarelo1amareloamarela1amarelayellow1yellow',
                 'y2a2amarelo2amareloamarela2amarelayellow2yellow',
                 'y3a3amarelo3amareloamarela3amarelayellow3yellow',
                 'y4a4amarelo4amareloamarela4amarelayellow4yellow',
                 'y5a5amarelo5amareloamarela5amarelayellow5yellow',
                 'y6a6amarelo6amareloamarela6amarelayellow6yellow',
                 'y7a7amarelo7amareloamarela7amarelayellow7yellow',
                 'y8a8amarelo8amareloamarela8amarelayellow8yellow',
                 'y9a9amarelo9amareloamarela9amarelayellow9yellow',
                 'g0verde0verdegreen0green',
                 'g1verde1verdegreen1green',
                 'g2verde2verdegreen2green',
                 'g3verde3verdegreen3green',
                 'g4verde4verdegreen4green',
                 'g5verde5verdegreen5green',
                 'g6verde6verdegreen6green',
                 'g7verde7verdegreen7green',
                 'g8verde8verdegreen8green',
                 'g9verde9verdegreen9green',
                 'b0azul0azulblue0blue',
                 'b1azul1azulblue1blue',
                 'b2azul2azulblue2blue',
                 'b3azul3azulblue3blue',
                 'b4azul4azulblue4blue',
                 'b5azul5azulblue5blue',
                 'b6azul6azulblue6blue',
                 'b7azul7azulblue7blue',
                 'b8azul8azulblue8blue',
                 'b9azul9azulblue9blue',
                 'r0vermelho0vermelhovermelha0vermelhared0red',
                 'r1vermelho1vermelhovermelha1vermelhared1red',
                 'r2vermelho2vermelhovermelha2vermelhared2red',
                 'r3vermelho3vermelhovermelha3vermelhared3red',
                 'r4vermelho4vermelhovermelha4vermelhared4red',
                 'r5vermelho5vermelhovermelha5vermelhared5red',
                 'r6vermelho6vermelhovermelha6vermelhared6red',
                 'r7vermelho7vermelhovermelha7vermelhared7red',
                 'r8vermelho8vermelhovermelha8vermelhared8red',
                 'r9vermelho9vermelhovermelha9vermelhared9red',
                 'yproibidoamareloproibidoproibidaamarelaproibida',
                 'gproibidoverdeproibido',
                 'bproibidoazulproibido',
                 'rproibidovermelhoproibidoproibidavermelhaproibida',
                 'y+maisdoisamarelomaisdoisamarelamaisdois',
                 'g+maisdoisverdemaisdois',
                 'b+maisdoisazulmaisdois',
                 'r+maisdoisvermelhomaisdoisvermelhamaisdois',
                 'ystrocaamarelotrocaramarelotrocarswitchyellowswitchamareloswitchtrocaamarelatrocaramarelatrocar',
                 'gstrocaverdetrocarverdetrocarswitchgreenswitchverdeswitch',
                 'bstrocaazultrocarazultrocarswitchblueswitchazulswitch',
                 'rstrocavermelhotrocarvermelhotrocarswitchredswitchvermelhoswitchtrocavermelhatrocarvermelhatrocar',
                 'coringamudacortrocacorpretanormalpretonormal',
                 'c+4maisquatromais4pretocompracoringacomprafamilyfriends'
                 ]
        achou = False
        for item in lista:
            if param in item:
                achou = True
                param = item[0:2]
                break
        if achou:
            return param
        else:
            return ''
    else:
        return ''


def analisaPosse(carta, jogador):
    global jogo
    if carta in jogo[jogador]['cartas']:
        return True
    else:
        return False


def criaBaralhospng(jogador):
    global jogo
    tamanho = len(jogo[jogador]['cartas'])
    # cartas = sorted(jogo[jogador]["cartas"])
    cartas = jogo[jogador]['cartas']
    path = pastaProjeto + f'/imagens/uno/'
    if tamanho == 1:
        carta = cartas[0]
        Im1 = Image.open(pastaProjeto + f'/imagens/uno/{carta}.png')
        Im1.save(f'{path}/temp/{jogador}.png')
    elif tamanho <= 5:
        lista = [(8, 20), (266, 20), (524, 20), (782, 20), (1040, 20)]
        Im1 = Image.open(pastaProjeto + f'/imagens/uno/5.png')
        for i in range(0, 5):
            try:
                Im2 = Image.open(f'{path}{cartas[i]}.png')
            except:
                break
            Im1.paste(Im2, lista[i])
        Im1.save(f'{path}/temp/{jogador}.png')
    elif tamanho <= 10:
        lista = [(11, 13), (269, 13), (527, 13), (785, 13), (1043, 13),
                 (11, 398), (269, 398), (527, 398), (785, 398), (1043, 398)]
        Im1 = Image.open(pastaProjeto + f'/imagens/uno/10.png')
        for i in range(0, 10):
            try:
                Im2 = Image.open(f'{path}{cartas[i]}.png')
            except:
                break
            Im1.paste(Im2, lista[i])
        Im1.save(f'{path}/temp/{jogador}.png')
    elif tamanho <= 18:
        lista = [(3, 10), (154, 10), (305, 10), (456, 10), (607, 10), (758, 10),
                 (3, 230), (154, 230), (305, 230), (456, 230), (607, 230), (758, 230),
                 (3, 450), (154, 450), (305, 450), (456, 450), (607, 450), (758, 450)]
        Im1 = Image.open(pastaProjeto + f'/imagens/uno/18.png')
        for i in range(0, 18):
            try:
                Im2 = Image.open(f'{path}s{cartas[i]}.png')
            except:
                break
            Im1.paste(Im2, lista[i])
        Im1.save(f'{path}/temp/{jogador}.png')
    elif tamanho <= 32:
        lista = [(18, 10), (166, 10), (314, 10), (462, 10), (610, 10), (758, 10), (906, 10), (1054, 10),
                 (18, 225), (166, 225), (314, 225), (462, 225), (610, 225), (758, 225), (906, 225), (1054, 225),
                 (18, 440), (166, 440), (314, 440), (462, 440), (610, 440), (758, 440), (906, 440), (1054, 440),
                 (18, 655), (166, 655), (314, 655), (462, 655), (610, 655), (758, 655), (906, 655), (1054, 655)]
        Im1 = Image.open(pastaProjeto + f'/imagens/uno/32.png')
        for i in range(0, 32):
            try:
                Im2 = Image.open(f'{path}s{cartas[i]}.png')
            except:
                break
            Im1.paste(Im2, lista[i])
        Im1.save(f'{path}/temp/{jogador}.png')
    elif tamanho <= 64:
        lista = [(18, 10), (166, 10), (314, 10), (462, 10), (610, 10), (758, 10), (906, 10), (1054, 10),
                 (18, 225), (166, 225), (314, 225), (462, 225), (610, 225), (758, 225), (906, 225), (1054, 225),
                 (18, 440), (166, 440), (314, 440), (462, 440), (610, 440), (758, 440), (906, 440), (1054, 440),
                 (18, 655), (166, 655), (314, 655), (462, 655), (610, 655), (758, 655), (906, 655), (1054, 655),
                 (18, 870), (166, 870), (314, 870), (462, 870), (610, 870), (758, 870), (906, 870), (1054, 870),
                 (18, 1085), (166, 1085), (314, 1085), (462, 1085), (610, 1085), (758, 1085), (906, 1085), (1054, 1085),
                 (18, 1300), (166, 1300), (314, 1300), (462, 1300), (610, 1300), (758, 1300), (906, 1300), (1054, 1300),
                 (18, 1515), (166, 1515), (314, 1515), (462, 1515), (610, 1515), (758, 1515), (906, 1515), (1054, 1515)]
        Im1 = Image.open(pastaProjeto + f'/imagens/uno/64.png')
        for i in range(0, 64):
            try:
                Im2 = Image.open(f'{path}s{cartas[i]}.png')
            except:
                break
            Im1.paste(Im2, lista[i])
        Im1.save(f'{path}/temp/{jogador}.png')


def comprar(num):
    baralho = []
    for i in range(0, num):
        pesos = [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4]
        carta = random.choices(cartas, weights=pesos, k=1)
        baralho.append(carta[0])
    return baralho


def compraMais(jogador, num):
    global jogo
    cartas = comprar(num)
    for carta in cartas:
        jogo[jogador]['cartas'].append(carta)


def encerraJogo():
    global verificaComeco, verificaUPronto, verificaU
    verificaComeco = False
    verificaUPronto = False
    verificaU = False


def formataCarta(carta):
    string = ''
    if carta[1] == '-':
        string += 'Cor '
    elif carta[1] == 'p':
        string += 'Proibido '
    elif carta[1] == '+':
        string += 'Compra '
    elif carta[1] == 's':
        string += 'Trocar Ordem '
    else:
        string += f'{carta[1] }'
    if carta[0] == 'y':
        string += 'Amarelo'
    elif carta[0] == 'b':
        string += 'Azul'
    elif carta[0] == 'g':
        string += 'Verde'
    elif carta[0] == 'r':
        string += 'Vermelho'
    return string


def mostraProximo(lista, atual):
    try:
        num = 0
        for jogador in lista:
            if jogador == atual:
                break
            num += 1
        retorna = lista[num + 1]
        return retorna
    except IndexError:
        return lista[0]


def retiraCarta(jogador, carta):
    global jogo
    jogo[jogador]['cartas'].remove(carta)


def trocaAVez():
    global jogo, ordemInvertida, ordemNormal, ordemContraria, vez, proibido
    if ordemInvertida:
        ordem = ordemContraria
    else:
        ordem = ordemNormal
    if proibido:
        proximo = mostraProximo(ordem, vez)
        proximo = mostraProximo(ordem, proximo)
    else:
        proximo = mostraProximo(ordem, vez)
    vez = proximo
    if proibido:
        proibido = False


verificaComeco = False
verificaUPronto = False
verificaU = False
path = os.path.realpath('monopoly.py')
path = path[0:path.rfind('/')]
pastaProjeto = path
pastaProjeto = ''  # 2022-03-11 modification


class Uno(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Eventos
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog uno está pronta')

    def verificadorComeco(ctx):
        global verificaComeco
        if verificaComeco:
            return True
        else:
            return False

    def verificadorUPronto(ctx):
        global verificaUPronto
        if verificaUPronto:
            return True
        else:
            return False

    def verificadorU(ctx):
        global verificaU
        if verificaU:
            return True
        else:
            return False

    # Comandos
    @commands.command(aliases=['cu', 'comecaruno', 'começaruno', 'comecarUno'])
    async def começarUno(self, ctx):
        global verificaComeco, contadorParticipantes, jogo, enviador, verificaU, escolherCor, proibido, verificaUPronto
        global ordemInvertida, compraPendente, batata, numBatata, numMaxCartas
        verificaU = False  # Só por enquanto
        if verificaU:
            await ctx.send('Já tem jogo rolando!')
        else:
            await ctx.send(
                f'Jogo de uno começado, escreva **.uparticipar** para poder participar e **.upronto** para quando tiver todos os jogadores já no jogo')
            verificaComeco = True
            verificaUPronto = False
            jogo = dict()
            contadorParticipantes = 0
            enviador = []
            escolherCor = False
            proibido = False
            ordemInvertida = False
            # Se a compra é pendente / quantas cartas acumuladas que serão compradas pelo jogador
            compraPendente = (False, 0)
            batata = False
            numBatata = 0
            numMaxCartas = 64


    @commands.command()
    @commands.check(verificadorComeco)
    async def uparticipar(self, ctx):
        global contadorParticipantes, jogo, enviador, verificaUPronto, verificaU
        if verificaU:
            await ctx.send('Já tem jogo rolando!')
        else:
            await ctx.send(f'{ctx.author.mention} agora faz parte do jogo')
            contadorParticipantes += 1
            id = ctx.author.id
            jogo[id] = {'nome': ctx.author.mention,
                        'cartas': comprar(7),
                        'user': self.client.get_user(id)
                        }
            if contadorParticipantes == 2:
                await ctx.send(f'Escreva **.upronto** para quando estiverem prontos')
                verificaUPronto = True

    @commands.command()
    @commands.check(verificadorUPronto)
    async def upronto(self, ctx):
        global jogo, verificaU, ordem, contrario, ordemNormal, ordemContraria, verificaU, ultimaCarta, vez
        if verificaU:
            await ctx.send('Já tem jogo rolando!')
        else:
            escolhidos = []
            for jogador in jogo.keys():
                user = jogo[jogador]['user']
                await user.send(f'**BARALHO INICIAL: **')
                escolhidos.append(jogador)
            random.shuffle(escolhidos)
            ordemNormal = escolhidos
            ordemContraria = ordemNormal[::-1]
            string = ''
            i = 1
            for jogador in escolhidos:
                string += f'{jogo[jogador]["nome"]} será o {i}º\n'
                i += 1
            string += 'Escreva **.u (carta)** para jogar carta na sua vez'
            await ctx.send(string)
            verificaU = True

            for jogador in jogo:
                criaBaralhospng(jogador)
                user = jogo[jogador]["user"]
                path = pastaProjeto + f'/imagens/uno/temp/{jogador}.png'
                file = discord.File(path, filename=f'{jogador}.png')
                await user.send(file=file)

            while True:
                ultimaCarta = comprar(1)
                ultimaCarta = ultimaCarta[0]
                if ultimaCarta != 'co' and ultimaCarta != 'c+':
                    break
            path = pastaProjeto + f'/imagens/uno/{ultimaCarta}.png'
            file = discord.File(path, filename=f'{ultimaCarta}.png')
            await ctx.send(file=file)
            vez = ordemNormal[0]


    @commands.command()
    @commands.check(verificadorU)
    async def u(self, ctx, *, param):
        global jogo, ordemNormal, ordemContraria, ultimaCarta, vez, escolherCor, ordemInvertida, pastaProjeto, proibido
        global compraPendente, batata, numBatata, cartaBatata, numMaxCartas
        try:
            jogador = ctx.author.id
            nome = jogo[jogador]["nome"]
        except:
            await ctx.send(f'Você não está no jogo, {ctx.author.mention}!')
        else:
            if vez != jogador:
                await ctx.send(f'**Não é sua vez {nome}!!!**')
            else:
                if len(jogo[jogador]["cartas"]) > numMaxCartas:
                    ordemNormal.remove(jogador)
                    ordemContraria.remove(jogador)
                    trocaAVez()
                    del jogo[jogador]
                    await ctx.send(f'**O jogador {nome} não faz mais parte do jogo, porque ultrapassou'
                                   f'o limite de {numMaxCartas} cartas!!!**')
                    if len(jogo) == 1:
                        campeao = ''
                        for key in jogo.keys():
                            campeao = key
                        await ctx.send(f'**{jogo[campeao]["nome"]} é o grande campeão!**\n'
                                       f'Jogo finalizado!\n'
                                       f'Para começar outro, tente **.cu**')
                        encerraJogo()
                    return
                if escolherCor:
                    cor = analisaCor(param)
                    if cor == '':
                        certo = formataCarta(ultimaCarta)
                        await ctx.send(f'**Cor não encontrada! Tente: amarelo, azul, verde ou vermelho, {nome}**\n'
                                       f'A última carta é **{certo}**.')
                    else:
                        ultimaCarta = cor + '-'
                        escolherCor = False
                        trocaAVez()
                        if cor == 'b':
                            cor = 'azul'
                        elif cor == 'g':
                            cor = 'verde'
                        elif cor == 'r':
                            cor = 'vermelho'
                        elif cor == 'y':
                            cor = 'amarelo'
                        await ctx.send(f'A COR DO CORINGA É **{cor.upper()}**\n\n'
                                       f'**É A VEZ DE {jogo[vez]["nome"]}**')
                else:
                    if param in 'comprarcoprar' and param != 'co':
                        string = ''
                        if batata:  # Se o jogador recebeu a batata e comprou, ele queima a batata
                            compraMais(jogador, numBatata)
                            string += f'\n**A BATATA QUEIMOU NA MÃO DE {nome}**.\n' \
                                      f'Ao todo ele comprou **{numBatata} cartas**\n\n'
                            batata = False
                            numBatata = 0
                        compraMais(jogador, 1)
                        criaBaralhospng(jogador)
                        user = jogo[jogador]['user']
                        criaBaralhospng(jogador)
                        path = pastaProjeto + f'/imagens/uno/temp/{jogador}.png'
                        file = discord.File(path, filename=f'{jogador}.png')
                        await user.send(file=file)
                        string += f'**{nome} comprou uma carta da loja!**'
                        await ctx.send(string)
                    elif param in 'vercartas':
                        string = ''
                        for j in jogo.keys():
                            string += f'**{jogo[j]["nome"]} tem {len(jogo[j]["cartas"])} cartas**\n'
                        await ctx.send(string)
                    else:
                        ordem = ordemNormal
                        if ordemInvertida:
                            ordem = ordemContraria
                        params = param.split(' ')
                        param = analisaParam(params)
                        if param == '':
                            await ctx.send(f'Carta inexistente!')
                        else:
                            tem = analisaPosse(param, jogador)
                            if tem is False:
                                await ctx.send(f'**VOCÊ NÃO TEM ESSA CARTA, {nome}!!!**')
                            else:
                                pode = analisaJogada(param, ultimaCarta)
                                if not pode:
                                    await ctx.send(f'**VOCÊ NÃO PODE JOGAR ESSA CARTA, {nome}!!!**')
                                # FIM DAS FISCALIZAÇÕES E JOGADA PŔOPRIA EM SI
                                else:
                                    '''if (param == 'c+' and ultimaCarta[0] == 'c+') or (param[1] == '+' and ultimaCarta[1] == '+'):
                                        batata = True
                                        if param == 'c+':
                                            numBatata += 4
                                        else:
                                            numBatata += 2'''
                                    '''if batata:
                                        if ultimaCarta[1] == '+':
                                            cartaBatata = ultimaCarta'''
                                    ultimaCarta = param
                                    retiraCarta(jogador, param)
                                    string = ''
                                    if batata:
                                        # Condições da batata queimar
                                        batataQueimo = False
                                        if cartaBatata == 'c+' and param != 'c+':
                                            batataQueimo = True
                                        elif param[1] != '+':
                                            batataQueimo = True
                                        elif param == 'c+' and cartaBatata[0] != 'c':
                                            batataQueimo = True
                                        # Se a batata queimou...
                                        if batataQueimo:
                                            compraMais(jogador, numBatata)
                                            string += f'\n**A BATATA QUEIMOU NA MÃO DE {nome}**.\n' \
                                                      f'Ao todo ele comprou **{numBatata} cartas**\n'
                                            batata = False
                                            numBatata = 0
                                        else:
                                            cartaBatata = param  # Salva a carta do jogador em batata para continuar o combo

                                            # Se a batata é de mais quatro
                                            if cartaBatata == 'c+':
                                                batata = True
                                                numBatata += 4
                                                proximo = mostraProximo(ordem, jogador)
                                                nomeproximo = jogo[proximo]["nome"]
                                                string += f'\n{nome} jogou a batata para {nomeproximo}\n' \
                                                          f'**Se** ele **não tiver** um **MAIS QUATRO** ele comprará {numBatata}\n'
                                            else:
                                                batata = True
                                                numBatata += 2
                                                proximo = mostraProximo(ordem, jogador)
                                                nomeproximo = jogo[proximo]["nome"]
                                                string += f'\n{nome} jogou a batata para {nomeproximo}\n' \
                                                          f'**Se** ele **não tiver** um **MAIS DOIS** ele comprará {numBatata}\n'
                                            user = jogo[proximo]['user']
                                            await user.send(f'O {nome} te jogou a batata, se você não tacar o mesmo'
                                                            f' tipo de carta para defender irá comprar o acúmulo de'
                                                            f' cartas')
                                    elif param[1] == '+':
                                        proximo = mostraProximo(ordem, jogador)
                                        v = analisaCompra(param, proximo)
                                        # Começando a batata se tiver disponível
                                        if v is True:
                                            batata = True
                                            if param[0] == 'c':
                                                numBatata = 4
                                            else:
                                                numBatata = 2
                                            cartaBatata = param
                                            string += f'\n{nome} fez {jogo[proximo]["nome"]} comprar **{numBatata} cartas**.\n'
                                        else:
                                            if param[0] == 'c':
                                                compraMais(proximo, 4)
                                                string += f'\n{nome} fez {jogo[proximo]["nome"]} comprar '
                                                string += '**4 cartas**.\n'
                                            else:
                                                compraMais(proximo, 2)
                                                string += f'\n{nome} fez {jogo[proximo]["nome"]} comprar '
                                                string += '**2 cartas**.\n'

                                        # Manda para o jogador que comprou cartas o seu novo baralho
                                        user = jogo[proximo]['user']
                                        if batata:
                                            await user.send(f'O {nome} te jogou a batata, se você não tacar o mesmo'
                                                            f' tipo de carta para defender irá comprar o'
                                                            f' acúmulo de cartas')
                                        criaBaralhospng(proximo)
                                        path = pastaProjeto + f'/imagens/uno/temp/{proximo}.png'
                                        file = discord.File(path, filename=f'{proximo}.png')
                                        await user.send(file=file)

                                    if param == 'co' or param == 'c+':
                                        escolherCor = True


                                    if param[1] == 's':
                                        string += f'\n{nome} inverteu a ordem da partida.'
                                        if ordemInvertida:
                                            ordemInvertida = False
                                        else:
                                            ordemInvertida = True
                                    if param[1] == 'p':
                                        proximo = mostraProximo(ordem, jogador)
                                        string += f'\n{nome} **pulou a vez de** {jogo[proximo]["nome"]}!'
                                        proibido = True

                                    # Vê se há ganhador
                                    tupla = analisaCampeao()
                                    if tupla[0] is True:
                                        campeao = tupla[1]
                                        await ctx.send(f'**{jogo[campeao]["nome"]} é o grande campeão!**\n'
                                                       f'Jogo finalizado!\n'
                                                       f'Para começar outro, tente **.cu**')
                                        encerraJogo()
                                        return
                                    # Não troca vez para poder deixar o jogador escolher a cor
                                    if not escolherCor:
                                        trocaAVez()
                                    else:
                                        string += f'{nome} escolha a cor com .u [cor]'
                                    # Manda a ultima imagem na call
                                    path = pastaProjeto + f'/imagens/uno/{ultimaCarta}.png'
                                    file = discord.File(path, filename=f'{ultimaCarta}.png')
                                    await ctx.send(file=file)

                                    string += '\n-------------------------||\n'
                                    for j in jogo:
                                        string += f'{jogo[j]["nome"]} tem {len(jogo[j]["cartas"])} cartas no baralho\n'
                                    string += '||-------------------------'
                                    string += f'\n\n**É A VEZ DE {jogo[vez]["nome"]}**'
                                    await ctx.send(string)


                                    # Manda para o jogador o seu baralho
                                    user = jogo[jogador]['user']
                                    criaBaralhospng(jogador)
                                    path = pastaProjeto + f'/imagens/uno/temp/{jogador}.png'
                                    file = discord.File(path, filename=f'{jogador}.png')
                                    await user.send(file=file)
def setup(client):
    client.add_cog(Uno(client))