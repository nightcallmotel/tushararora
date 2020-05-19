import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import platform
import colorsys
import random
import os
import time
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType

Forbidden= discord.Embed(title="Permission Denied", description="1) Please check whether you have permission to perform this action or not. \n2) Please check whether my role has permission to perform this action in this channel or not. \n3) Please check my role position.", color=0x00ff00)
client = Bot(description="best moderation bot", command_prefix="%", pm_help = True)
client.remove_command('help')


async def status_task():
    while True:
        await client.change_presence(game=discord.Game(name='for %help'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='with '+str(len(set(client.get_all_members())))+' users'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='in '+str(len(client.servers))+' servers'))
        await asyncio.sleep(5)
        

	
@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('--------')
    print('Started Direct Message BOT')
    print('Created by low')
    client.loop.create_task(status_task())


  
	
def is_owner(ctx):
    return ctx.message.author.id == "611122880952008704","611122880952008704"

 
@client.command(pass_context = True)
@commands.check(is_owner)
async def restart():
    await client.logout()

@client.event
async def on_message(message):
	await client.process_commands(message)


@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)

async def unbanall(ctx):
    server=ctx.message.server
    ban_list=await client.get_bans(server)
    await client.say('Unbanning {} members'.format(len(ban_list)))
    for member in ban_list:
        await client.unban(server,member)
	
@client.command(pass_context = True)
@commands.has_permissions(kick_members=True) 

@commands.cooldown(rate=5,per=86400,type=BucketType.user) 
async def access(ctx, member: discord.Member):
    role = discord.utils.get(member.server.roles, name='Access')
    await client.add_roles(member, role)
    embed=discord.Embed(title="User Got Access!", description="**{0}** got access from **{1}**!".format(member, ctx.message.author), color=0xff00f6)
    await client.say(embed=embed)
    await asyncio.sleep(45*60)
    await client.remove_roles(member, role)
	

	
@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)
async def getuser(ctx, role: discord.Role = None):
    if role is None:
        await client.say('There is no "STAFF" role on this server!')
        return
    empty = True
    for member in ctx.message.server.members:
        if role in member.roles:
            await client.say("{0.name}: {0.id}".format(member))
            empty = False
    if empty:
        await client.say("Nobody has the role {}".format(role.mention))
	

@commands.has_permissions(administrator=True)
@client.command(pass_context = True)
async def send(ctx, *, content: str):
        for member in ctx.message.server.members:
            try:
                await client.send_message(member, content)
                await client.say("DM Sent To : {} :white_check_mark:  ".format(member))
            except:
                print("can't")
                await client.say("DM can't Sent To : {} :x: ".format(member))
		

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def joinvoice(ctx):
    author = ctx.message.author
    channel = author.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True, aliases=['em', 'e'])
async def modmail(ctx, *, msg=None):
    channel = discord.utils.get(client.get_all_channels(), name='📬mod-mails📬')
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    color = discord.Color((r << 16) + (g << 8) + b)
    if not msg:
        await client.say("Please specify a message to send")
    else:
        await client.send_message(channel, embed=discord.Embed(color=color, description=msg + '\n Message From-' + ctx.message.author.id))
        await client.delete_message(ctx.message)
    return

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)     
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)
 
@client.command(pass_context = True)

@commands.has_permissions(manage_roles=True)     
async def role(ctx, user: discord.Member, *, role: discord.Role = None):
        if role is None:
            return await client.say("You haven't specified a role! ")

        if role not in user.roles:
            await client.add_roles(user, role)
            return await client.say("{} role has been added to {}.".format(role, user))

        if role in user.roles:
            await client.remove_roles(user, role)
            return await client.say("{} role has been removed from {}.".format(role, user))
 
@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, userName: discord.User, *, message:str): 
    await client.send_message(userName, "You have been warned for: **{}**".format(message))
    await client.say(":warning: __**{0} Has Been Warned!**__ :warning: ** Reason:{1}** ".format(userName,message))
    pass

