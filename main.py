import discord
import os
from discord.ext import commands
from keep_alive import keep_alive


bot = commands.Bot(command_prefix=commands.when_mentioned_or(";"))
bot.author_id = 482284652514508800
bot.remove_command('help')
filtred_words = [ 
]


intents = discord.Intents().default()
intents.messages = True
intents.reactions = True
intents.presences = True
intents.members = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = True
intents.webhooks = False


@bot.event
async def on_ready():
    print("Ready!")
    await bot.change_presence(
      activity=discord.Activity(type=discord.ActivityType.playing,
                                  name=";help"))

    print('Servers connected to:')
    for guild in bot.guilds:
        print(guild.name)



#on message and filtred words
@bot.event
async def on_message(message):
	if message.content == ";-;":
		await message.channel.send('°-°')

	for word in filtred_words:
		if word in message.content:
			await message.delete()
			await message.channel.send(
			    f':no_entry: **Non si può dire!**\n Leggi le regole!')

	await bot.process_commands(message)



#help command
@bot.command(invoke_without_command=True)
async def helpgggfg(ctx):
	p1 = discord.Embed(title='Moderation <:justice:828566039016243230>',
	                   description='These commands are for moderators only',
	                   colour=discord.Colour.green())
	p1.set_thumbnail(url=bot.user.avatar_url)
	p1.add_field(
	    name="Commands:",
	    value=
	    "`ban`\n`unban`\n`hackban`\n`baninfo`\n`kick`\n`mute`\n`unmute`\n`block`\n`unblock`\n`addrole`\n`removerole`\n`purge`\n`clearall`\n`block`\n`unblock`\n`lockdown`\n-For more information on the command, do `;help [command]`"
	)
	p1.set_footer(text=f"Page 1/3")

	p2 = discord.Embed(title='Information <:information:828585185766670376>',
	                   description='These commands are for moderators and members',
	                   colour=discord.Colour.green())
	p2.set_thumbnail(url=bot.user.avatar_url)
	p2.add_field(
	    name="Commands:",
	    value=
	    "`userinfo`\n`serverinfo`\n`channels`\n`roleinfo`\n`ping`\n`wiki`\n`servers`\n`charinfo`\n`rpoll`\n\n-For more information on the command, do `;help [command]`"
	)
	p2.set_footer(text=f"Page 2/3")

	p3 = discord.Embed(title='Fun <:fun:828585230818213889>',
	                   description='These commands are for moderators and members',
	                   colour=discord.Colour.green())
	p3.set_thumbnail(url=bot.user.avatar_url)
	p3.add_field(
	    name="Commands:",
	    value=
	    "`reverse`\n`rps`\n`textmojify`\n`cat`\n`dog`\n`fox`\n`coin`\n`dice`\n`roll`\n`guess`\n`virus`\n\n-For more information on the command, do `;help [command]`"
	)
	p3.set_footer(text=f"Page 3/3")

	p4 = discord.Embed(title='Fun <:fun:828585230818213889>',
	                   description='These commands are for moderators and members',
	                   colour=discord.Colour.green())
	p4.set_thumbnail(url=bot.user.avatar_url)
	p4.add_field(
	    name="Commands:",
	    value=
	    "`reverse`\n`rps`\n`textmojify`\n`cat`\n`dog`\n`fox`\n`coin`\n`dice`\n`roll`\n`guess`\n`virus`\n\n-For more information on the command, do `;help [command]`"
	)
	p4.set_footer(text=f"Page 3/3")


	pages = [p1, p2, p3, p4]

	message = await ctx.send(embed=p1)
	await message.add_reaction('⏮')
	await message.add_reaction('◀')
	await message.add_reaction('▶')
	await message.add_reaction('⏭')

	def check(reaction, user):
		return user == ctx.author

	i = 0
	reaction = None

	while True:
		if str(reaction) == '⏮':
			i = 0
			await message.edit(embed=pages[i])
		elif str(reaction) == '◀':
			if i > 0:
				i -= 1
				await message.edit(embed=pages[i])
		elif str(reaction) == '▶':
			if i < 2:
				i += 1
				await message.edit(embed=pages[i])
		elif str(reaction) == '⏭':
			i = 2
			await message.edit(embed=pages[i])

		try:
			reaction, user = await bot.wait_for('reaction_add',
			                                    timeout=30.0,
			                                    check=check)
			await message.remove_reaction(reaction, user)
		except:
			break

	await message.clear_reactions()



