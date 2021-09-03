import discord
from discord.ext import commands
from ext import embedtobox
import random


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def channels(self, ctx, serverid:int = None):
        """Shows ALL channels, use wisely!"""

        if serverid is None:
            server = ctx.guild
        else:
            if server is None:
                return await ctx.send('Server not found!')

      
      

        voice = ''
        text = ''
        categories = ''

        for channel in server.voice_channels:
            voice += f'\U0001f508 {channel}\n'
        for channel in server.categories:
            categories += f'\U0001f4da {channel}\n'
        for channel in server.text_channels:
            text += f'\U0001f4dd {channel}\n'
        
        e = discord.Embed(color = discord.Colour.blurple())

        if len(server.text_channels) > 0:
            e.add_field(name='Text Channels', value=f'{text}')
        if len(server.categories) > 0:
            e.add_field(name='Categories', value=f'{categories}')
        if len(server.voice_channels) > 0:
            e.add_field(name='Voice Channels', value=f'{voice}')

        try:
            await ctx.send(embed=e)
        except discord.HTTPException:
            em_list = await embedtobox.etb(e)
            for page in em_list:
                await ctx.send(page)

 
                


    @commands.command(aliases=['server','si','svi'], no_pm=True)
    @commands.guild_only()
    async def serverinfo(self, ctx, server_id : int=None):
        '''See information about the server.'''
        server = ctx.guild
        text_channels = len([x for x in server.channels if isinstance(x, discord.TextChannel)])
        voice_channels = len([x for x in server.channels if isinstance(x, discord.VoiceChannel)])
        categories = len(server.channels) - text_channels - voice_channels
        passed = (ctx.message.created_at - server.created_at).days
        created_at = ":calendar: Since {}. That's over {} days ago!".format(server.created_at.strftime("%d %b %Y %H:%M"), passed)
        total_text_channels = len(server.text_channels)
        total_voice_channels = len(server.voice_channels)
        total_channels = total_text_channels + total_voice_channels


        data = discord.Embed(colour = discord.Colour.blurple() , description=created_at)
        data.add_field(name=":flag_eu: Region", value=str(server.region))
        data.add_field(name="<:boost:827513613517979668> Boosters",
	                value=server.premium_subscription_count)
        data.add_field(name=":hash: Channels", value=total_channels)          
        data.add_field(name=":pencil: Text Channels", value=text_channels)
        data.add_field(name=":speaking_head: Voice Channels", value=voice_channels)
        data.add_field(name="<:category:827512249789972521> Categories", value=categories)
        data.add_field(name=":closed_book: Roles", value=len(server.roles))
        data.add_field(name=":crown: Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + str(server.id))
        data.set_author(name=server.name, icon_url=None or server.icon_url)
        data.set_thumbnail(url=None or server.icon_url)
        try:
            await ctx.send(embed=data)
        except discord.HTTPException:
            em_list = await embedtobox.etb(data)
            for page in em_list:
                await ctx.send(page)

  

    @commands.command(aliases=['ui'], no_pm=True)
    @commands.guild_only()
    async def userinfo(self, ctx, *, member : discord.Member=None):
        '''Get information about a member of a server'''
        server = ctx.guild
        user = member or ctx.message.author
        avi = user.avatar_url
        if len(user.roles) > 1:
		       role_string = ' '.join([r.mention for r in user.roles][1:])  
        perm_string = ', '.join([
	         str(p[0]).replace("_", " ").title() for p in user.guild_permissions
	         if p[1]
	      ])
        roles = sorted(user.roles, key=lambda c: c.position)
        for role in roles:
            if str(role.color) != "#000000":
                color = role.color
        if 'color' not in locals():
            color = 0


        time = ctx.message.created_at
        desc = '{0} is chilling in {1} mode.'.format(user.name, user.status)

        em = discord.Embed(colour=color, description=desc, timestamp=time)
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name=':pencil: Account Created', value=user.created_at.__format__('%A, %d. %B %Y'))
        em.add_field(name=':inbox_tray: Join Date', value=user.joined_at.__format__('%A, %d. %B %Y'))
        em.add_field(name=":medal: Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
        em.add_field(name=":book: Permisions", value=perm_string, inline=False)
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url=server.icon_url)

        try:
            await ctx.send(embed=em)
        except discord.HTTPException:
            em_list = await embedtobox.etb(em)
            for page in em_list:
                await ctx.send(page)

    

             

    @commands.command(aliases=["ri","role"], no_pm=True)
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        '''Shows information about a role'''
        guild = ctx.guild

        since_created = (ctx.message.created_at - role.created_at).days
        role_created = role.created_at.strftime("%d %b %Y %H:%M")
        created_on = "{} ({} days ago!)".format(role_created, since_created)
        members = ''
        i = 0
        for user in role.members:
            members += f'{user.name}, '
            i+=1
            if i > 30:
                break

        if str(role.colour) == "#000000":
            colour = "default"
            color = ("#%06x" % random.randint(0, 0xFFFFFF))
            color = int(colour[1:], 16)
        else:
            colour = str(role.colour).upper()
            color = role.colour

        em = discord.Embed(colour=color)
        em.set_author(name=role.name)
        em.add_field(name=":bust_in_silhouette: Users", value=len(role.members))
        em.add_field(name="Mentionable", value=role.mentionable)
        em.add_field(name="Hoist", value=role.hoist)
        em.add_field(name="Position", value=role.position)
        em.add_field(name="Managed", value=role.managed)
        em.add_field(name="Colour", value=colour)
        em.add_field(name='Creation Date', value=created_on)
        em.add_field(name='Members', value=members[:-2], inline=False)
        em.set_footer(text=f'Role ID: {role.id}')

        await ctx.send(embed=em)


   

def setup(bot):
	bot.add_cog(Information(bot))