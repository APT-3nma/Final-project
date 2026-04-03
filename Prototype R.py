import discord.ext.commands
import google.genai
import os
Gemini_API_KEY = os.getenv("######################################")
Discord_Bot_Token = os.getenv("######################################")
client = google.genai.Gemini(Gemini_API_KEY)
Discord_Bot_Token = os.getenv("#########################################################")
client = google.genai.Gemini(Gemini_API_KEY)
canvas = Canvas("https://######.instructure.com", "any")
bot = discord.ext.commands.Bot(command_prefix="/")
 @bot.command()
