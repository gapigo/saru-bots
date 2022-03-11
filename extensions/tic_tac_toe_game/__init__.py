import discord
from discord.ext import commands
#import testes

class JogoDaVelha(commands.Cog):
    jogo = '123456789'
    troca = ['x', True]
    p1 = False
    p2 = False

    # Instância de classe
    def __init__(self, client):
        self.client = client

    # Registro de inicialização no console
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog jogoDaVelha está pronta')

    # Iniciar jogo da velha
    @commands.command(aliases=['jogodavelha', 'tictactoe'])
    async def velha(self, ctx):
        global jogo, p1, p2, troca
        troca = ['', True]
        p1 = False
        p2 = False
        jogo = '123456789'
        await ctx.send('Jogo iniciado!')

    # Instruções
    @commands.command()
    async def velhaInstruções(self, ctx):
        global testes
        await ctx.send('Jogo da velha básico\n'
                       '--------------------\n'
                       'Digite "<prefixo padrão>velha" para começar um jogo e'
                       'Digite "<prefixo padrão>x (ou \'o\') <número da casa>\n para fazer uma jogada'
                       'Exemplo: .x 3 para jogar como X na casa 3\n'
                       '      ou .o 5 para jogar como O na casa 5\n'
                       '-----------------------------------------\n'
                       'As casas disponíveis são:\n'
                       '1 2 3    X + +\n'
                       '4 5 6   O + X\n'
                       '7 8 9   + O +\n'
                       'X está nas casas 1 e 6\n'
                       'O está nas casas 4 e 8')

    # Fazer jogada como X
    @commands.command(aliases=['X', 'p1', 'j1', 'Player1'])
    async def x(self, ctx, jogada):
        global troca, jogo, p1
        if jogo.isnumeric():
            troca = ['x', True]
        if (troca[0] == 'x' and troca[1] is True) or (troca[0] == 'o' and troca[1] is False):
            jogada = jogada.strip()
            try:
                jogada = int(jogada)
            except:
                await ctx.send('Valor desconhecido, digite novamente')
                return
            else:
                if jogada not in range(1, 10):
                    await ctx.send(f'{jogada} passou do intervalo de 1 a 9, tente novamente')
                    return
                else:
                    if jogo[int(jogada)-1].isnumeric():
                        inteiro = (int(jogada))
                        jogo = jogo.replace(f'{inteiro}', 'X')

                        string = jogo

                        ''' troca números por _ '''
                        for i in range(0, 9):
                            string = string.replace(f'{i+1}', '+')


                        await ctx.send(f'{string[0]}{string[1]}{string[2]}\n'
                                       f'{string[3]}{string[4]}{string[5]}\n'
                                       f'{string[6]}{string[7]}{string[8]}')

                    else:
                        await ctx.send('Valor já utilizado, tente novamente')
                        return
        else:
            await ctx.send('Não é a vez de X jogar')
            return
        if jogo[0] == 'X' and jogo[1] == 'X' and jogo[2] == 'X':
            p1 = True
        if jogo[3] == 'X' and jogo[4] == 'X' and jogo[5] == 'X':
            p1 = True
        if jogo[6] == 'X' and jogo[7] == 'X' and jogo[8] == 'X':
            p1 = True
        if jogo[0] == 'X' and jogo[3] == 'X' and jogo[6] == 'X':
            p1 = True
        if jogo[1] == 'X' and jogo[4] == 'X' and jogo[7] == 'X':
            p1 = True
        if jogo[2] == 'X' and jogo[5] == 'X' and jogo[8] == 'X':
            p1 = True
        if jogo[0] == 'X' and jogo[4] == 'X' and jogo[8] == 'X':
            p1 = True
        if jogo[2] == 'X' and jogo[4] == 'X' and jogo[6] == 'X':
            p1 = True
        if p1 is True:
            await ctx.send('O JOGADOR X ganhou!')
            jogo = '123456789'
            return
        else:
            if troca[0] == 'x':
                troca[1] = False
            else:
                troca[1] = True
        if jogo.isalpha():
            await ctx.send('DEU VELHA!')
            jogo = '123456789'

    # Erros de X
    @x.error
    async def x_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Jogada não declarada')

    # Fazer jogada como O
    @commands.command(aliases=['O', 'p2', 'j2', 'Player2'])
    async def o(self, ctx, jogada):
        global troca, jogo, p2
        if jogo.isnumeric():
            troca = ['o', True]
        if (troca[0] == 'o' and troca[1] is True) or (troca[0] == 'x' and troca[1] is False):
            jogada = jogada.strip()
            try:
                jogada = int(jogada)
            except:
                await ctx.send('Valor desconhecido, digite novamente')
                return
            else:
                if jogada not in range(1, 10):
                    await ctx.send(f'{jogada} passou do intervalo de 1 a 9, tente novamente')
                    return
                else:
                    if jogo[int(jogada)-1].isnumeric():
                        inteiro = (int(jogada))
                        jogo = jogo.replace(f'{inteiro}', 'O')

                        string = jogo

                        ''' troca números por _ '''
                        for i in range(0, 9):
                            string = string.replace(f'{i+1}', '+')


                        await ctx.send(f'{string[0]}{string[1]}{string[2]}\n'
                                       f'{string[3]}{string[4]}{string[5]}\n'
                                       f'{string[6]}{string[7]}{string[8]}')

                    else:
                        await ctx.send('Valor já utilizado, tente novamente')
                        return
        else:
            await ctx.send('Não é a vez de O jogar')
            return
        if jogo[0] == 'O' and jogo[1] == 'O' and jogo[2] == 'O':
            p2 = True
        if jogo[3] == 'O' and jogo[4] == 'O' and jogo[5] == 'O':
            p2 = True
        if jogo[6] == 'O' and jogo[7] == 'O' and jogo[8] == 'O':
            p2 = True
        if jogo[0] == 'O' and jogo[3] == 'O' and jogo[6] == 'O':
            p2 = True
        if jogo[1] == 'O' and jogo[4] == 'O' and jogo[7] == 'O':
            p2 = True
        if jogo[2] == 'O' and jogo[5] == 'O' and jogo[8] == 'O':
            p2 = True
        if jogo[0] == 'O' and jogo[4] == 'O' and jogo[8] == 'O':
            p2 = True
        if jogo[2] == 'O' and jogo[4] == 'O' and jogo[6] == 'O':
            p2 = True
        if p2 is True:
            await ctx.send('O JOGADOR O ganhou!')
            jogo = '123456789'
            return
        else:
            if troca[0] == 'o':
                troca[1] = False
            else:
                troca[1] = True
        if jogo.isalpha():
            await ctx.send('DEU VELHA!')
            jogo = '123456789'

    # Erros de O
    @o.error
    async def o_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Jogada não declarada')


def setup(client):
    client.add_cog(JogoDaVelha(client))
