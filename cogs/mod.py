import discord
from discord.ext import commands
import asyncio



class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def format_mod_embed(self, ctx, user, success, method, duration = None, location=None):
        '''Helper func to format an embed to prevent extra code'''
        emb = discord.Embed(timestamp=ctx.message.created_at)
        emb.set_author(name=method.title(), icon_url=user.avatar_url)
        emb.color = discord.Colour.orange()
        emb.set_footer(text=f'User ID: {user.id}')
        if success:
            
            if method == 'ban' or method == 'hackban':
                emb.description = f'{user} was just {method}ned.'
            elif method == 'unmute':
                emb.description = f'{user} was just {method}d.'
            elif method == 'mute':
                emb.description = f'{user} was just {method}d for {duration}.'
            elif method == 'channel-lockdown' or method == 'server-lockdown':
                emb.description = f'`{location.name}` is now in lockdown mode!'
            else:
                emb.description = f'{user} was just {method}ed.'
        else:
            if method == 'lockdown' or 'channel-lockdown':
                emb.description = f"You do not have the permissions to {method} `{location.name}`"
            else:
                emb.description = f"You do not have the permissions to {method} {user.name}."
      

    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

         await ctx.guild.ban(member, reason=reason)
         
         if reason == None:
           em = discord.Embed(
			     title=f':exclamation: | Ban {member}',
			     description=f'{member} was banned from the server by {ctx.author}',
			     color=discord.Colour.green())
           em.add_field(name="Target", value=f"{member}")
           em.add_field(name="Moderator", value=f"{ctx.author}")
           em.add_field(name="Reason", value=f"none")
           await ctx.send(embed=em)
           
         else:
           em = discord.Embed(
			     title=f':exclamation: | Ban {member}',
			     description=f'{member} was banned from the server by {ctx.author}',
			     color=discord.Colour.green())
           em.add_field(name="Target", value=f"{member}")
           em.add_field(name="Moderator", value=f"{ctx.author}")
           em.add_field(name="Reason", value=f"{reason}")
           await ctx.send(embed=em)
      
    



    @ban.error
    async def ban_error(self, msg,error):
        if isinstance(error, commands.MissingPermissions):
            return await msg.send(em=discord.Embed(title=":exclamarion: | Error", description=""))
  
        

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, name_or_id, *, reason=None):
        '''Unban someone from the server.'''
        ban = await ctx.get_ban(name_or_id)

        try:
            await ctx.guild.unban(ban.user, reason=reason)
        except:
            success = False
        else:
            success = True
        
        emb = await self.format_mod_embed(ctx, ban.user, success, 'unban')

        await ctx.send(embed=emb)

    @commands.command(aliases=['del','prune'])
    @commands.has_permissions(kick_members=True)
    async def purge(self, ctx, limit : int, member:discord.Member=None):
        '''Clean a number of messages'''
        if member is None:
            await ctx.purge(limit=limit+1)
        else:
            async for message in ctx.channel.history(limit=limit+1):
                if message.author is member:
                    await message.delete()

    @commands.command()
    async def clean(self, ctx, quantity: int):
        ''' Clean a number of your own messages
        Usage: {prefix}clean 5 '''
        if quantity <= 15:
            total = quantity +1
            async for message in ctx.channel.history(limit=total):
                if message.author == ctx.author:
                    await message.delete()
                    await asyncio.sleep(3.0)
        else:
            async for message in ctx.channel.history(limit=6):
                if message.author == ctx.author:
                    await message.delete()
                    await asyncio.sleep(3.0)

    @commands.command()
    async def bans(self, ctx):
        '''See a list of banned users in the guild'''
        try:
            bans = await ctx.guild.bans()
        except:
            return await ctx.send('You dont have the perms to see bans.')

        em = discord.Embed(title=f'List of Banned Members ({len(bans)}):')
        em.description = ', '.join([str(b.user) for b in bans])
        em.color = discord.Colour.orange()

        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def baninfo(self, ctx, *, name_or_id):
        '''Check the reason of a ban from the audit logs.'''
        ban = await ctx.get_ban(name_or_id)
        em = discord.Embed()
        em.color = discord.Colour.orange()
        em.set_author(name=str(ban.user), icon_url=ban.user.avatar_url)
        em.add_field(name='Reason', value=ban.reason or 'None')
        em.set_thumbnail(url=ban.user.avatar_url)
        em.set_footer(text=f'User ID: {ban.user.id}')

        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, *, rolename: str):
        '''Add a role to someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        try:
            await member.add_roles(role)
            await ctx.send(f'Added: `{role.name}`')
        except:
            await ctx.send("I don't have the perms to add that role.")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, *, rolename: str):
        '''Remove a role from someone else.'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        try:
            await member.remove_roles(role)
            await ctx.send(f'Removed: `{role.name}`')
        except:
            await ctx.send("I don't have the perms to add that role.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member:discord.Member, duration, *, reason=None):
        '''Denies someone from chatting in all text channels and talking in voice channels for a specified duration'''
        unit = duration[-1]
        if unit == 's':
            time = int(duration[:-1])
            longunit = 'seconds'
        elif unit == 'm':
            time = int(duration[:-1]) * 60
            longunit = 'minutes'
        elif unit == 'h':
            time = int(duration[:-1]) * 60 * 60
            longunit = 'hours'
        else:
            await ctx.send('Invalid Unit! Use `s`, `m`, or `h`.')
            return

        progress = await ctx.send('Muting user!')
        try:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)

            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
        except:
            success = False
        else:
            success = True

        emb = await self.format_mod_embed(ctx, member, success, 'mute', f'{str(duration[:-1])} {longunit}')
        progress.delete()
        await ctx.send(embed=emb)
        await asyncio.sleep(time)
        try:
            for channel in ctx.guild.channels:
                await channel.set_permissions(member, overwrite=None, reason=reason)
        except:
            pass
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member:discord.Member, *, reason=None):
        '''Removes channel overrides for specified member'''
        progress = await ctx.send('Unmuting user!')
        try:
            for channel in ctx.message.guild.channels:
                await channel.set_permissions(member, overwrite=None, reason=reason)
        except:
            success = False
        else:
            success = True
            
        emb = await self.format_mod_embed(ctx, member, success, 'unmute')
        progress.delete()
        await ctx.send(embed=emb)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx):
        """Server/Channel lockdown"""
        pass

    @lockdown.command(aliases=['channel'])
    async def chan(self, ctx, channel:discord.TextChannel = None, *, reason=None):
        if channel is None: channel = ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
        except:
            success = False
        else:
            success = True
        emb = await self.format_mod_embed(ctx, ctx.author, success, 'channel-lockdown', 0, channel)
        await ctx.send(embed=emb)
    
    @lockdown.command()
    async def server(self, ctx, server:discord.Guild = None, *, reason=None):
        if server is None: server = ctx.guild
        progress = await ctx.send(f'Locking down {server.name}')
        try:
            for channel in server.channels:
                await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
        except:
            success = False
        else:
            success = True
        emb = await self.format_mod_embed(ctx, ctx.author, success, 'server-lockdown', 0, server)
        progress.delete()
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def block(self, ctx, user: discord.Member):
        """
        Blocks a user from chatting in current channel.
           
        Similar to mute but instead of restricting access
        to all channels it restricts in current channel.
        """
        

        if not user: # checks if there is user
            return await ctx.send("You must specify a user")
                                
        await ctx.channel.set_permissions(user, send_messages=False)
        embed = discord.Embed(title="Block", description=f"{user} user can no longer write to this channel!")
        

        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unblock(self, ctx, user: discord.Member):
        """Unblocks a user from current channel"""
                                
        if not user: # checks if there is user
            return await ctx.send("You must specify a user")
        
        await ctx.channel.set_permissions(user, send_messages=True) 
        await ctx.channel.set_permissions(user, send_messages=False)
        embed = discord.Embed(title="Unblock", description=f"{user} user can write to this channel!")
        

        await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Mod(bot))