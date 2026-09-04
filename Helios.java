package com.helios;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.requests.GatewayIntent;

import dev.langchain4j.model.googleai.GoogleAiGeminiChatModel;
import io.github.cdimascio.dotenv.Dotenv;


public class Helios extends ListenerAdapter{

    // Initialize Environmental Variables.
    private static GoogleAiGeminiChatModel geminiModel;
    public static void main(String[] args) {
        Dotenv dotenv = Dotenv.load();
        String token = dotenv.get("Bot.Key");
        String geminiApiKey = dotenv.get("GenAi.Key");

        // Initialize Gemini Ai Model.

        geminiModel = GoogleAiGeminiChatModel.builder()
                .apiKey(geminiApiKey)
                .modelName("gemini-2.5-flash")
                .build();



        // Initialize JDA Bot.
        JDABuilder.createDefault(token, 
            GatewayIntent.GUILD_MESSAGES,
             GatewayIntent.MESSAGE_CONTENT)
                .addEventListeners(new Helios())
                .build();
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        if (event.getAuthor().isBot()) {
            return;
        }

            String messageText = event.getMessage().getContentRaw();

        

        // Process in a secondary thread to avoid blocking the thread in discord.

        new Thread(() -> {
            try{

                // Check if the user wants voce response in the voice chnner.
                if (messageText.startsWith("!voice")) {
                    String prompt = messageText.substring(7);
                    String aiResponse = geminiModel.generator(" Responding briefly:" + prompt);
                    
                    // Send the response in text.
                    event.getChannel().sendMessage(aiResponse).queue();

                    var guild = event.getGuild();
                    var member = event.getMember();

                    if (member != null && member.getVoiceState() != null && member.getVoiceState().inAudioChannel()) {
                        var audioChannel= member.getVoiceState().getChannel();
                        guild.getAudioManager().openAudioConnection(audioChannel);

                        // This lines make the integration with the audio stream send by Gemini.
                    } else {
                        event.getChannel().sendMessage("You need to access to the voice channel to use this feature.").queue();

                    }    


                } else {
                    // Normal text output.
                    String aiResponse = geminiModel.generate(messageText);
                    event.getChannel().sendMessage(aiResponse).queue();
                }
                

            

            } catch (Exception e) {
                event.getChannel().sendMessage("An error occured while processing the mesage.").queue();
                e.printStackTrace();

            }
        }).start();







            }
        }


    