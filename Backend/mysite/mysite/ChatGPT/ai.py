import openai, os
import json

def getAIResponse(userInputBag):

    counter = userInputBag["counter"]
    userInput = userInputBag["userInput"]
    emotions = userInputBag["emotions"][:3]
    history = userInputBag["history"]
    print("this is the history", history)
    print("THis is the counter", counter)
    for x in counter:
        print(json.loads(x))
    finalMessages = []

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

        prompt = {"role": "system", "content": initial_prompt}
        finalMessages.append(prompt)
    else:
        

        for index, elemenet in enumerate(history):
            print(elemenet)
            if index == 1:
                temp = f'''From now on, assume the following:
                    I am a non-native English speaker trying to learn English. 
                    You will be the English teacher guiding me and teaching me. 
                    I want to learn English and apply it in real life and I want practical experience. 
                    Now I will give you the following scenario:
                    {elemenet["content"]}
                    Assign the role for me and the role for you for a roleplay scenario based on the given situation.
                    For example, if I ask to simulate buying a toy in a toy shop, you will assign me the role of customer, and you as the shopkeeper.
                    '''
                firstOne = {"role": "system", "content": temp}
                finalMessages.append(firstOne)
            else:
                finalMessages.append({"role": elemenet["role"], "content": elemenet["content"]})
        
        currentInput = f'''Now, as the role that you set for me, and based on your previous response as 
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

                        Format your response like this:
                        1. whatever feedback, wrap it in a @ symbol
                        2. whatever response to continue the original conversation wrap it in a % symbol
                        '''

        finalMessages.append({"role": "user", "content": currentInput})
    api_key = os.getenv("OPENAI_KEY", None)
    print("!"*100)

    if api_key is not None:
            openai.api_key = api_key
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=finalMessages
            )
            return res.choices[0].message.content.strip()