@client.command(pass_context=True)
async def ownerinfo(ctx):
    embed = discord.Embed(title="Information about owner", description="Bot Name- JARVIS", color=0x00ff00)
    embed.set_footer(text="Copyright@HAEMAN")
    embed.set_author(name=" Bot Owner Name- R€FL€X | HARMAN #3398: Id 611122880952008704")
    embed.add_field(name="Server https://discord.gg/vTF9PPm", value="Thanks for adding our bot", inline=True)
    await client.say(embed=embed)
    
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def setup(ctx):
    author = ctx.message.author
    server = ctx.message.server
    mod_perms = discord.Permissions(manage_messages=True, kick_members=True, manage_nicknames =True,mute_members=True)
    admin_perms = discord.Permissions(ADMINISTRATOR=True)

    await client.create_role(author.server, name="Owner", permissions=admin_perms)
    await client.create_role(author.server, name="Admin", permissions=admin_perms)
    await client.create_role(author.server, name="Senior Moderator", permissions=mod_perms)
    await client.create_role(author.server, name="G.O.H")
    await client.create_role(author.server, name="Moderator", permissions=mod_perms)
    await client.create_role(author.server, name="Muted")
    
    await client.create_role(author.server, name="Friend of Owner")
    await client.create_role(author.server, name="Verified")
    everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
    user_perms = discord.PermissionOverwrite(read_messages=True)
    user = discord.ChannelPermissions(target=server.default_role, overwrite=user_perms)
    private_perms = discord.PermissionOverwrite(read_messages=False)
    private = discord.ChannelPermissions(target=server.default_role, overwrite=private_perms)    
    await client.create_channel(author.server, '🎉welcome🎉',everyone)
    await client.create_channel(author.server, '🎯rules🎯',everyone)
    await client.create_channel(author.server, '🎥featured-content🎥',everyone)
    await client.create_channel(author.server, '📢announcements📢',everyone)
    await client.create_channel(author.server, '📢vote_polls📢',everyone)
    await client.create_channel(author.server, 'private_chat',private)
    await client.create_channel(author.server, '🎮general_chat🎮',user)
    await client.create_channel(author.server, '🎮general_media🎮',user)
    await client.create_channel(author.server, '👍bots_zone👍',user)
    await client.create_channel(author.server, '🎥youtube_links🎥',user)
    await client.create_channel(author.server, '🎥giveaway_links🎥',user)
    await client.create_channel(author.server, '🎥other_links🎥',user)
    await client.create_channel(author.server, '🔥Music Zone🔥', type=discord.ChannelType.voice)
    await client.create_channel(author.server, '🔥music_command🔥s',user)
    await client.create_channel(author.server, '🔥Chill Zone🔥', type=discord.ChannelType.voice)
    
@client.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await client.change_nickname(user, nickname)
    await client.delete_message(ctx.message)

@client.command(pass_context=True)
async def poll(ctx, question, *options: str):
        if len(options) <= 1:
            await client.say('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await client.say('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['👍', '👎']
        else:
            reactions = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=question, description=''.join(description), color = discord.Color((r << 16) + (g << 8) + b))
        react_message = await client.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await client.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await client.edit_message(react_message, embed=embed)
        
@client.command(pass_context = True)
async def googlefy(ctx, *, msg = None):
    if msg.content == "@everyone":
        return
    if msg.content == "@here":
        return
    if not msg: await client.say("Please specify a string")
    else:
        await client.say('http://lmgtfy.com/?q=' + msg)
    return

@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Help')
    embed.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
    embed.add_field(name = '``Our Help Server Link`` ',value ='https://discord.gg/vTF9PPm',inline = False)
    embed.add_field(name = '%modhelp ',value ='Explaines all the commands which are only usable by Those who has moderation permissions. Like- Manage Nicknames, Manage Messages, Kick/Ban Members,etc.',inline = False)
    embed.add_field(name = '%funhelp ',value ='Explaines all the commands which are usable by everyone.',inline = False)
    await client.send_message(author,embed=embed)
    await client.say('📨 Check DMs For Information')
