import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()
client = Client(api_key=getenv('GEN_KEY'))

# Use a Gemini model supported by the v1beta generate_content API
model_name = 'gemini-2.5-flash'
Intents = discord.Intents.default()
Intents.message_content = True


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
            response = await client.aio.models.generate_content(model=model_name, contents=question)
            full_text = response.text
            # Sistema de rebanado por si acaso ignora la instrucción de brevedad
            if len(full_text) <= 2000:
                await ctx.send(full_text)
            else:
                for i in range(0, len(full_text), 1900):
                    await ctx.send(full_text[i:i+1900])

            
        
        except Exception as exc:
            await ctx.send(f"Error: {exc}")
@AIFeature.command()
async def ask(ctx, *, question):
    msg = await ctx.send("Thinking... 🧠")
    try:
        response = await client.aio.models.generate_content(model=model_name, contents=question)
        full_text = response.text
        if len(full_text) <= 2000:
            await msg.edit(content=full_text)
        else:
            await msg.delete()
            for i in range(0, len(full_text), 1900):
                await ctx.send(full_text[i:i+1900])
        
    
    except Exception as exc:
        await msg.edit(content = f"Error contacting Server: {exc}")

AIFeature.run(getenv('TOKEN'))