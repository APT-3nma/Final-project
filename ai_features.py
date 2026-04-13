import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()
api_key = getenv('GEN_KEY')
client = genai.Client(api_key=api_key)
model_name = 'gemini-1.5-flash'
Intents = discord.Intents.default()
Intents.message_content = True


AIFeature = commands.Bot(command_prefix="!", intents=Intents)

@AIFeature.command()
async def  test(ctx,*args):
    await ctx.send(" ".join(args))

@AIFeature.command(aliases=["tell"])
async def chat(ctx,*args):
    question = " ".join(args)
    try:
        response = client.models.generate_content(model=model_name, contents=question)
    except Exception as exc:
        await ctx.send(f"Error contacting Gemini: {exc}")
        return
    await ctx.send(response.text)

@AIFeature.command()
async def ask(ctx, *, question):
    try:
        response = client.models.generate_content(model=model_name, contents=question)
    except Exception as exc:
        await ctx.send(f"Error contacting Gemini: {exc}")
        return
    await ctx.send("Thinking...")
    await ctx.send(response.text)

AIFeature.run(getenv('TOKEN'))