import openai, os

def getAIResponse(userInputBag):

    counter = userInputBag["counter"]
    userInput = userInputBag["userInput"]
    emotions = userInputBag["emotions"][:3]
    print("THis is the counter", counter)
    if counter == "1":
        #print("@" * 100)
        initial_prompt = f'''From now on, assume the following:
        I am a non-native English speaker trying to learn English. 
        You will be the English teacher guiding me and teaching me. 
        I want to learn English and apply it in real life and I want practical experience. 
        Now I will give you the following scenario:
        {userInput}
        Assign the role for me and the role for you for a roleplay scenario based on the given situation.
        For example, if I ask to simulate buying a toy in a toy shop, you will assign me the role of customer, and you as the shopkeeper.
        '''
    else:
        initial_prompt = f'''Now, as the role that you set for me, and based on your previous response as 
        the role you set for yourself, here is the response I am now giving: 
        <start of my response>
          {userInput}
        <end of my response>
        Also, here is a list some emotions that I express when I am giving this response: {emotions}


        ++++++++++

        Based on the response and emotions. Tell me two things:
        1. How accurate is the grammar of my response?
        2. Is the emotions I am using suitable for this scenario?

        Also, tell me how I can improve and how a native english speaker would speak in my role.

        ++++++++++

        Additionally, if it is appropriate to end the conversation based on the inputted scenario, give final feedback based on the prior criteria,
        grammatical accuracy and emotional expression.

        Otherwise, continue the conversion as the role you defined for yourself and 
        give an approporiate response back for the scenario I previously inputted.
        '''
    api_key = os.getenv("OPENAI_KEY", None)
    print("!"*100)
    if api_key is not None:
            openai.api_key = api_key
            res = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = initial_prompt,
                max_tokens = 256,
                temperature = 0.5
            )
            return res.choices[0]["text"]

