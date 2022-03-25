import math
import discord
import re
import os
import random

from dotenv import load_dotenv
from asyncio import sleep
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup, Option, permissions
from discord.ext.commands.bot import when_mentioned_or


intents = discord.Intents.all()
client = commands.AutoShardedBot(
	intents=intents,
	case_insensitive=True
)
prefix = when_mentioned_or('!')
client.remove_command('help')

owner_id = client.get_user(235071908473733121)
randColour = random.randint(0, 0xffffff)
url_regex = r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\"\.,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"
gifLink = r"https://tenor\.com/.*"
gifLinkTwo = r"https://c\.tenor\.com/.*"
mediaLink = r"https?://media.discordapp.net/.*"
guild_ids = [540954170572931074]


@client.event
async def on_ready():
	print('SCARBot Ready!')
	await client.change_presence(status=discord.Status.online, activity=discord.Game('Developed By Jim Wright'))
	client.command_prefix = prefix

@client.command()
@permissions.is_owner()
async def load(message, extension):
	client.load_extension(f'cogs.{extension}')
	await owner_id.send(f'{extension} was loaded.')

@client.command()
@permissions.is_owner()
async def unload(message, extension):
	client.unload_extension(f'cogs.{extension}')
	await owner_id.send(f'{extension} was unloaded.')

@client.command()
@permissions.is_owner()
async def reload(message, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')
	print(f'{extension} was reloaded.')
	await owner_id.send(f'{extension} was reloaded.')

@client.slash_command(description="Bans a user", guild_ids=guild_ids)
@permissions.has_role("Admin")
async def ban(ctx, member: Option(discord.Member, "User to ban"), *, reason: Option(str, "Reason for ban", default=None)):
	if member is None:
		return await ctx.respond("You must provide a user to ban", ephemeral=True)
	else:
		await member.ban(reason=reason)
		await ctx.respond(f'Banned {member} for {reason}', ephemeral=True)

@client.slash_command(description="Kicks a user", guild_ids=guild_ids)
@permissions.has_role("Admin")
async def kick(ctx, member: Option(discord.Member, "The user to kick"), *, reason: Option(str, "Reason for kick", default=None)):
	if member is None:
		return await ctx.respond("You must provide a user to kick", ephemeral=True)

	await member.kick(reason=reason)
	await ctx.respond(f'{member} has been kicked for {reason}', ephemeral=True)

@client.slash_command(description="Unbans a user", guild_ids=guild_ids)
@permissions.has_role("Admin")
async def unban(ctx, *, member: Option(discord.Member, "The user to kick")):
	if member is None:
		return await ctx.respond("You must provide a user to unban", ephemeral=True)

	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.respond(f'Unbanned {user.name}#{user.discriminator}', ephemeral=True)
			return

@client.slash_command(description="Removes the user's ability to send messages", guild_ids=guild_ids)
@permissions.has_role("Admin")
async def mute(ctx, member: Option(discord.Member, "The user to mute")):
	role = discord.utils.get(member.guild.roles, name='muted')
	if member is None:
		await ctx.respond("Please enter a valid user.", ephemeral=True)
		return

	await member.add_roles(role)
	await ctx.respond(f'{str(member)} has been muted.', ephemeral=True)

@client.slash_command()
@permissions.permission(manage_messages = True)
async def clear(ctx, amount: Option(int, "The amount of messages to remove", default=2)):
	await ctx.channel.purge(limit=amount)



#######################################################EVENTS############################################################

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send('That command does not exist. Use `help` to see a list of commands.')
		print("Someone tried using a command that does not exist.")

	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('You are missing a part of the command. Use `help` to see the proper use of the command.')
		print("Someone tried using a command without a required argument.")

	elif isinstance(error, commands.BadArgument):
		await ctx.send('That argument is incorrect. Use `help` to see the proper use of the command.')
		print("Someone tried to use an incorrect argument in a command.")

	elif isinstance(error, commands.DisabledCommand):
		await ctx.send('That command is disabled. Use `help` to get a list of commands.')
		print('Someone tried to use a disabled command.')

	elif isinstance(error, commands.BotMissingPermissions):
		await ctx.send('I dont have permission to do that, check with Zane to make sure I get the correct permissions.')
		print('The bot was missing permissions to run the command.')

	elif isinstance(error, commands.TooManyArguments):
		await ctx.send('You added too many arguments. Use `help` to see the proper use of the command.')
		print('Someone added too many arguments when using a command.')

	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send('That command is on cooldown. Please wait to use it again.')
		print('Someone used a command while it was on cooldown.')

	elif isinstance(error, commands.MissingRole):
		await ctx.send(
			f'You need the `{error.missing_role}` role to use that command, message an admin to get this fixed.')
		print(f'Someone was missing the {error.missing_role} role for a command.')

	else:
		print(error)

@client.event
async def on_message(message: discord.Message):
	if not message.guild:
		return print("Someone DM'd the bot.")
	else:
		return await client.process_commands(message)
	"""
	#Checks if a link was posted in a non links channel
	if re.search(url_regex, message.content) and message.channel.name != "links": if re.search(gifLink,
		message.content) or re.search(gifLinkTwo, message.content) or re.search(mediaLink, message.content): return await
		client.process_commands(message) else: await dest.send(f'{message.author.mention} Posted this link in another
		channel. I moved it here. \n \n {message.content}') await message.delete()
	"""

@client.event
async def on_member_join(member):
	ruleList = [
		'`1.` '
	]
	page = 1
	items_per_page = 100
	pages = math.ceil(len(ruleList) / items_per_page)
	start = (page - 1) * items_per_page
	end = start + items_per_page
	rule_list = ''

	for i, rule in enumerate(ruleList[start:end], start=start):
		rule_list += f'{rule}\n'

	e = discord.Embed(
		title= 'Rules of SCAR Airsoft Discord',
		description= f'{rule_list}',
		colour = randColour
	)


	welcome = discord.utils.get(client.get_all_channels(), guild__name="Bot Testing", name="general")
	hello = client.get_channel(welcome.id)

	await hello.send(f'Welcome {member.mention} to the SCAR Airsoft Discord!!')
    
	await member.send(f'Welcome {member.display_name} to the SCAR Airsoft Discord.')
	await member.send(embed=e)


load_dotenv()
client.run(os.getenv('TOKEN'))