@client.command(pass_context = True)
async def modhelp(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Moderation Commands Help')
    embed.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
    embed.add_field(name = '%say(Admin permission required) ',value ='Use it like ``%say <text>``',inline = False)
    embed.add_field(name = '%embed(Admin permission required) ',value ='Use it like ``%embed <text>``',inline = False)
    embed.add_field(name = '%membercount(Kick members Permission Required) ',value ='Use it like ``%membercount`` to get membercount',inline = False)
    embed.add_field(name = '%removemod(Admin Permission Required)',value ='Use it like ``%removemod @user`` to remove him from mod. Note-You need Moderator role in your server below darkbot to use it.',inline = False)
    embed.add_field(name = '%makemod(Admin Permission Required)',value ='Use it like ``%makemod @user`` to make him mod. Note-You need Moderator role in your server below darkbot to use it.',inline = False)
    embed.add_field(name = '%setup(Admin Permission Required)',value ='Use it to add channels, voice channels and roles if your server is not developed currently and you have just 1-2 channels. Note- Use it only 1 time. If you will use same command again then it will do same thing again .i.e It will add true copy of previous channels + true copy of roles that made in previous command use. So be careful.',inline = False)
    embed.add_field(name = '%friend(Admin Permission Required) ',value ='Use it like ``%friend @user`` to give anyone Friend of Owner role',inline = False)
    embed.add_field(name = '%role(Manage Roles Permission Required)',value ='Use it like ``%role @user <rolename>``.',inline = False)
    embed.add_field(name = '%setnick(Manage nickname permission required)',value ='Use it like ``%setnick @user <New nickname>`` to change the nickname of tagged user.',inline = False)
    embed.add_field(name = '%english(Kick members Permission Required)',value ='Use it like ``%english @user`` when someone speaks languages other than English.',inline = False)
    embed.add_field(name = '%serverinfo(Kick members Permission Required) ',value ='Use it like ``%serverinfo`` to get server info',inline = False)
    embed.add_field(name = '%userinfo(Kick members Permission Required) ',value ='Use it like ``%userinfo @user`` to get some basic info of tagged user',inline = False)
    embed.add_field(name = '%kick(Kick members Permission Required)',value ='Use it like ``%kick @user`` to kick any user',inline = False)
    embed.add_field(name = '%roles(Kick members Permission Required) ',value ='Use it to check roles present in server',inline = False)
    embed.add_field(name = '%clear(Manage Messages Permission Required)',value ='Use it like ``%clear <number>`` to clear any message',inline = False)
    embed.add_field(name = '%mute(Mute members Permission Required)',value ='Use it like ``%mute @user <time>`` to mute any user',inline = False)
    embed.add_field(name = '%unmute(Mute members Permission Required) ',value ='Use it like ``%unmute @user`` to unmute anyone',inline = False)
    embed.add_field(name = '%ban(Ban members Permission Required) ',value ='Use it like ``%ban @user`` to ban any user',inline = False)
    embed.add_field(name = '%rules(Kick members Permission Required)',value ='Use it like ``%rules @user <violation type>`` to warn user',inline = False)
    embed.add_field(name = '%warn(Kick members Permission Required)',value ='Use it like ``%warn @user <violation type>`` to warn any user',inline = False)    
    embed.add_field(name = '%norule(Kick members Permission Required) ',value ='Use it like ``%norole @user`` to warn anyone if he/she asks for promotion',inline = False)
    embed.add_field(name = '%getuser(Kick members Permission Required) ',value ='Use it like ``%getuser @rolename`` to get list of all users having a particular role',inline = False)
    await client.send_message(author,embed=embed)
    await client.say('📨 Check DMs For Information')

@client.command(pass_context = True)
async def funhelp(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name = '%poll ',value ='Use it like ``%poll "Question" "Option1" "Option2" ..... "Option9"``.',inline = False)
    embed.add_field(name = '%guess ',value ='To play guess game use ``d!guess <number> and number should be between 1-10``',inline = False)
    embed.add_field(name = '%github ',value ='Use it like- ``%github harman3955/vortex``',inline = False)
    embed.add_field(name = '%bottutorial ',value ='Use it like ``%bottutorial <tutorial name by darklegend>``',inline = False)
    embed.add_field(name = '%dyno ',value ='Use it like ``%dyno <dyno command name>``',inline = False)
    embed.add_field(name = '%donate ',value ='Use it to donate us and get a special post on Official DarkBot server.',inline = False)
    embed.add_field(name = '%ownerinfo ',value ='To get basic information about owner.',inline = False)
    embed.add_field(name = '%sourcecode ',value ='Use it to see darkbot sourcecode.',inline = False)
    embed.add_field(name = '%upvote ',value ='Use it to Upvote our bot and help us to grow',inline = False)
    embed.add_field(name = '%authlink ',value ='Use it to get authorizing link to authorize this bot to your server.',inline = False)
    embed.add_field(name = '%happybirthday @user ',value ='To wish someone happy birthday',inline = False)
    embed.add_field(name = '%technews ',value ='Use it to get tech news',inline = False)
    embed.add_field(name = '%googlefy ',value ='Use it like ``%googlefy <string>``.',inline = False)
    embed.add_field(name = '%spacenews ',value ='Use it to get space news',inline = False)
    embed.add_field(name = '%phynews ',value ='Use it to get physycs',inline = False)
    embed.add_field(name = '%verify ',value ='Use it to get verified role. Note- It needs proper setup.',inline = False)
    embed.add_field(name = '%flipcoin ',value ='Flipps coin',inline = False)
    embed.add_field(name = '%rolldice ',value ='Rolls dice',inline = False)
    embed.add_field(name = '%avatar @user ',value ='Shows avatar',inline = False)
		 	
    await client.send_message(author,embed=embed)
    await client.say('📨 Check DMs For Information')

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     
async def kick(ctx,user:discord.Member):

    if user.server_permissions.kick_members:
        await client.say('**He is mod/admin and i am unable to kick him/her**')
        return
    
    try:
        await client.kick(user)
        await client.say(user.name+' was kicked. Good bye '+user.name+'!')
        await client.delete_message(ctx.message)

    except discord.Forbidden:
        await client.say('Permission denied.')
        return

@client.command(pass_context = True)
@commands.has_permissions(manage_messages=True)  
async def clear(ctx, number):
 
    if ctx.message.author.server_permissions.manage_messages:
         mgs = [] #Empty list to put all the messages in the log
         number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number+1):
        mgs.append(x)            
       
    try:
        await client.delete_messages(mgs)          
        await client.say(str(number)+' messages deleted')
     
    except discord.Forbidden:
        await client.say(embed=Forbidden)
        return
    except discord.HTTPException:
        await client.say('clear failed.')
        return         
   
 
    await client.delete_messages(mgs)      



    	 		


