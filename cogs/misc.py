import discord
import asyncio
import random
import unicodedata
import wikipedia
import textwrap
import aiohttp
import io
from discord.ext import commands
from enum import Enum

from ext import embedtobox


class RPSLS(Enum):
    rock     = "\N{RAISED FIST} Rock!"
    paper    = "\N{RAISED HAND WITH FINGERS SPLAYED} Paper!"
    scissors = "\N{BLACK SCISSORS} Scissors!"
    lizard   = "\N{LIZARD} Lizard!"
    spock    = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS} Spock!"


class RPSLSParser:
    def __init__(self, argument):
        argument = argument.lower()
        if argument == "rock":
            self.choice = RPSLS.rock
        elif argument == "paper":
            self.choice = RPSLS.paper
        elif argument == "scissors":
            self.choice = RPSLS.scissors
        elif argument == "lizard":
            self.choice = RPSLS.lizard
        elif argument == "spock":
            self.choice = RPSLS.spock
        else:
            raise



class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def virus(self, ctx, virus=None, *, user: discord.Member = None):
        '''
        Destroy someone's device with this virus command!
        '''
        virus = virus or 'discord'
        user = user or ctx.author
        with open('data/virus.txt') as f:
            animation = f.read().splitlines()
        base = await ctx.send(animation[0])
        for line in animation[1:]:
            await base.edit(content=line.format(virus=virus, user=user))
            await asyncio.sleep(random.randint(1, 4))

    @commands.command()
    async def textmojify(self, ctx, *, msg):
        """Convert text into emojis"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        if msg != None:
            out = msg.lower()
            text = out.replace(' ', '    ').replace('10', '\u200B:keycap_ten:')\
                      .replace('ab', '\u200B🆎').replace('cl', '\u200B🆑')\
                      .replace('0', '\u200B:zero:').replace('1', '\u200B:one:')\
                      .replace('2', '\u200B:two:').replace('3', '\u200B:three:')\
                      .replace('4', '\u200B:four:').replace('5', '\u200B:five:')\
                      .replace('6', '\u200B:six:').replace('7', '\u200B:seven:')\
                      .replace('8', '\u200B:eight:').replace('9', '\u200B:nine:')\
                      .replace('!', '\u200B❗').replace('?', '\u200B❓')\
                      .replace('vs', '\u200B🆚').replace('.', '\u200B🔸')\
                      .replace(',', '🔻').replace('a', '\u200B🅰')\
                      .replace('b', '\u200B🅱').replace('c', '\u200B🇨')\
                      .replace('d', '\u200B🇩').replace('e', '\u200B🇪')\
                      .replace('f', '\u200B🇫').replace('g', '\u200B🇬')\
                      .replace('h', '\u200B🇭').replace('i', '\u200B🇮')\
                      .replace('j', '\u200B🇯').replace('k', '\u200B🇰')\
                      .replace('l', '\u200B🇱').replace('m', '\u200B🇲')\
                      .replace('n', '\u200B🇳').replace('ñ', '\u200B🇳')\
                      .replace('o', '\u200B🅾').replace('p', '\u200B🅿')\
                      .replace('q', '\u200B🇶').replace('r', '\u200B🇷')\
                      .replace('s', '\u200B🇸').replace('t', '\u200B🇹')\
                      .replace('u', '\u200B🇺').replace('v', '\u200B🇻')\
                      .replace('w', '\u200B🇼').replace('x', '\u200B🇽')\
                      .replace('y', '\u200B🇾').replace('z', '\u200B🇿')
            try:
                await ctx.send(text)
            except Exception as e:
                await ctx.send(f'```{e}```')
        else:
            await ctx.send('Write something, reee!', delete_after=3.0)

    @commands.command(pass_context=True)
    async def rpoll(self, ctx, *, args):
        """Create a poll using reactions. {p}help rpoll for more information.
        {p}rpoll <question> | <answer> | <answer> - Create a poll. You may use as many answers as you want, placing a pipe | symbol in between them.
        Example:
        {p}rpoll What is your favorite anime? | Steins;Gate | Naruto | Attack on Titan | Shrek
        You can also use the "time" flag to set the amount of time in seconds the poll will last for.
        Example:
        {p}rpoll What time is it? | HAMMER TIME! | SHOWTIME! | time=10
        """
        await ctx.message.delete()
        options = args.split(" | ")
        time = [x for x in options if x.startswith("time=")]
        if time:
            time = time[0]
        if time:
            options.remove(time)
        if len(options) <= 1:
            raise commands.errors.MissingRequiredArgument
        if len(options) >= 11:
            return await ctx.send(self.bot.bot_prefix + "You must have 9 options or less.")
        if time:
            time = int(time.strip("time="))
        else:
            time = 30
        emoji = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
        to_react = []
        confirmation_msg = "**{}?**:\n\n".format(options[0].rstrip("?"))
        for idx, option in enumerate(options[1:]):
            confirmation_msg += "{} - {}\n".format(emoji[idx], option)
            to_react.append(emoji[idx])
        confirmation_msg += "\n\nYou have {} seconds to vote!".format(time)
        poll_msg = await ctx.send(confirmation_msg)
        for emote in to_react:
            await poll_msg.add_reaction(emote)
        await asyncio.sleep(time)
        async for message in ctx.message.channel.history():
            if message.id == poll_msg.id:
                poll_msg = message
        results = {}
        for reaction in poll_msg.reactions:
            if reaction.emoji in to_react:
                results[reaction.emoji] = reaction.count - 1
        end_msg = "The poll is over. The results:\n\n"
        for result in results:
            end_msg += "{} {} - {} votes\n".format(result, options[emoji.index(result)+1], results[result])
        top_result = max(results, key=lambda key: results[key])
        if len([x for x in results if results[x] == results[top_result]]) > 1:
            top_results = []
            for key, value in results.items():
                if value == results[top_result]:
                    top_results.append(options[emoji.index(key)+1])
            end_msg += "\nThe victory is tied between: {}".format(", ".join(top_results))
        else:
            top_result = options[emoji.index(top_result)+1]
            end_msg += "\n{} is the winner!".format(top_result)
        await ctx.send(end_msg)

    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """Shows you information about a number of characters."""
        if len(characters) > 15:
            return await ctx.send('Too many characters ({}/15)'.format(len(characters)))

        fmt = '`\\U{0:>08}`: `\\N{{{1}}}` - `{2}` - <http://www.fileformat.info/info/unicode/char/{0}>'

        def to_string(c):
            digit = format(ord(c), 'x')
            name = unicodedata.name(c, 'Name not found.')
            return fmt.format(digit, name, c)

        await ctx.send('\n'.join(map(to_string, characters)))

    @commands.command()
    async def history(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://numbersapi.com/random/date?json') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.orange(),
                    title="Random History Fact",
                    description=f"**Fact:** \n{res['text']}")
                embed.set_footer(text=f"Year | {res['year']} ")
         
                await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/img/cat') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.green(), title=":cat: | Meow")
                embed.set_image(url=res['link'])
                embed.set_footer(text="Here, take some cat")

                await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.green(),
                    title=":dog: | Woffy"
                )
                embed.set_image(url=res['message'])
                embed.set_footer(text="Here, take some dog")

                await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://randomfox.ca/floof/') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.green(),
                    title=":fox: | Floffy! "
                )
                embed.set_image(url=res['image'])
                embed.set_footer(text="Here, take some fox")

                await ctx.send(embed=embed)


                

    @commands.command()
    async def duck(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random-d.uk/api/v1/random") as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.green(),
                    title=":duck: Duck"
                )
                embed.set_image(url=res['url'])

                await ctx.send(embed=embed)
                embed.set_footer(text="Here, take some duck")

                

    @commands.command()
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.green(),
                    title=":panda_face: | Panda"
                )
                embed.set_image(url=res['link'])

                await ctx.send(embed=embed)
                embed.set_footer(text="Here, take some panda")

                

    @commands.command()
    async def redpanda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/red_panda") as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.green(),
                    title=":panda_face: | Red Panda",
                )
                embed.set_image(url=res['link'])
                embed.set_footer(text="Here, take some red panda")

                await ctx.send(embed=embed)

               

    @commands.command()
    async def catfact(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://cat-fact.herokuapp.com/facts/random') as r:
                res = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.blue(),
                    title="Meow Fact",
                    description=f":cat: | Fact: {res['text']}"
                )

                await ctx.send(embed=embed)

    @commands.command()
    async def triggered(self, ctx):
        picture = ctx.author.avatar_url_as(size=1024, format=None, static_format='png')
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://some-random-api.ml/canvas/triggered?avatar={picture}") as r:
                res = io.BytesIO(await r.read())
                triggered_file = discord.File(res, filename=f"triggered.gif")
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="→ Triggered",
                )
                embed.set_image(url="attachment://triggered.gif")

                await ctx.send(embed=embed, file=triggered_file)                


    @commands.command(brief="Gives a random number between 1 and 100")
    async def roll(self, ctx):
        n = random.randrange(1, 101)
        await ctx.send(n)

    @commands.command(brief="Random number between 1 and 6")
    async def dice(self, ctx):
        n = random.randrange(1, 6)
        await ctx.send(n)

    @commands.command()
    async def coin(self, ctx):
        n = random.randint(0, 1)
        await ctx.send("Heads" if n == 1 else "Tails")


    @commands.command(aliases=['banner'])
    async def serverbanner(self, ctx):
        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title="Server Banner",
        )
        embed.set_image(url=ctx.guild.icon_url_as(size=1024, format=None, static_format="png"))

        await ctx.send(embed=embed)
   
    @commands.command()
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"

        first = random.choice(emojis)
        second = random.choice(emojis)
        third = random.choice(emojis)

        slot_machine = f"{first} | {second} | {third}"

        embed = discord.Embed(title="Slot Machine", description = "", color=discord.Colour.blurple())

        if first == second == third:
            embed.add_field(name="**Winner! All Matching Fruits!**", value=slot_machine)
        elif (first == second) or (first == third) or (second == third):
            embed.add_field(name="**Winner! Two in a Row!**", value=slot_machine)
        else:
            embed.add_field(name="**Loser! No Matches!**", value=slot_machine)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def wiki(self, ctx, *, search: str = None):
        '''Addictive Wikipedia results'''
        if search == None:
            await ctx.channel.send(f'Usage: `{ctx.prefix}wiki [search terms]`')
            return

        results = wikipedia.search(search)
        if not len(results):
            no_results = await ctx.channel.send("Sorry, didn't find any result.")
            await asyncio.sleep(5)
            await ctx.message.delete(no_results)
            return

        newSearch = results[0]
        try:
            wik = wikipedia.page(newSearch)
        except wikipedia.DisambiguationError:
            more_details = await ctx.channel.send('Please input more details.')
            await asyncio.sleep(5)
            await ctx.message.delete(more_details)
            return

        emb = discord.Embed()
        emb.color = discord.Colour.purple()
        emb.title = wik.title
        emb.url = wik.url
        textList = textwrap.wrap(wik.content, 1000, break_long_words=True, replace_whitespace=False)
        emb.add_field(name="Wikipedia Results", value=textList[0] + "...")
        await ctx.send(embed=emb)

    @commands.command()
    async def reverse(self, ctx, *, msg: str = None):
        '''Writes backwards because reasons, in Embed.'''
        e = discord.Embed()
        e.colour = discord.Colour.purple()
        if msg is None:
            usage = 'Write a message after command'
            e.description = usage
        else:
            e.description = f'\N{LEFTWARDS BLACK ARROW} `{msg.lower()[::-1]}`'
        await ctx.send(embed=e)

    @commands.command(aliases=['rock', 'paper', 'scissors', 'lizard', 'spock', 'rps'])
    async def settle(self, ctx, your_choice : RPSLSParser= None):
        '''Play rock paper scissors, lizard spock '''
        if your_choice != None:
            author = ctx.message.author.display_name
            grok = self.bot.user.name
            player_choice = your_choice.choice
            available = RPSLS.rock, RPSLS.paper, RPSLS.scissors, RPSLS.lizard, RPSLS.spock
            bot_choice = random.choice((available))
            cond = {
                    (RPSLS.rock,     RPSLS.paper)    : False,
                    (RPSLS.rock,     RPSLS.scissors) : True,
                    (RPSLS.rock,     RPSLS.lizard)   : True,
                    (RPSLS.rock,     RPSLS.spock)    : False,
                    (RPSLS.paper,    RPSLS.rock)     : True,
                    (RPSLS.paper,    RPSLS.scissors) : False,
                    (RPSLS.paper,    RPSLS.lizard)   : False,
                    (RPSLS.paper,    RPSLS.spock)    : True,
                    (RPSLS.scissors, RPSLS.rock)     : False,
                    (RPSLS.scissors, RPSLS.paper)    : True,
                    (RPSLS.scissors, RPSLS.lizard)   : True,
                    (RPSLS.scissors, RPSLS.spock)    : False,
                    (RPSLS.lizard,   RPSLS.rock)     : False,
                    (RPSLS.lizard,   RPSLS.paper)    : True,
                    (RPSLS.lizard,   RPSLS.scissors) : False,
                    (RPSLS.lizard,   RPSLS.spock)    : True,
                    (RPSLS.spock,    RPSLS.rock)     : True,
                    (RPSLS.spock,    RPSLS.paper)    : False,
                    (RPSLS.spock,    RPSLS.scissors) : True,
                    (RPSLS.spock,    RPSLS.lizard)   : False
                   }
            em = discord.Embed()
            em.color = discord.Colour.purple()
            em.add_field(name=f'{author}', value=f'{player_choice.value}', inline=True)
            em.add_field(name=f'{grok}', value=f'{bot_choice.value}', inline=True)
            if bot_choice == player_choice:
                outcome = None
            else:
                outcome = cond[(player_choice, bot_choice)]
            if outcome is True:
                em.set_footer(text="You win!")
                await ctx.send(embed=em)
            elif outcome is False:
                em.set_footer(text="You lose...")
                await ctx.send(embed=em)
            else:
                em.set_footer(text="We're square")
                await ctx.send(embed=em)
        else:
            msg = 'rock, paper, scissors, lizard, OR spock'
            await ctx.send(f'Enter: `{ctx.prefix}{ctx.invoked_with} {msg}`', delete_after=5)


	
    @commands.command()
    async def guess(self,ctx, number: int):
        """Write a number between 1 and 10"""
        answer = random.randint(1, 10)

        e = discord.Embed()
        e.colour = discord.Colour.purple()
        if number < answer or number > answer:
            q_mark = '\N{BLACK QUESTION MARK ORNAMENT}'
            guessed_wrong = [
                'Not even close, the right number was:',
                'Better luck next time, the number was:',
                'How could you have known that the number was:',
                'Hmm, well, the right number was:',
                'Not getting any better, the number was:',
                'Right number was:'
                ]
            e.add_field(name=f'{q_mark} Choice: `{number}`', 
                        value=f'```{random.choice(guessed_wrong)} {answer}```', inline=True)
            try:
                await ctx.send(embed=e)
            except discord.HTTPException:
                em_list = await embedtobox.etb(e)
                for page in em_list:
                    await ctx.send(page)

        if number is answer:
            q_mark = '\N{BLACK QUESTION MARK ORNAMENT}'
            guessed_right = [
                'You guessed correctly!',
                'Everyone knew you could do it!',
                'You got the right answer!',
                'History will remember you...'
                ]
            e.add_field(name=f'{q_mark} Correct number: `{answer}`', 
                        value=f'```{random.choice(guessed_right)}```', inline=True)
            try:
                await ctx.send(embed=e)
            except discord.HTTPException:
                em_list = await embedtobox.etb(e)
                for page in em_list:
                    await ctx.send(page)
        else:
            return



def setup(bot):
    bot.add_cog(Misc(bot))