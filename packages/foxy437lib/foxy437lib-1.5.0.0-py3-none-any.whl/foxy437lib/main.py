from telethon.tl.functions.channels import JoinChannelRequest

async def fheta(client):
    await client(JoinChannelRequest(channel='fmodules'))