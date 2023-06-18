# CalHacks
Inspiration
For foreigners visiting English-speaking countries, spoken English is by far the most common yet most challenging aspect of language learning. However, many non-native English speakers struggle to find real-life practice of spoken English due to factors including cost, location, and most importantly, a lack of fluent speakers to engage in conversations with. However, many popular language learning apps such as Duolingo lack this crucial feature. Having a real-time English teacher in a conversational format will help people learn and practice one of the most widely used languages in the world.

What it does
First, the user designs a role-play scenario, preferably where they and our AI are speaking directly to each other. Then, Chat-GPT outputs relevant information about the roleplay (ex: A customer (the user) ordered their meal from a waiter (our AI) at a local restaurant). The user then has a conversation with Chat-GPT in the given roleplay, receiving real-time feedback regarding grammatical correctness, emotion, and tonality. This helps the user quickly understand their strengths and weaknesses, making it easier for them to progress and feel comfortable with their English in any conceivable situation.

How we built it
We utilized React.js for our front-end and Django for the back-end. For detecting the emotions and tonality of the user's speech, we used Hume.AI's speech prosody model to rank the most likely emotions in the user's speech. Finally, we wrote our own guidelines of prompts for Chat-GPT to follow to allow the user to have both accurate and real-time vocal interaction with Chat-GPT.

Challenges we ran into
We had many surprising issues with picking up, downloading, and processing the audio we received from the users. We had issues with different GPT/conversation AI models running too slowly for real-time conversations.

Accomplishments that we're proud of
We managed to understand and incorporate the Hume API and prosody models successfully and managed to resolve the runtime of the audio-to-text aspect of our pipeline by utilizing AssemblyAI as opposed to OpenAI's Whisper model. In addition, we are proud to have resolved all of the major issues with the audio processing aspect of our pipeline.

What we learned
We had a great opportunity to create a clear problem statement and execute it to the best of our ability. We learned a lot about audio processing and how it is different from text, image, or video. We learned how to implement and test a wide variety of models from HuggingFace Transformers, OpenAI, and more.

What's next for EnglishAI
We would like to integrate a reward system via a mathematical model evaluating scores and a database with users. We'd also like to, on the flip side of what we currently provide, explore the ability to provide native English speakers a chance to perfect the spoken form of foreign languages.
