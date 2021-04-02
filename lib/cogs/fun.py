from random import choice, randint
from typing import Optional
from aiohttp import request
from discord.ext.commands import BadArgument
from discord import Member, Embed
from discord.errors import HTTPException
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown, has_permissions
from discord.ext.commands import CheckFailure
import random
from discord.ext.commands import has_any_role, has_role
import discord
from datetime import datetime
import asyncio
from discord.ext import commands, menus
import discord
import random
import logging
from urllib.parse import quote as uriquote
import yarl
import io
import re

# |CUSTOM|
embed_color = 0x000000
server_logo = "https://cdn.discordapp.com/attachments/819152230543654933/819153523190005782/server_logo_final.png"
# |CUSTOM|

#IMPPORTANT | All the details for command help (for example command description or command brief) is written WITH THE COMMAND ITSELF-
class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.allowed_channels = (803031892235649044, 803029543686242345, 803033569445675029, 823130101277261854,
		 826442024927363072, 818444886243803216)

	#FLIP COMMAND
	@command(name="flip", brief="Flip a Coin", help="Flips either Heads or Tails")
	@cooldown(3, 60, BucketType.user)
	async def flip(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			n = random.randint(0, 1)
			description="Heads" if n == 1 else "Tails"
			embed = Embed(description=f"**You flipped {description}!**", color=embed_color)
			await ctx.reply(embed=embed)


	#URBAN COMMAND
	@command(name="urban", brief="Urban Command", he="Sends meaning of any word", hidden=False)
	@cooldown(3, 30, BucketType.user)
	async def _urban(self, ctx, *, word):
		url = 'http://api.urbandictionary.com/v0/define'
		async with ctx.session.get(url, params={'term': word}) as resp:
			if resp.status != 200:
				return await ctx.send(f'An error occurred: {resp.status} {resp.reason}')
			js = await resp.json()
			data = js.get('list', [])
			if not data:
				return await ctx.send('No results found, sorry.')

		pages = RoboPages(UrbanDictionaryPageSource(data))
		try:
			await pages.start(ctx)
		except menus.MenuError as e:
			await ctx.send(e)


	#ROLL COMMAND
	@command(name="roll", brief="Roll A Number", help="Rolls a random number in between 1-100")
	@cooldown(3, 60, BucketType.user)
	async def roll(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			n = random.randrange(1, 101)
			embed = Embed(description=f"You rolled **{n}**", color=embed_color)
			await ctx.reply(embed=embed)
    

    #HELLO COMMAND
	@command(name="hello", aliases=["hi"], brief="Say Hello ",help="Sends a greeting!")
	@cooldown(3, 60, BucketType.user)
	async def say_hello(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			embed=Embed(title=f"{choice(('Hows it going?', 'Hey mate, sup?', 'Hows it hanging?', 'Yo Yo Yo'))}",color=embed_color)		
			await ctx.reply(embed=embed)


	#SLAP COMMAND
	@command(name="slap", aliases=["hit"], brief="Slap A Member",help="Slaps a guild member.")
	@cooldown(3, 60, BucketType.user)
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			embed=Embed(title=(f":flushed: {ctx.author.display_name} slapped you {reason}"),color=embed_color)		
			await ctx.send(ctx.author.mention,embed=embed)

	@slap_member.error
	async def slap_member_error (self, ctx, exc):
		if isinstance(exc, BadArgument):
			embed=Embed(title="I cant find that member.",color=embed_color)			
			await ctx.reply(embed=embed)

	#PING MUTED MEMBERS COMMAND
	@command(name="pingmuted", aliases=["pingm"],brief="Ping Muted Members", help="Pings muted members so that they can recieve the gulag role", hidden=True)
	@has_any_role('Chad', 'Admin', 'Executive')
	async def ping_muted(self, ctx):
		embed = Embed(title="Welcome To The Gulag", 
					description="In order to unlock the gulag text and voice channel, React to the bots **Reaction message** .\nScroll up or click this link. \nhttps://discord.com/channels/803028981698789407/816992178877366282/816992939912986666\nGood luck begging for mercy...",
					color = 0x000000)
		await ctx.message.delete()
		await self.gulag_channel.send("<@&821503690405183501>", embed=embed, delete_after=86400)
	
	@ping_muted.error
	async def ping_muted_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed,delete_after=10)

	#MEMBER COUNT COMMAND
	@command(name="membercount", aliases=["members"], brief="Member Count", help="Displays the number of members present in the server")
	@cooldown(3, 60, BucketType.user)
	async def member_count(self,ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000, timestamp=datetime.utcnow())
			await ctx.reply(embed=embed)
		
		else:
			embed = Embed(title="Member Count", color=0x000000)
			fields = [("Members", len(ctx.guild.members), False),
					("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))),False),
					("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), False)]
			for name , value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			embed.set_thumbnail(url=ctx.guild.icon_url)
			await ctx.reply(embed=embed)


	#SEND EMBEDS COMMAND
	@command(name="embed",brief="Send Embeds",help="Send embeds throught the bot.", hidden=True)
	@has_any_role('Admin','Chad','Executive')
	async def say_embed(self, ctx, *, message):	
		embed=Embed(description=f"{message}",color=embed_color)
		await ctx.send(embed=embed)
		await ctx.message.delete()
	
	@say_embed.error
	async def say_embed_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.message.delete(delay=60)
			await ctx.reply(ctx.author.mention,embed=embed,delete_after=10)
    

    #SEND MESSAGES COMMAND
	@command(name="say",brief="Send Messages",help="Send a message throught the bot.", hidden=True)
	@has_any_role('Admin','Chad','Executive')
	async def say_message(self, ctx,*, message):		
		await ctx.send(f"{message}")
		await ctx.message.delete()

	@say_message.error
	async def say_message_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			embed = Embed(title="Permission Not Granted",description=":x: **Insufficient permissions to perform that task**", color=0x002eff)			
			await ctx.reply(embed=embed,delete_after=10)

    #BYE COMMAND
	@command(name="bye", aliases=["later"],brief="Say Bye ",help="Sends a farewell message!")
	@cooldown(3, 60, BucketType.user)
	async def say_bye(self, ctx):
		if ctx.channel.id not in self.allowed_channels:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
		
		else:
			embed=Embed(title=(f"{choice(('Catch you later!', 'See you soon!', 'Have a good one!', 'Bye!!', 'See you around!'))}"),color=0x000000)		
			await ctx.reply(embed=embed)


    #API | ANIMAL FACTS
	@command(name="afact", brief="Animal Facts",help="Sends an intersting fact reguarding the given animal. Avaliable animals include __cat__, __dog__, __bird__ and __koala__.")
	@cooldown(3, 60, BucketType.user)
	async def animal_fact(self, ctx, animal: str):
		if ctx.channel.id in self.allowed_channels:
			if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
				fact_url = f"https://some-random-api.ml/facts/{animal}"
				image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

				async with request("GET", image_url, headers={}) as response:
					if response.status == 200:
						data = await response.json()
						image_link = data["link"]

					else:
						image = None

				async with request("GET", fact_url, headers={}) as response:
					if response.status == 200:
						data = await response.json()

						embed = Embed(title=f"{animal.title()} fact",
							description=data["fact"],
							color=0x000000)
						if image_link is not None:
							embed.set_image(url=image_link)
							embed.set_footer(text =f"Requested By {ctx.author.display_name}",
								 			icon_url=f"{ctx.author.avatar_url}")
						
						await ctx.reply(embed=embed)

					else:
						await ctx.send(f"API returned a {response.status} status.",color=0x000000)
				
			else:
				embed=Embed(title="Something Went Wrong",description="You have either entered an invalid animal or some arguments are missing.\n Try one of the avalaible animals in lowercase, which include __*cat, dog, bird and koala*__",color=0x000000)
				embed.set_footer(text =f"Requested By {ctx.author.display_name}",
								 icon_url=f"{ctx.author.avatar_url}")
				await ctx.reply(embed=embed)

		else:
			embed = Embed(title="Blacklisted Channel", description=f"{ctx.channel.mention}  **Is blacklisted for bot commands, please use  <#803031892235649044>**", color=0x000000)
			await ctx.reply(embed=embed)
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.gulag_channel = self.bot.get_channel(816992178877366282)
			self.bot.cogs_ready.ready_up("fun") #IMPORTANT! - ("Fun") is the FILE NAME, NOT print name. 

def setup(bot):
	bot.add_cog(Fun(bot))
