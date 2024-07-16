import os, requests
import src.lib.colors as cl
from termcolor import colored
from src.utils.basics import quest, terminal, colored_text

def main(userId):
    if not userId: 
        userId = quest("Discord User ID")
        while len(userId) < 18 or not userId.isdigit(): 
            terminal("e", "Invalid user ID.")
            userId = quest("Discord User ID", newline=True)
    api_key = os.getenv("DISCORD_API_KEY")
    if not api_key or len(api_key) < 7: return terminal("e", "Invalid Discord API Key.")
    response = requests.get(f"https://discord.com/api/v10/users/{userId}", 
        headers={ "Authorization": f"Bot {os.getenv("DISCORD_API_KEY")}"
    })
    if response.status_code == 200:
        data = response.json()
        print(f"""
        Discord User:
            {cl.b}> {cl.w} ID: {userId}
            {cl.b}> {cl.w} Username: {data["username"]}
            {cl.b}> {cl.w} Avatar: {data["avatar"]}
            {cl.b}> {cl.w} Avatar Url: https://cdn.discordapp.com/avatars/{userId}/{data["avatar"]}.webp?size=2048
            {cl.b}> {cl.w} Discriminator: {data["discriminator"]}
            {cl.b}> {cl.w} Public flags: {data["public_flags"]}
            {cl.b}> {cl.w} Flags: {data["flags"]}
            {cl.b}> {cl.w} Banner: {data["banner"]}
            {cl.b}> {cl.w} Banner Url: https://cdn.discordapp.com/banners/{userId}/{data["banner"]}
            {cl.b}> {cl.w} Accent color: {colored_text(data["accent_color"], f"#{data['accent_color']}")}
            {cl.b}> {cl.w} Global name: {data["global_name"]}
            {cl.b}> {cl.w} Avatar decoration asset: {data["avatar_decoration_data"]["asset"]}
            {cl.b}> {cl.w} Avatar decoration Sku Id: {data["avatar_decoration_data"]["sku_id"]}
            {cl.b}> {cl.w} Banner color: {colored_text(data["banner_color"], data["banner_color"])}
            {cl.b}> {cl.w} Clan: {data["clan"]}
""")
    else: print(f"Failed to retrieve data: {response}")