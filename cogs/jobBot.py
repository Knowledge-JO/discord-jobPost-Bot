import asyncio
import time
import discord
from discord.ext import commands
questions = ['What role are you looking for?', 'What would compensation be? (upfront payment, weekly payment, mint% amount, etc)', 'Project Details? (Name, social links, discord link, etc)']
channel_id = 000000000000000000
class Post(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.inputs = []
		

	@commands.command()
	@commands.has_any_role('Administrator', 'Founder')
	async def post(self, ctx):
		#embed = discord.Embed(title='New Job Posting', color=0x00000)
		await ctx.message.delete()
		try:
			for i in questions:
				job_post = discord.Embed(title=i, color=0x00000)
				sent = await ctx.send(embed=job_post)

				
				msg = await self.bot.wait_for("message", timeout=60, check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
				if msg:
					await sent.delete()
					time.sleep(3)
					await msg.delete()
					#await ctx.send(msg.content)
					self.inputs.append(msg.content)

			embed = discord.Embed(title='New Job Posting', color=0x00000)
			embed.add_field(name='What role are you looking for?', value = self.inputs[0], inline = False)
			embed.add_field(name='What would compensation be? (upfront payment, weekly payment, mint% amount, etc)', value = self.inputs[1], inline = False)
			embed.add_field(name='Project Details? (Name, social links, discord link, etc)', value = self.inputs[2], inline = False)
			embed.add_field(name='react to this message if you are Eligible for this role', value="if you are not, you won't be considered even if you react")
			self.channel = self.bot.get_channel(channel_id)
			self.mssg = await self.channel.send(embed=embed)
			await self.mssg.add_reaction('✅')

			self.inputs.clear()


		except asyncio.TimeoutError:
			await sent.delete()
			await ctx.send("canceling due to timeout", delete_after=10)
			self.inputs.clear()


	@commands.command()
	@commands.has_any_role('Administrator', 'Founder')
	async def finish(self, ctx, arg):
		await ctx.message.delete()
		self.volunteers = []
		self.message= await self.channel.fetch_message(self.mssg.id)
		#print(self.message.reactions)
		for reaction in self.message.reactions:
			i = await reaction.users().flatten()
			for user in i:
				if user.bot == False:
					self.volunteers.append(str(user))
		#await self.message.delete()
		reg = ''
		arg = int(arg)
		for i in self.volunteers[:arg]:
			reg+=f'{i}\n'
		r = discord.Embed(title=f'''Volunteers''', color=0x00000)
		r.add_field(name='Volunteered for the role', value=f'{reg}')
		channel = self.bot.get_channel(channel_id)
		await channel.send(embed=r)
		self.volunteers.clear()
		reg = ''

	@commands.command()
	async def hello(self, ctx):
		await ctx.message.delete()
		user = ctx.author.id
		channel = self.bot.get_channel(channel_id)
		msg = await channel.send(f'Hello <@{user}>')
		time.sleep(2)
		mssg = await channel.fetch_message(msg.id)
		time.sleep(5)
		await mssg.delete()


def setup(bot):
	bot.add_cog(Post(bot))
