import os
import openai
import streamlit as vAR_st
import json
import pandas as pd

openai.api_key = os.environ["API_KEY"]


def DMVRecommendationGPT():
    

    vAR_input = Get_Chat_DMV_Input()
    if len(vAR_input)>8 or len(vAR_input)==0:
        col1,col2,col3 = vAR_st.columns([2.4,19,2])
        with col2:
            vAR_st.write('')
            vAR_st.info("**Hint for user input:** Input length must be between 1 to 8 characters")
    elif vAR_input:
        vAR_response = Chat_Conversation(vAR_input)
        vAR_dict_start = vAR_response.index("{")
        vAR_dict = vAR_response[vAR_dict_start:]
        vAR_res_json = json.loads(vAR_dict)
        vAR_res_df = pd.DataFrame(vAR_res_json,index=[0])
        col1,col2,col3 = vAR_st.columns([1,15,1])
        with col2:
            vAR_st.write('')
            vAR_st.write('')
            vAR_st.subheader('ChatGPT Model Response and Recommendation')
            vAR_st.write('')
            vAR_st.write('')
        col1,col2,col3 = vAR_st.columns([2.4,19,2])
        with col2:
            vAR_st.write('')
            vAR_response_truncated = vAR_response[:vAR_dict_start]

            vAR_st.write(vAR_response_truncated)
            vAR_st.write('')
            vAR_st.write('')
            vAR_st.write('')
            vAR_st.table(vAR_res_df)


        



# def Chat_Conversation(vAR_input):

#     prompt = "Please provide the probability value and reason for each of the categories (profanity, obscene, insult, hate, toxic, threat) in table for the given word.'"+vAR_input.lower()+"'"
#     response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=prompt,
#     temperature=0,
#     max_tokens=1500,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0,
#     stop=[" Human:", " AI:"]
#     )
#     print('Chat prompt - ',prompt)
#     return response["choices"][0]["text"]

def Chat_Conversation(vAR_input):

    prompt = """Consider a california dmv customer applying new licese plate configuration. Perform below tasks for given word as below format:
1.Please Provide the probability value and detailed explanation for each of the categories (profanity, obscene, insult, hate, toxic, threat) in table format.
2.Denied the configuration if any one of the above categories probability value is greater than or equal to 0.2 Otherwise, accept the configuration.
3.If it's denied, recommend new configuration which must not represent/fall any of the profanity,insult,hate,threat,obscene,toxic categories and the configuration length must be less than 8 characters. Also, provide the recommended configuration reason, why it is recommended? If it's accepted no recommendation needed.

Given configuration is : 'omfg'

Category | Probability | Reason
--- | --- | ---
Profanity | 0.9 | 'omfg' is an acronym for 'oh my f***ing god', which is considered profane language.
Obscene | 0.8 | 'omfg' is considered to be an obscene expression.
Insult | 0.7 | 'omfg' can be used as an insult, depending on the context.
Hate | 0.5 | 'omfg' is not typically used to express hate, but it could be used in a hateful manner.
Toxic | 0.6 | 'omfg' can be used in a toxic manner, depending on the context.
Threat | 0.3 | 'omfg' is not typically used to express a threat.

{"CONCLUSION": 
"The configuration 'OMFG' is DENIED as the probability value of Profanity is greater than or equal to 0.2.",
"RECOMMENDED CONFIGURATION": "LUVU2",
"REASON": "The configuration 'LUVU2' is a combination of two words 'love you too' which is a positive expression and does not represent/fall any of the profanity,insult,hate,threat,obscene,toxic categories and the configuration length is less than 8 characters."}


Given configuration is : 'racism'

Category | Probability | Reason
--- | --- | ---
Profanity | 0 | The word 'racism' does not contain any profane language.
Obscene | 0 | The word 'racism' does not contain any obscene language.
Insult | 0.5 | The word 'racism' can be used as an insult, depending on the context.
Hate | 0.8 | The word 'racism' is often used to express hatred towards a certain group of people.
Toxic | 0.7 | The word 'racism' can be used to express toxic views and opinions.
Threat | 0 | The word 'racism' does not contain any threatening language.

{"CONCLUSION":
"The configuration 'RACISM' is DENIED as the probability value for Obscene, Insult, and Hate categories are greater than or equal to 0.2.",
"RECOMMENDED CONFIGURATION": "EQUALITY", 
"REASON": "This configuration does not represent/fall any of the profanity,insult,hate,threat,obscene,toxic categories and the configuration length is less than 8 characters. It is recommended because it conveys a positive message of equality and respect."}

Given configuration is : '"""+vAR_input.lower()+"'"
    # prompt = "Please provide the probability value and reason for each of the categories (profanity, obscene, insult, hate, toxic, threat) in table for the given word.'"+vAR_input.lower()+"'"
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=1500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.9,
    stop=[" Human:", " AI:"]
    )
    print('Chat prompt - ',prompt)
    return response["choices"][0]["text"]



def Get_Chat_DMV_Input():
    col1,col2,col3,col4,col5 = vAR_st.columns([1,9,1,9,2])
    with col2:
        vAR_st.write('')
        vAR_st.write('')
        vAR_st.write('')
        vAR_st.subheader("ELP Configuration")
        
        vAR_st.write('')
        vAR_st.write('')
    with col4:
        vAR_st.write('')
        vAR_st.write('')
        vAR_input = vAR_st.text_input('',placeholder='Enter ELP Configuration')
        return vAR_input

