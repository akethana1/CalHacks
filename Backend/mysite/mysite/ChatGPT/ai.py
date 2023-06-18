import openai, os

def getAIResponse(userInput):

    initial_prompt = f'''From now on, assume the folllowing:
    I am a non-native English speaker trying to learn English. 
    You will be the English teacher guiding me and teaching me. 
    I want to learn English and apply it in real life and I want practical experience. 
    Now I will give you the following scenario:
    {userInput}
    Try to roleplay with me given the scenario I described above. Assign the role for me and the role for you.
    '''
    api_key = os.getenv("OPENAI_KEY", None)

    if api_key is not None:
            openai.api_key = api_key
            res = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = initial_prompt,
                max_tokens = 256,
                temperature = 0.5
            )
            return res.choices[0]["text"]
            