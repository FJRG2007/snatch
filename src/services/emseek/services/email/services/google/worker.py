
import asyncio

def main(email):
    from .modules import login
    asyncio.run(login.check_and_login(None))
    from .modules import email
    asyncio.run(email.hunt(None, email))
    """
    from .modules import gaia
    asyncio.run(gaia.hunt(None, args.gaia_id, args.json))
    from .modules import drive
    asyncio.run(drive.hunt(None, args.file_id, args.json))
    from .modules import geolocate
    asyncio.run(geolocate.main(None, args.bssid, args.file, args.json))
    """