import os, requests
import src.lib.colors as cl
from src.utils.basics import quest, terminal, setColor, coloredText

def main(userId):
    if not userId: 
        userId = quest("Discord User ID")
        while len(userId) < 18 or not userId.isdigit(): 
            terminal("e", "Invalid user ID.")
            userId = quest("Discord User ID", newline=True)
    api_key = os.getenv("DISCORD_API_KEY")
    if not api_key or len(api_key) < 7: return terminal("e", "Invalid Discord API Key.")
    try:
        response = requests.get(f"https://discord.com/api/v10/users/{userId}", 
        headers={ "Authorization": f"Bot {os.getenv("DISCORD_API_KEY")}"
        })
        if response.status_code == 200:
            data = response.json()
            print(f"""
        Discord User:
            {cl.b}> {cl.w} ID: {userId}
            {cl.b}> {cl.w} IP Address: {setColor("Coming Soon")}
            {cl.b}> {cl.w} Username: {data["username"]}
            {cl.b}> {cl.w} Avatar: {data["avatar"]}
            {cl.b}> {cl.w} Avatar Url: https://cdn.discordapp.com/avatars/{userId}/{data["avatar"]}.webp?size=2048
            {cl.b}> {cl.w} Discriminator: {data["discriminator"]}
            {cl.b}> {cl.w} Public flags: {data["public_flags"]}
            {cl.b}> {cl.w} Flags: {data["flags"]}
            {cl.b}> {cl.w} Banner: {data["banner"]}
            {cl.b}> {cl.w} Banner Url: {f"https://cdn.discordapp.com/banners/{userId}/{data["banner"]}" if data["banner"] else setColor("Does not exist") }
            {cl.b}> {cl.w} Accent color: {coloredText(f"#{str(data['accent_color'])}", f"#{str(data['accent_color'])}")}
            {cl.b}> {cl.w} Global name: {data["global_name"]}
            {cl.b}> {cl.w} Avatar decoration asset: {data["avatar_decoration_data"]["asset"] if data["avatar_decoration_data"] else setColor("Does not exist")}
            {cl.b}> {cl.w} Avatar decoration asset Url: {f"https://cdn.discordapp.com/avatar-decoration-presets/{data["avatar_decoration_data"]["asset"]}?size=512" if data["avatar_decoration_data"] else setColor("Does not exist")}
            {cl.b}> {cl.w} Avatar decoration Sku Id: {data["avatar_decoration_data"]["sku_id"] if data["avatar_decoration_data"] else setColor("Does not exist")}
            {cl.b}> {cl.w} Banner color: {coloredText(f"{data['banner_color']}", data["banner_color"])}
            {cl.b}> {cl.w} Clan: {data["clan"]}
""")
        else: terminal("e", f"Failed to retrieve data: {response}")
    except Exception as e: terminal("e", f"Failed to retrieve data: {e}")