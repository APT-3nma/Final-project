import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv()
client = Client(api_key=getenv('GEN_KEY'))
Intents = discord.Intents.default()
Intents.message_content = True
model_name = 'gemini-2.5-flash'




AIFeature = commands.Bot(command_prefix="!", intents=Intents)

@AIFeature.command()
async def  test(ctx,*args):
    await ctx.send(" ".join(args))

@AIFeature.command(aliases=["tell"])
async def chat(ctx,*args):
    question = " ".join(args)
    if not question:
        return
    async with ctx.typing():
        try:
            response = await client.aio.models.generate_content(model=model_name, contents=question, config=types.GenerateContentConfig(max_output_tokens=2000))
            full_text = response.text

            if len(full_text) <= 2000:
                await ctx.send(full_text)
            else:
                for i in range(0, len(full_text), 1900):
                    await ctx.send(full_text[i:i+1900])

            
        
        except Exception as exc:
            await ctx.send(f"Error: {exc}")

user_chats={}
@AIFeature.command()
async def ask(ctx, *, question):
    userID = ctx.author.id
    msg = await ctx.send("Thinking... 🧠")
    try:
       if userID not in user_chats:
        user_chats[userID] = client.aio.chats.create(model=model_name)
        chatSession = user_chats[userID]
        response = await chatSession.send_message(question, config=types.GenerateContentConfig(max_output_tokens=1000))
        full_text = response.text
        if len(full_text) <= 2000:
            await msg.edit(content=full_text)
        else:
            await msg.delete()
            for i in range(0, len(full_text), 1900):
                await ctx.send(full_text[i:i+1900])
        
    
    except Exception as exc:
        await msg.edit(content = f"Error contacting Server: {exc}")
#This line is extra is just to avoid using command prefix when messaging privately or DM.
@AIFeature.event
async def on_message(message):
    if message.author == AIFeature.user:
        return
    if not message.content.startswith("!"):
        if AIFeature.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            cleanContent = message.content.replace(f"<@{AIFeature.user.id}>", "").replace(f"<@!{AIFeature.user.id}>", "").strip()
            if cleanContent:
                ctx = await AIFeature.get_context(message)
                await ask(ctx, question=cleanContent)
    await AIFeature.process_commands(message)

    
    

AIFeature.run(getenv('TOKEN'))