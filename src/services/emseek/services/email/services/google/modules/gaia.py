from ..apis.peoplepa import PeoplePaHttp
from ..helpers import gmaps, auth
from ..helpers.knowledge import get_user_type_definition
from ..helpers.utils import get_httpx_client
import httpx
from typing import *
from pathlib import Path

async def hunt(as_client: httpx.AsyncClient, gaia_id: str, json_file: Path=None):
    if not as_client: as_client = get_httpx_client()
    ghunt_creds = await auth.load_and_auth(as_client)
    people_pa = PeoplePaHttp(ghunt_creds)
    # vision_api = VisionHttp(ghunt_creds)
    is_found, target = await people_pa.people(as_client, gaia_id, params_template="max_details")
    if not is_found: exit("[-] The target wasn't found.")
    if json_file: json_results = {}
    containers = target.sourceIds
    if len(containers) > 1 or not "PROFILE" in containers:
        print("[!] You have this person in these containers :")
        for container in containers:
            print(f"- {container.title()}")
    if not "PROFILE" in containers: exit("[-] Given information does not match a public Google Account.")
    container = "PROFILE"
    print("🙋 Google Account data\n")

    if container in target.profilePhotos:
        if target.profilePhotos[container].isDefault: print("[-] Default profile picture")
        else:
            print("[+] Custom profile picture !")
            print(f"=> {target.profilePhotos[container].url}")
            print()
    if container in target.coverPhotos:
        if target.coverPhotos[container].isDefault: print("[-] Default cover picture\n")
        else:
            print("[+] Custom cover picture !")
            print(f"=> {target.coverPhotos[container].url}")
            print()
    print(f"Last profile edit : {target.sourceIds[container].lastUpdated.strftime('%Y/%m/%d %H:%M:%S (UTC)')}\n")
    print(f"Gaia ID : {target.personId}\n")
    if container in target.profileInfos:
        print("User types :")
        for user_type in target.profileInfos[container].userTypes:
            definition = get_user_type_definition(user_type)
            print(f"- {user_type} ({definition})")
    print(f"\n📞 Google Chat Extended Data\n")
    #print(f"Presence : {target.extendedData.dynamiteData.presence}")
    print(f"Entity Type : {target.extendedData.dynamiteData.entityType}")
    #print(f"DND State : {target.extendedData.dynamiteData.dndState}")
    print(f"Customer ID : {x if (x := target.extendedData.dynamiteData.customerId) else 'Not found.'}")
    print(f"\n🌐 Google Plus Extended Data\n")
    print(f"Entreprise User : {target.extendedData.gplusData.isEntrepriseUser}")
    #print(f"Content Restriction : {target.extendedData.gplusData.contentRestriction}")
    if container in target.inAppReachability:
        print("\n[+] Activated Google services :")
        for app in target.inAppReachability[container].apps:
            print(f"- {app}")

    print("\n🗺️ Maps data")
    err, stats, reviews, photos = await gmaps.get_reviews(as_client, target.personId)
    gmaps.output(err, stats, reviews, photos, target.personId)
    if json_file:
        if container == "PROFILE":
            json_results[f"{container}_CONTAINER"] = {
                "profile": target,
                "maps": {
                    "photos": photos,
                    "reviews": reviews,
                    "stats": stats
                }
            }
        else:
            json_results[f"{container}_CONTAINER"] = {
                "profile": target
            }
    
    if json_file:
        import json
        from ..objects.encoders import GHuntEncoder;
        with open(json_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(json_results, cls=GHuntEncoder, indent=4))
        print(f"\n[+] JSON output wrote to {json_file} !")
    await as_client.aclose()