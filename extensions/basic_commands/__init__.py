import discord
from discord.ext import commands


class ComandosSimples(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Registro de inicialização
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog comandosSimples está pronta')

    '''
        1. COMANDOS
    '''

    # Ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    # Kicks
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        if reason is not None:
            await ctx.send(f'{member.mention} foi kickado (・｀ω´・)\nMotivo: {reason}')
        else:
            await ctx.send(f'{member.mention} tomou kick (・｀ω´・)')

    # Ban
    @commands.command(aliases=['banir'])
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        if reason is not None:
            await ctx.send(f'{member.mention} foi banido (╥_╥)\nMotivo: {reason}')
        else:
            await ctx.send(f'{member.mention} foi banido (╥_╥)')

    # Unban
    @commands.command(aliases=['desban', 'desbanir'])
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name}#{user.discriminator} foi desbanido')
                return
        await ctx.send(f'O usuário {member} não foi encontrado na lista de ban')

    # Banlist
    @commands.command(aliases=['listadeban', 'listaban', 'banimentos'])
    async def banlist(self, ctx):
        banned_users = await ctx.guild.bans()
        try:
            user = banned_users[0].user
        except:
            await ctx.send(f'A lista de ban está vazia ( ‾ʖ̫‾)')
        else:
            string = ''
            for ban_entry in banned_users:
                user = ban_entry.user
                string += f'{user}\n'
            await ctx.send(f'{string}')

    # Clear
    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=(amount+1))

    '''
        2. TRATAMENTO DE ERROS
    '''

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('O usuário não existe! Banimento não concluído')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('É necessário informar o nome do usuário a ser banido')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('O formato do nome é inválido!\nTente algo como "unban Nome de Usuário#0000"')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('É necessário informar o nome do usuário a ser desbanido')


def setup(client):
    client.add_cog(ComandosSimples(client))
