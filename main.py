import discord
from discord.ext import commands
import requests
from discord.ext.commands import cooldown, BucketType
import datetime
import random
import re
import json
with open("settings.json", "r") as config_file:
    config = json.load(config_file)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["command_prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print('Guilds:')
    total_members = 0
    for guild in bot.guilds:
        print(guild.name)
        total_members += len(guild.members)
    print(f'Total members: {total_members}')
    print(f'Total guilds: {len(bot.guilds)}')

def calculate_percentages(value, total):
    given_percentage = (value / total) * 100
    remaining_percentage = 100 - given_percentage
    
    return given_percentage, remaining_percentage
def uwu_converter(message):
    uwu_message = (
        re.sub(r'(r|l)', 'w', message, flags=re.IGNORECASE)
        .replace('n([aeiou])', 'ny$1')
        .replace('N([aeiou])', 'Ny$1')
        .replace('N', 'Ny')
        .replace('n', 'ny')
        .replace(r'([.!?])\s', r'\1~')
        .replace(r'([.!?])\n', r'\1~\n')
    )

    uwu_emojis = [":3", ";3", ":3", ";3", ":3", ";3", "OwO", "UwU", "OvO", "ÒwÓ", "0v0", "ÕwÕ", "0w0", "~v~", "~w~"]
    random_emoji = random.choice(uwu_emojis)

    uwu_message += f'~ {random_emoji}'
    return uwu_message
assettypes= {
    1: "Image",
    2: "T-Shirt",
    3: "Audio",
    4: "Mesh",
    5: "Script",
    8: "Hat",
    9: "Place",
    10: "Model",
    11: "Shirt",
    12: "Pants",
    13: "Decal",
    17: "Head",
    18: "Face",
    19: "Gear",
    21: "Badge",
    24: "Animation",
    27: "Torso",
    28: "Right Arm",
    29: "Left Arm",
    30: "Left Leg",
    31: "Right Leg",
    32: "Package",
    34: "Gamepass",
    38: "Plugin",
    40: "Meshpart",
    41: "Hair Accessory",
    42: "Face Accessory",
    43: "Neck Accessory",
    44: "Shoulder Accessory",
    45: "Front Accessory",
    46: "Back Accessory",
    47: "Waist Accessory",
    61: "Emote Animation",
    62: "Video",
}
@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def info(ctx, *, item_id1: str):
    print(f"{ctx.message.author} used the command: Info with {item_id1}")
    try:
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        else:
            item_id = item_id1
        if item_id:
            details_url = f"https://economy.roproxy.com/v2/assets/{item_id}/details"
            details_response = requests.get(details_url)

            if details_response.status_code == 200:
                details_data = details_response.json()
               
                name = details_data.get("Name")
                try:
                    creation = details_data.get("Created")
                    creationdatetime_object = datetime.datetime.strptime(creation, "%Y-%m-%dT%H:%M:%S.%fZ")
                    creationdiscord_timestampTR = f"<t:{int(creationdatetime_object.timestamp())}:R>"
                    creationdiscord_timestampT = f"<t:{int(creationdatetime_object.timestamp())}>"
                    update = details_data.get("Updated")
                    updatedatetime_object = datetime.datetime.strptime(update, "%Y-%m-%dT%H:%M:%S.%fZ") 
                    updatediscord_timestampTR = f"<t:{int(updatedatetime_object.timestamp())}:R>"
                    updatediscord_timestampT = f"<t:{int(updatedatetime_object.timestamp())}>"
                    workedtime = "true"
                except ValueError:
                    workedtime = "false"
                creator = details_data.get("Creator", {}).get("Name")
                price_in_robux = details_data.get("PriceInRobux")
                total_quantity = 0
                lowest_resale = 0
                if details_data.get("CollectiblesItemDetails") and details_data.get("CollectiblesItemDetails").get("TotalQuantity"):
                    total_quantity = details_data.get("CollectiblesItemDetails").get("TotalQuantity", 0)
                description = details_data.get("Description")
                remaining = details_data.get("Remaining", 0)
                remaining_url = f"https://catalog.roproxy.com/v1/catalog/items/{item_id}/details?itemType=Asset"
                remaining_response = requests.get(remaining_url)
                if remaining_response.status_code == 200:
                    remaining_data = remaining_response.json()
                    if remaining_data and remaining_data.get("lowestResalePrice") and remaining_data.get("lowestResalePrice") != 0:
                        lowest_resale = remaining_data.get("lowestResalePrice", 0)

                thumbnail_url = f"https://thumbnails.roproxy.com/v1/assets?assetIds={item_id}&returnPolicy=PlaceHolder&size=150x150&format=Png"
                thumbnail_response = requests.get(thumbnail_url)

                if thumbnail_response.status_code == 200:
                    thumbnail_data = thumbnail_response.json()
                    image_url = thumbnail_data["data"][0]["imageUrl"]
                    item_link = f"https://www.roblox.com/catalog/{item_id}/"
                    game_links = []
                    game_names = []
                    if details_data.get("SaleLocation", {}) and details_data.get("SaleLocation", {}).get("UniverseIds", []):
                        sale_location = details_data.get("SaleLocation", {})
                        universe_ids = sale_location.get("UniverseIds", [])
                        for game_id in universe_ids:
                            gameuniverse_url = f"https://games.roproxy.com/v1/games?universeIds={game_id}"
                            gameuniverse_response = requests.get(gameuniverse_url)
                            if gameuniverse_response.status_code == 200:
                                game_data = gameuniverse_response.json()
                                real_game_id = game_data['data'][0]['rootPlaceId']
                                real_game_name = game_data['data'][0]['name']
                                game_names.append(real_game_name)
                                game_idlink = f"https://www.roblox.com/games/{real_game_id}/Redblue"
                                game_links.append(game_idlink)
                if details_data.get("AssetTypeId") in assettypes:
                    embed = discord.Embed(
                        title=f"Roblox Item Information",
                        description=f"**Name:** {name}\n**Creator:** {creator}\n**Price in Robux:** {price_in_robux}\n**Accessory Type:** {str(assettypes[details_data.get('AssetTypeId')])}\n**Description:**\n ```{description}```"
                    )
                else:
                    embed = discord.Embed(
                        title=f"Roblox Item Information",
                        description=f"**Name:** {name}\n**Creator:** {creator}\n**Price in Robux:** {price_in_robux}\n**Description:** {description}"
                    )
                
                embed.set_thumbnail(url=image_url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                if workedtime == "true":
                    embed.add_field(name="Created in", value=f"{creationdiscord_timestampTR} | {creationdiscord_timestampT}", inline=False)
                    embed.add_field(name="Last Updated in", value=f"{updatediscord_timestampTR} | {updatediscord_timestampT}", inline=False)
                if total_quantity != 0 and total_quantity is not None:
                    given_percent, remaining_percent = calculate_percentages(remaining, total_quantity)
                    embed.add_field(
                        name="Stock Info",
                        value=f"> Remaining: {remaining}/{total_quantity}\n> Percentage Left: {given_percent:.1f}% | ({str(remaining)} left)\n> Percentage Sold: {remaining_percent:.1f}% | ({str(total_quantity-remaining)} sold)",
                        inline=False
                    )
                    if lowest_resale is not None and lowest_resale != 0:
                        embed.add_field(name="Lowest Resale Price", value=lowest_resale, inline=False)
                if details_data.get("CollectiblesItemDetails") and details_data.get("CollectiblesItemDetails").get("CollectibleQuantityLimitPerUser"):
                    embed.add_field(name="Quantity Limit Per User: ", value=str(details_data.get("CollectiblesItemDetails").get("CollectibleQuantityLimitPerUser")), inline=False)
                embed.add_field(name="Item Link", value=item_link, inline=False)
                if details_data.get("SaleLocation", {}) and details_data.get("SaleLocation", {}).get("UniverseIds", []):
                    if details_data.get("SaleLocation", {}).get("SaleLocationType") != 6:
                        embed.add_field(name="Website Item!!", value="[Wagoogus](https://www.roblox.com/games/975820487)  |-|  [Join](https://www.roblox.com/games/start?launchData=hichat&placeId=975820487)\n[Rolimons ](https://www.roblox.com/games/14056754882)  |-|  [Join](https://www.roblox.com/games/start?launchData=hichat&placeId=14056754882)", inline=False)
                    else:
                        for idx, game_name in enumerate(game_names, start=1):
                            embed.add_field(name=f"〘{idx}〙 {game_name}", value=game_links[idx-1], inline=False)
                await ctx.send(str(item_id),embed=embed, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
            else:
                await ctx.send("Failed to retrieve item details.", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
        if item_id1 is None: 
            await ctx.send("Please add an item link or item ID", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        print(e)
        await ctx.send("Error occurred or invalid item ID. ", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def stock(ctx, *, item_id1: str):
    print(f"{ctx.message.author} used the command: Stock with {item_id1}")
    try:
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        else:
            item_id = item_id1
        if item_id:
            details_url = f"https://economy.roproxy.com/v2/assets/{item_id}/details"
            details_response = requests.get(details_url)

            if details_response.status_code == 200:
                details_data = details_response.json()
                name = details_data.get("Name")
                creator = details_data.get("Creator", {}).get("Name")
                total_quantity = 0
                if details_data.get("CollectiblesItemDetails") and details_data.get("CollectiblesItemDetails").get("TotalQuantity"):
                    total_quantity = details_data.get("CollectiblesItemDetails").get("TotalQuantity", 0)
                remaining = details_data.get("Remaining", 0)
                embed = discord.Embed(
                    title=f"Roblox Stock Information",
                    description=f"**Name:** {name}\n**Creator:** {creator}"
                )
                
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                if total_quantity != 0 and total_quantity is not None:
                    given_percent, remaining_percent = calculate_percentages(remaining, total_quantity)
                    embed.add_field(
                        name="Stock Info",
                        value=f"> Remaining: {remaining}/{total_quantity}\n> Percentage Left: {given_percent:.1f}% | ({str(remaining)} left)\n> Percentage Sold: {remaining_percent:.1f}% | ({str(total_quantity-remaining)} sold)",
                        inline=False
                    )
                embed.add_field(name="Item Link", value=f"https://www.roblox.com/catalog/{item_id}/", inline=False)
                await ctx.send(str(item_id),embed=embed, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
            else:
                await ctx.send("Failed to retrieve item details.", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
        if item_id1 is None: 
            await ctx.send("Please add an item link or item ID", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        print(e)
        await ctx.send("Error occurred or invalid item ID.", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))


@stock.error
async def stock_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)

async def item2universe(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: item2universe with {item_id1}")
    try:
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        else:
            item_id = item_id1
        url = f"https://economy.roproxy.com/v2/assets/{item_id}/details"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sale_location = data.get("SaleLocation", {})
            universe_ids = sale_location.get("UniverseIds", [])

            if universe_ids:
                message = f"**```Universe ID(s):```**\n > " + '\n > '.join(str(id) for id in universe_ids) + "."

                await ctx.send(message)
            else:
                await ctx.send("No universe IDs found for this item.")
        else:
            await ctx.send("Failed to retrieve item details.")
        if item_id1 is None: 
            await ctx.send("Please add an item link or item ID")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while fetching the sale universes.")
@item2universe.error
async def item2universe_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def item2game(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: item2game with {item_id1}")
    try:
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        else:
            item_id = item_id1
        response = requests.get(f'https://economy.roproxy.com/v2/assets/{item_id}/details')
        if response.status_code == 200:
            data = response.json()
            sale_location = data.get('SaleLocation', {})
            universe_ids = sale_location.get('UniverseIds', [])
            if universe_ids:
                root_place_ids = []  
                root_place_names = []  
                for universe_id in universe_ids:
                    game_response = requests.get(f'https://games.roproxy.com/v1/games?universeIds={universe_id}')
        
                    if game_response.status_code == 200:
                        game_data = game_response.json()
                        root_place_id = game_data['data'][0]['rootPlaceId']
                        root_place_ids.append(root_place_id)
                        root_place_name = game_data['data'][0]['name'].replace('\n', ' ')
                        root_place_names.append(root_place_name)
                    else:
                        await ctx.send(f"Error: Unable to fetch data {universe_id}. Status code: {game_response.status_code}")
                modified_ids = ['\n\n> **``{}``**\n> [{}](<https://www.roblox.com/games/{}/Redblue>)'.format(gamena, id, id) for gamena, id in zip(root_place_names, root_place_ids)]
                message = f"**```Root Game(s):```**\n{', '.join(modified_ids)}"
                await ctx.send(message)
            else:
                await ctx.send(f"Error: Unable to fetch data. Status code: {response.status_code}")
        else:
            await ctx.send("No universe IDs found for this item.")
        if item_id1 is None: 
            await ctx.send("Please add an item link or item ID")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while fetching the sale universes.")
        
@item2game.error
async def item2game_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)
@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)

async def item2places(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: item2places with {item_id1}")
    try:
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        else:
            item_id = item_id1
        response = requests.get(f'https://economy.roproxy.com/v2/assets/{item_id}/details')

        if response.status_code == 200:
            data = response.json()
            sale_location = data.get('SaleLocation', {})
            universe_ids = sale_location.get('UniverseIds', [])
            if universe_ids:
                place_ids = []  
                place_names = []  

                for universe_id in universe_ids:
                    game_response = requests.get(f'https://develop.roproxy.com/v1/universes/{universe_id}/places?isUniverseCreation=false&limit=100&sortOrder=Asc')

                    if game_response.status_code == 200:
                        game_data = game_response.json()
                        place_ids.extend([place['id'] for place in game_data['data']])
                        place_names.extend([place['name'].replace('\n', ' ') for place in game_data['data']])

                    else:
                        await ctx.send(f"Error: Unable to fetch data {universe_id}. Status code: {game_response.status_code}")
        
                modified_ids = ['\n\n > **``{}``**\n> [{}](<https://www.roblox.com/games/{}/Redblue>)'.format(gamena, id, id) for gamena, id in zip(place_names, place_ids)] 
        
                message = f"**```Place(s):```** {', '.join(modified_ids)}"
                await ctx.send(message)
            else:
                await ctx.send("No universe IDs found for this item.")
        else:
            await ctx.send(f"Error: Unable to fetch data. Status code: {response.status_code}")
        if item_id1 is None: 
            await ctx.send("Please add an item link or item ID")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while fetching the sale universes.")


@item2places.error
async def item2places_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def game2places(ctx, game_id1: str):
    print(f"{ctx.message.author} used the command: game2places with {game_id1}")
    try:
        if "games/" in game_id1:
            game_id = game_id1.split("/games/")[1].split("/")[0]
        else:
            game_id = game_id1
        response = requests.get(f'https://apis.roproxy.com/universes/v1/places/{int(game_id)}/universe')

        if response.status_code == 200:
            data = response.json()
            universe_ids = data.get('universeId')
            if universe_ids:
                place_ids1 = []
                place_names1 = []

                for universe_id in [universe_ids]:
                    game_response = requests.get(f'https://develop.roproxy.com/v1/universes/{universe_id}/places?isUniverseCreation=false&limit=100&sortOrder=Asc')

                    if game_response.status_code == 200:
                        game_data = game_response.json()

                        if isinstance(game_data['data'], list):
                            place_ids1.extend([str(place['id']) for place in game_data['data']])
                            place_names1.extend([str(place['name'].replace('\n', ' ')) for place in game_data['data']])
                        else:
                            await ctx.send(f"Error: Unexpected data format for universe_id {universe_id}")
                    else:
                        await ctx.send(f"Error: Unable to fetch data {universe_id}. Status code: {game_response.status_code}")

                modified_ids = ['\n\n > **``{}``**\n> [{}](<https://www.roblox.com/games/{}/Redblue>)'.format(gamena1, id1, id1) for gamena1, id1 in zip(place_names1, place_ids1)]

                message = f"**```Place(s):```** {', '.join(modified_ids)}"
                await ctx.send(message)
            else:
                await ctx.send("No universe IDs found for this item.")
        else:
            await ctx.send(f"Error: Unable to fetch data. Status code: {response.status_code}")
        if game_id1 is None: 
            await ctx.send("Please add a game link or game ID")
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while fetching the sale universes.")

@game2places.error
async def game2places_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def waifu(ctx):
    print(f"{ctx.message.author} used the command: Waifu")
    try:
        response = requests.get(f'https://api.waifu.im/search?is_nsfw=false')
        if ctx.author.id != 662339610411532319 and  response.status_code == 200:
            waifu_json = response.json()
            waifu_image = waifu_json.get("images")[0]
            if waifu_image:
                waifu_url = waifu_image.get("url")
                embed = discord.Embed(title=f"meooow :3 waifu generated", description=f"nyaaaaaaaaaw", color=10181046)
                if waifu_image.get("source") is not None:
                    embed.add_field(name=f"Source:", value=str(waifu_image.get("source")), inline=False)
                if waifu_image.get("artist") is not None:
                    embed.add_field(name=f"Artist:", value=str(waifu_image.get('artist').get('name')), inline=False)
                    if waifu_image.get("artist").get("pixiv") is not None:
                        embed.add_field(name=f"Artist's Pixiv:", value=str(waifu_image.get('artist').get('pixiv')), inline=False)
                    if waifu_image.get("artist").get("twitter") is not None:
                        embed.add_field(name=f"Artist's Twitter:", value=str(waifu_image.get('artist').get('twitter')), inline=False)
                if waifu_url:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_image(url=str(waifu_url))
                    embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                    await ctx.send(embed=embed) 
                else:
                    await ctx.send("no waifus ;c")
            else:
                await ctx.send("no waifus ;c")
        else:
            await ctx.send("no waifus ;c")
    except Exception as e:
        print(e)
        await ctx.send("no waifus ;c")

@waifu.error
async def waifu_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down! (u weird asf tho)", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='redblue is disgusted, redblue better',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)
@bot.command()
@commands.cooldown(1, 18, commands.BucketType.user)
async def neko(ctx, content_type="safe"):
    print(f"{ctx.message.author} used the command: neko {content_type}" )
    try:
        if content_type == "safe":
            response = requests.get(f'https://api.nekosapi.com/v3/images/random?limit=1&rating={content_type}')
        elif content_type in ["explicit", "borderline", "suggestive"] and ctx.channel.is_nsfw(): 
            response = requests.get(f'https://api.nekosapi.com/v3/images/random?limit=1&rating={content_type}')
        if ctx.author.id != 662339610411532319 and content_type and response.status_code == 200:
            waifu_json = response.json()
            waifu_image = waifu_json.get("items")[0]
            if waifu_image:
                waifu_url = waifu_image.get("image_url")
                embed = discord.Embed(title=f"meooow :3 waifu generated", description=f"nyaaaaaaaaaw", color=10181046)
                if waifu_image.get("artist") is not None:
                    if waifu_image.get("artist").get("name") is not None:
                        embed.add_field(name=f"artist:", value=str(waifu_image.get("artist").get("name")), inline=False)
                    if waifu_image.get("artist").get("links") is not None:
                        embed.add_field(name=f"links:", value=str(waifu_image.get("artist").get("links")), inline=False)
                if waifu_url:
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_image(url=str(waifu_url))
                    embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                    await ctx.send(embed=embed) 
                else:
                    await ctx.send("no waifus ;c")
            else:
                await ctx.send("no waifus ;c")
        else:
            await ctx.send("no waifus ;c ")
    except Exception as e:
        print(e)
        await ctx.send("no waifus ;c (NSFW Channel or wrong age rating or error)")
@neko.error
async def neko_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down! (u weird asf tho)", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='redblue is disgusted, redblue better',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)
@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def ping(ctx):
    print(f"{ctx.message.author} used the command: Ping")
    await ctx.send(f'{round(bot.latency * 1000)} ms')


@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def support(ctx):
    print(f"{ctx.message.author} used the command: Support")
    await ctx.send(f' > [**Keep the Bot Running!**](<https://bot-hosting.net/?aff=1013590472255619103?)\n > [**My Discord**](<https://discord.gg/AynQT7rEy8>)\n > [**UGC Discord**](https://discord.gg/ugcleaks)\n > ****Cashapp - JustAPlayer****\n > [**Robux Donation**](<https://www.roblox.com/catalog/11733073941>)\n > [**Linkvertise**](https://direct-link.net/611550/donation)')

@support.error
async def support_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def convertvip(ctx, vip_link: str):
    print(f"{ctx.message.author} used the command: convertvip with {vip_link}")
    url = str(vip_link)
    response = requests.get(url)
    await ctx.send("(For Mobile Players)\n``Your Final Link for The vip is`` [**this**](" + str(response.url) + ")\n(<" + response.url + ">)", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    if vip_link is None: 
        await ctx.send("Please put a VIP Link with the new format.")
@convertvip.error
async def convertvip_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)
@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def redblue(ctx):
    print(f"{ctx.message.author} used the command: redblue")
    try:
        url = 'https://api.github.com/repos/JustAP1ayer/redblue/contents/'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            random_file = random.choice(data)
            embed = discord.Embed(title=f"meooow :3 redblue wife generated (Powered by Bing AI)", description=f"nyaaaaaaaaaw", color=10181046)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_image(url=str(random_file['download_url']))
            embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
            await ctx.send(embed=embed) 
        else:
            await ctx.send('Error: ' + str(response.status_code), allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        print(e)
        await ctx.send("no waifus ;c", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))

@redblue.error
async def redblue_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down! (i love redblue too <3)", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def uwuify(ctx,*, message : str):
    print(f"{ctx.message.author} used the command: uwuify")
    try:
        embed = discord.Embed(title=f"uwuified text made ^~^", description=f"```{uwu_converter(message)}```", color=7419530)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_thumbnail(url="https://staticdelivery.nexusmods.com/mods/2861/images/thumbnails/243/243-1691911373-110081999.png")

        await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        print(e)
        await ctx.send("smth went wrong", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
@uwuify.error
async def uwuify_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))


@bot.command()
@commands.cooldown(1, 14, commands.BucketType.user)
async def uploader(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: uploader with {item_id1}")
    try:

        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        else:
            item_id = item_id1

        url = "https://assetdelivery.roproxy.com/v1/asset/"
        params = {
            "id": item_id,
            "version": "0"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            pattern = r'rbxassetid://(\d+)'
            match = re.search(pattern, response.text)

            if match:
                asset_id = match.group(1)
                details_url = f"https://economy.roproxy.com/v2/assets/{str(asset_id)}/details"
                details_response = requests.get(details_url)
                details_data = details_response.json()
                creatorname = details_data.get("Creator", {}).get("Name")
                creatorid = details_data.get("Creator", {}).get("Id")
                em = discord.Embed(title=f"Asset Uploader Found!")
                em.add_field(name=f"Item Id: {item_id}", value=f"https://www.roblox.com/catalog/{item_id}/Redblue", inline=False)
                player_url = f"https://users.roproxy.com/v1/users/{str(creatorid)}"
                player_response = requests.get(player_url)
                thumbnail_url = f"https://thumbnails.roproxy.com/v1/users/avatar-headshot?userIds={str(creatorid)}&size=352x352&format=Png&isCircular=false"
                thumbnail_response = requests.get(thumbnail_url)
                em.add_field(name=f"Creator ID: {creatorid}", value=f"https://www.roblox.com/users/{str(creatorid)}/profile", inline=False)
                em.timestamp = datetime.datetime.utcnow()
                em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
                if thumbnail_response.status_code == 200:
                    thumbnail_data = thumbnail_response.json()
                    em.set_thumbnail(url=str(thumbnail_data["data"][0]["imageUrl"]))
                if player_response.status_code == 200:
                    player_response_data = player_response.json()
                    em.add_field(name=f"Creator Name: {creatorname}", value=f"Creator Display Name: **{player_response_data.get('displayName')}**", inline=False)
                await ctx.send(embed=em, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
            else:
                await ctx.send("Error Finding the Uploader!", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
        else:
            await ctx.send(f"Error: {response.status_code}", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
        if item_id1 is None: 
            await ctx.send("Please add an item link or an item id", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        print(e)
        await ctx.send("An error occurred (are you sure it was an accessory?)", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))


@uploader.error
async def uploader_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    try:
        if message.content == ":3" or message.content == ";3":
            random_number = random.random()
            if random_number < 0.07:
                response = requests.get('https://g.tenor.com/v1/search?q=Boykisser&key=LIVDSRZULELA')
                random_gif = random.choice(response.json()['results'])
                preview_url = random_gif['media'][0]['gif']['preview']
                embed = discord.Embed(title=f"meooow :3 boykisser easter egg found", description=f"nyaaaaaaaaaw", color=10181046)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url=str(preview_url))
                embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                await message.channel.send(embed=embed) 
        if message.content == "<@1013590472255619103>" or message.content == "<@1013590472255619103> ":
            random_number = random.random()
            if random_number < 0.25:
                await message.channel.send("https://cdn.discordapp.com/attachments/1028098087480205344/1178823457744621608/dGA7oggFcD6SzfKp.mp4?ex=65778be5&is=656516e5&hm=a9775d6add67709ac6085a61a3362e02db576c73eaad2397ea96793ce2b9e858&") 
    except Exception as e:
        print(e)
bot.run(config["token"])
