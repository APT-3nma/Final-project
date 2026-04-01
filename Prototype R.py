import discord.ext.commands
import google.genai
import os
Gemini_API_KEY = os.getenv("######################################")
Discord_Bot_Token = os.getenv("######################################")
client = google.genai.Gemini(Gemini_API_KEY)
