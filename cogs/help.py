import asyncio
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    829667308547997737
    #commands
    @commands.group(invoke_without_command=True)
    async def help(self,ctx):
        first_run = True
        totalpages = 5
        while True:
            if first_run:
                page1=discord.Embed(title='Help | command',description='Click on the reaction corresponding to the category to go to the desired page!',colour=discord.Colour.green())
                page1.add_field(name=f"Pages", value=f">>> 1️⃣ This page\n2️⃣ **Moderation**\n3️⃣ **Information**\n4️⃣ **Fun**\n5️⃣ **Music**")
                page1.add_field(name=":exclamation: | Tips", value=":white_small_square: To get more information on the command do: `;help {command}`\n:white_small_square: If you found a bug, you can do: `;bug {text}` to report it to the creator\n:white_small_square: If you want to invite me to your server do: `;invite`")
                page1.set_footer(text=f"About | Page 1/{totalpages}")
                first_run=False
                msg = await ctx.send(embed=page1)

                reactmoji = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
                
                for react in reactmoji:
                    await msg.add_reaction(react)

            def check_react(reaction, user):
                if reaction.message.id != msg.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactmoji:
                    return False
                return True
            
            try:
                res, user = await self.bot.wait_for('reaction_add', timeout=30,check=check_react)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            if user != ctx.message.author:
                pass
            elif '1️⃣' in str(res.emoji):
                
                await msg.remove_reaction("1️⃣",user)
                await msg.edit(embed=page1)
            elif '2️⃣' in str(res.emoji):
                
                page2 = discord.Embed(title='<:justice:828566039016243230> | Moderation', description='These commands are for moderators only',
                colour=discord.Colour.green())
                page2.set_thumbnail(url='https://cdn.discordapp.com/attachments/829956252511371274/829956351961858088/Requirements-Setting-Icon.png')
                page2.add_field(name="Commands:",value=f">>> `ban`\n`unban`\n`hackban`\n`baninfo`\n`kick`\n`mute`\n`unmute`\n`block`\n`unblock`\n`addrole`\n`removerole`\n`purge`\n`clearall`\n`block`\n`unblock`\n`lockdown`")
                page2.add_field(name=":exclamation: | Tips", value="To get more information on the command do: `;help {command}`")
                page2.set_footer(text=f"About | Page 2/{totalpages}")
                await msg.remove_reaction("2️⃣",user)
                await msg.edit(embed=page2)
            elif '3️⃣' in str(res.emoji):
                
                page3=discord.Embed(title='<:information:828585185766670376> | Information',description='These commands are for moderators and members',colour=discord.Colour.green())
                page3.set_thumbnail(url='https://cdn.discordapp.com/attachments/829956252511371274/829968556476727296/023-information.png')
                page3.add_field(name="Commands:",value="`userinfo`\n`serverinfo`\n`channels`\n`roleinfo`\n`ping`\n`wiki`\n`servers`\n`charinfo`\n`rpoll`\n`history`")
                page3.set_footer(text=f"Page 3/{totalpages}")
                page3.add_field(name=":exclamation: | Tips",value="To get more information on the command do: `;help {command}`")
                await msg.remove_reaction("3️⃣",user)
                await msg.edit(embed=page3)
            elif '4️⃣' in str(res.emoji):
                
                page4=discord.Embed(title='<:fun:828585230818213889> | Fun',description='These commands are for moderators and members',colour=discord.Colour.green())
                page4.set_thumbnail(url='https://cdn.discordapp.com/attachments/829956252511371274/829968556476727296/023-information.png')
                page4.add_field(name="Commands:",value="`cat`\n`duck`\n`panda`\n`redpanda`\n`catfact`\n`dog`\n`fox`\n`dice`\n`textmojify`\n`coin`\n`roll`\n`rps`\n`reverse`\n`virus`\n`guess`")
                page4.add_field(name=":exclamation: | Tips", value="To get more information on the command do: `;help {command}`")
                page4.set_footer(text=f"Page 4/{totalpages}")
                await msg.remove_reaction("4️⃣",user)
                await msg.edit(embed=page4)
            elif '5️⃣' in str(res.emoji):
                
              page5=discord.Embed(title='<:information:828585185766670376> | Music',description='These commands are for moderators and members',colour=discord.Colour.green())
              page5.set_thumbnail(url='https://cdn.discordapp.com/attachments/829956252511371274/829968556476727296/023-information.png')
              page5.add_field(name="Commands:",value="`play`\n`queue`\n`repeat`\n`reset`\n`skip`\n`stop`\n`leave`\n`pause`\n`resume`\n`songinfo`\n`join`\n`volume (max 200)`\n`download`")
              page5.add_field(name=":exclamation: | Tips", value="To get more information on the command do: `;help {command}`")
              page5.set_footer(text=f"Page 5/{totalpages}")
              await msg.remove_reaction("5️⃣",user)
              await msg.edit(embed=page5)


    #help command
    @help.command(invoke_without_command=True)
    async def ban(self, ctx):
     help = discord.Embed(title='',description='',colour=discord.Colour.green())
     help.add_field(name="Help | Ban", value="Ban someone from the server")
     help.add_field(name="Usage:",
	                value="`;ban {member} {reason}`")
     help.add_field(name="Example:", value=f";ban {ctx.author.mention} bad boy/girl")
     help.add_field(name="Aliases:", value="none")
     await ctx.send(embed=help)


def setup(bot):
    bot.add_cog(Help(bot))