#join message
@bot.event
async def on_guild_join(guild):
    general = guild.text_channels[0]
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))
    else:
      print("Error")



#error message
'''@bot.event
async def on_command_error(ctx, error):
    print(f"{ctx.guild.name}:  {error}")  # Consolemessage
    if isinstance(error, commands.CommandError):
        await ctx.send(f">>> **I just found an error!**\n{error}")  # Errormessage'''

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
      em = discord.Embed(
	    title=":exclamation: | Error",
	    description=
	    "Sorry, but this command doesn't exist",
	    color=discord.Colour.red())
      em.add_field(name=":bulb: | Tips", value=f">>> If you want to see the list of commands, do: `;help`")
      await ctx.send(embed=em)

#eval command
import contextlib
import io
@bot.command()
async def eval(ctx, *, code):
    id = str(ctx.author.id)
    if id == '482284652514508800':
     str_obj = io.StringIO()
     try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
     except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'```{str_obj.getvalue()}```')



#Cogs load system
@bot.command()
async def load(ctx, extension):
    id = str(ctx.author.id)
    if id == '482284652514508800':
        bot.load_extension(f'cogs.{extension}')
    else:
        await ctx.send("You can't use this command,\nthis command is for the creator only")

@bot.command()
async def unload(ctx, extension):
    id = str(ctx.author.id)
    if id == '482284652514508800)':
        bot.unload_extension(f'cogs.{extension}')
    else:
        await ctx.send("You can't use this command,\nthis command is for the creator only")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



#commands
@bot.command()
async def servers(ctx):
	channel = ctx.channel
	em = discord.Embed(title=f"I am used in {len(bot.guilds)} servers!",
	                   description="Can we reach 100 servers?",
	                   color=discord.Colour.purple())
	await ctx.send(embed=em)
	pass


@bot.command()
async def status(ctx):
	channel = ctx.channel
	em = discord.Embed(
	    title=
	    f"My status page\n:chart_with_downwards_trend: :chart_with_upwards_trend: ",
	    description=
	    "[StatusPage](https://stats.uptimerobot.com/ZvR37HMq9D)\n** password:**\n000000 \n",
	    color=discord.Colour.purple())
	await ctx.send(embed=em)
	pass


@bot.command()
async def bug(ctx, *, bug):
	filename = f'B-{ctx.author.name}.txt'
	f = open(filename, "w")
	f.write(f'{ctx.author.name} Ha segnalato:\n{bug}')
	channel = ctx.channel
	em = discord.Embed(
	    title="Thanks!",
	    description=
	    f":white_check_mark: The bug was reported to my creator!",
	    color=discord.Colour.red())
	em.add_field(name=":scroll: The bug:", value=f'{bug}')
	em.set_thumbnail(url=bot.user.avatar_url)
	await ctx.send(embed=em)
	pass


@bot.command()
async def off(ctx):
	id = str(ctx.author.id)
	if id == '482284652514508800':
		await ctx.send('**Shutting down...**')
		await bot.logout()
		#await login(token, *)

	else:
		ctx.send(":no_entry: **You can't turn off the Bot!**")


@bot.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.send(f"Slowmode has been set to {seconds} seconds")


@bot.command()
@commands.has_permissions(administrator=True)
async def cleanall(ctx):
	new_channel = await ctx.channel.clone(reason="Clone")
	await ctx.channel.delete()
	em = discord.Embed(title="The canal has been cleared!",
	                   description=f"<:kek:827246643895992350>",
	                   color=discord.Colour.blurple())

	await new_channel.send(embed=em)


@bot.command()
async def ping(ctx):
	channel = ctx.channel
	em = discord.Embed(title="Pong:ping_pong:",
	                   description=f"{round(bot.latency * 1000)}ms",
	                   color=discord.Colour.blurple())
	await ctx.send(embed=em)
	pass


@bot.command()
async def invite(ctx):
	cannel = ctx.channel
	em = discord.Embed(
	    title="Invite me to your server!",
	    description=
	    "",
	    color=discord.Colour.blurple())
	em.add_field(
	    name="Add Cold",
	    value=
	    "[Invite me](https://discord.com/api/oauth2/authorize?client_id=793275503556952075&permissions=373288951&redirect_uri=https%3A%2F%2Fdiscord.gg%2FDwTMj5acR8&scope=bot)"
	)
	await ctx.send(embed=em)
	pass



keep_alive()
token = os.environ.get("Token")
bot.run(os.getenv("TOKEN"))