@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)      
async def ban(ctx,user:discord.Member):

    if user.server_permissions.ban_members:
        await client.say('**He is mod/admin and i am unable to ban him/her**')
        return

    try:
        await client.ban(user)
        await client.say(user.name+' was banned. Good bye '+user.name+'!')

    except discord.Forbidden:

        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('ban failed.')
        return		 



@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     


async def unban(ctx):
    ban_list = await client.get_bans(ctx.message.server)

    # Show banned users
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    # Unban last banned user
    if not ban_list:
    	
        await client.say('Ban list is empty.')
        return
    try:
        await client.unban(ctx.message.server, ban_list[-1])
        await client.say('Unbanned user: `{}`'.format(ban_list[-1].name))
    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('unban failed.')
        return		      	 		 		  
  
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def say(ctx, *, msg = None):
    await client.delete_message(ctx.message)

    if not msg: await client.say("Please specify a message to send")
    else: await client.say(msg)
    return

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def rules(ctx, *, msg = None):
    await client.delete_message(ctx.message)
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Please specify a user to warn")
    else: await client.say(msg + ', Please Read Rules again and never break any one of them again otherwise i will mute/kick/ban you next time.')
    return

@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def bans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of The Banned Idiots", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     

async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def norule(ctx, *, msg = None):
    await client.delete_message(ctx.message)
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Please specify a user to warn")
    else: await client.say(msg + ', Please Do not ask for promotions check Rules again.')
    return

@client.command(pass_context = True)
async def happybirthday(ctx, *, msg = None):
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Please specify a user to wish")
    await client.say('Happy birthday ' + msg + ' \nhttps://asset.holidaycardsapp.com/assets/card/b_day399-22d0564f899cecd0375ba593a891e1b9.png')
    return


@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def english(ctx, *, msg = None):
    await client.delete_message(ctx.message)
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Please specify a user to warn")
    else: await client.say(msg + ', Please do not use language other than **English.**')
    return

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def hindi(ctx, *, msg = None):
    await client.delete_message(ctx.message)
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Please specify a user to warn")
    else: await client.say(msg + ' abe oo angrez ke bacche chup chap hindi me baat kar nahi to mai pagla jaunga')
    return


@client.command(pass_context = True) 
async def htmltutorial(ctx, *, msg = None):
    await client.delete_message(ctx.message)
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Please specify a user")
    else: await client.say('Welcome' + msg +  ', Please check http://uksoft.000webhostapp.com/Programming-Tutorials/index.html')
    return
   
@client.command(pass_context = True)
async def github(ctx, *, msg = None):
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Please specify respo. ``Format- https://github.com/uksoftworld/DarkBot``")
    else: await client.say('https://github.com/' + msg)
    return

@client.command(pass_context = True)
async def reactionroles(ctx, *, msg = None):
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Check this video to setup YAGPDB BOT- https://www.youtube.com/watch?v=icAqiw6txRQ")
    else: await client.say('Check this video to setup YAGPDB BOT- https://www.youtube.com/watch?v=icAqiw6txRQ ' + msg)
    return

