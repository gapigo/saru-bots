import discord
import random
from discord.ext import commands


class JoguinhosBobos(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.adivinhaNumero = 0
        self.adivinhaInicializado = False
        self.adivinhaTentativas = 0

    # Eventos
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog joguinhosBobos está pronta')

    # Jogo bola 8: jogo bobo de adinhação
    @commands.command()
    async def bola8(self, ctx, *, question):
        responses = ['Isto é certo.',
                     'Está decidido.',
                     'Sem dúvidas.',
                     'Sim - definitivamente.',
                     'Você pode contar com isso.',
                     'Até on eu consigo ver, sim.',
                     'Provavelmente.',
                     'A perspectiva é boa.',
                     'Sim.',
                     'Sinais apontam que sim.',
                     'O respondedor está nublado, tente novamente.',
                     'Pergunte de novo depois.',
                     'Melhor eu nem te dizer.',
                     'Não posso predizer agora.',
                     'Concentre-se e pergunte novamente.',
                     "Não conte com isso.",
                     'Minha resposta é não.',
                     'Minhas fontes dizem que não.',
                     'A perspectiva não é boa.',
                     'Muito duvidoso.']
        await ctx.send(f'{random.choice(responses)}')

    # Jogo de adivinhar o número
    @commands.command()
    async def adnum(self, ctx, menor=0, maior=0):
        if (not self.adivinhaInicializado) or (maior != 0 and maior != menor):
            self.adivinhaInicializado = True
            await ctx.send(f'Jogo adivinha número iniciado!\n'
                           f'Tente adivinhar um número entre {menor} e {maior}')
            self.adivinhaNumero = random.randint(menor, maior)
            self.adivinhaTentativas = 0
        else:
            num = menor
            if num == self.adivinhaNumero:
                await ctx.send(f'Parabéns, você acertou... em {self.adivinhaTentativas} tentativas')
                self.adivinhaInicializado = False
            else:
                if num > self.adivinhaNumero:
                    await ctx.send(f'Menor')
                else:
                    await ctx.send(f'Maior')
                self.adivinhaTentativas += 1


def setup(client):
    client.add_cog(JoguinhosBobos(client))