@client.command(pass_context = True)
async def bottutorial(ctx, *, msg = None):
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Tutorial not found or maybe you have mistyped it")
    else: await client.say('https://github.com/uksoftworld/discord.py-tutorial/blob/master/' + msg + '.py')
    return

@client.command(pass_context = True)
async def dyno(ctx, *, msg = None):
    if '@here' in msg or '@everyone' in msg:
      return
    if not msg: await client.say("Command name not found or maybe you have mistyped it")
    else: await client.say('https://github.com/uksoftworld/dynoCC/blob/master/' + msg)
    return

@client.command(pass_context=True)
async def unverify(ctx):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Unverified')
    await client.add_roles(ctx.message.author, role)
    
@client.command(pass_context=True)
async def verify(ctx):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Verified')
    await client.add_roles(ctx.message.author, role)
    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def friend(ctx, user:discord.Member,):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='Friend of Owner')
    await client.add_roles(ctx.message.mentions[0], role)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)     
async def makemod(ctx, user: discord.Member):
    nickname = '♏' + user.name
    await client.change_nickname(user, nickname=nickname)
    role = discord.utils.get(ctx.message.server.roles, name='Moderator')
    await client.add_roles(user, role)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Congratulations Message')
    embed.add_field(name = '__Congratulations__',value ='**Congratulations for mod.Hope you will be more active here. Thanks for your help and support.**',inline = False)
    embed.set_image(url = 'https://preview.ibb.co/i1izTz/ezgif_5_e20b665628.gif')
    await client.send_message(user,embed=embed)
    await client.delete_message(ctx.message)
    
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)     
async def removemod(ctx, user: discord.Member):
    nickname = user.name
    await client.change_nickname(user, nickname=nickname)
    role = discord.utils.get(ctx.message.server.roles, name='Moderator')
    await client.remove_roles(user, role)
    await client.delete_message(ctx.message)

@client.command(pass_context = True)
async def botwarncode(ctx):
    await client.say('https://hastebin.com/ibogudoxot.py')
    return

@client.command(pass_context=True)
async def guess(ctx, number):
    try:
        arg = random.randint(1, 10)
    except ValueError:
        await client.say("Invalid number")
    else:
        await client.say('The correct answer is ' + str(arg))

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True) 
async def roles(context):
	"""Displays all of the roles with their ids"""
	roles = context.message.server.roles
	result = "The roles are "
	for role in roles:
		result += '``' + role.name + '``' + ": " + '``' + role.id + '``' + "\n "
	await client.say(result)
    
@client.command(pass_context=True, aliases=['server'])
@commands.has_permissions(kick_members=True)
async def membercount(ctx, *args):
    """
    Shows stats and information about current guild.
    ATTENTION: Please only use this on your own guilds or with explicit
    permissions of the guilds administrators!
    """
    if ctx.message.channel.is_private:
        await bot.delete_message(ctx.message)
        return

    g = ctx.message.server

    gid = g.id
    membs = str(len(g.members))
    membs_on = str(len([m for m in g.members if not m.status == Status.offline]))
    users = str(len([m for m in g.members if not m.bot]))
    users_on = str(len([m for m in g.members if not m.bot and not m.status == Status.offline]))
    bots = str(len([m for m in g.members if m.bot]))
    bots_on = str(len([m for m in g.members if m.bot and not m.status == Status.offline]))
    created = str(g.created_at)
    
    em = Embed(title="Membercount")
    em.description =    "```\n" \
                        "Members:   %s (%s)\n" \
                        "  Users:   %s (%s)\n" \
                        "  Bots:    %s (%s)\n" \
                        "Created:   %s\n" \
                        "```" % (membs, membs_on, users, users_on, bots, bots_on, created)

    await client.send_message(ctx.message.channel, embed=em)
    await client.delete_message(ctx.message)
	
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def embed(ctx, *args):
    """
    Sending embeded messages with color (and maby later title, footer and fields)
    """
    argstr = " ".join(args)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    text = argstr
    color = discord.Color((r << 16) + (g << 8) + b)
    await client.send_message(ctx.message.channel, embed=Embed(color = color, description=text))
    await client.delete_message(ctx.message)

client.run("NzEyMjI3NjYxMjMzMjU4NTc2.XsOvlA.U_Z2yCJ_Fvq1JRsPbUX-Wo3iSQg")
