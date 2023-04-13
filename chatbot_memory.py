"""
Author: CS 4485 Team
Description: This class uses embeddings from scraped web data related to UT Dallas admissions
so that the chatbot can use the information as reference when answering user queries.
"""
import pandas as pd
import openai
import os
import pickle
from openai.embeddings_utils import get_embedding, cosine_similarity
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader
import shutil
import json
import numpy as np
from numpy.linalg import norm
from time import time, sleep
from uuid import uuid4
import datetime
import pinecone

class Chatbot:

    def __init__(self, data_file_name, embedding_model):
        self.folder_path = "website data"
        # load the passkey file from .env file
        load_dotenv(dotenv_path='key.env')
        # store the passkey as this variable
        self.open_ai_key = os.getenv("OPENAI_PASSKEY")

        self.file_name = data_file_name
        self.embedding_model = embedding_model

        # authentication with OpenAI API
        openai.api_key = self.open_ai_key

        pinecone.init(api_key=self.open_file('pinecone.txt'), environment="us-east1-gcp")
        self.vdb = pinecone.Index(index_name="raven-mvp")

        # Clear conversation history in the "nexus" folder
        self.clear_conversation_history()

        # Clear existing vectors from Pinecone
        self.clear_existing_vectors()

    def save_file(self, filepath, content):
        with open(filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
            
 
    def load_conversation(self, results):
        result = list()
        for m in results['matches']:
            info = self.load_json('nexus/%s.json' % m['id'])
            result.append(info)
        
        ordered = sorted(result, key=lambda d: d.get('time', 0), reverse=False)

        messages = [i['message'] for i in ordered if 'message' in i]

        message_block = '\n'.join(messages).strip()
        return message_block

    def gpt3_embedding(self, content, engine='text-embedding-ada-002'):
        content = content.encode(encoding='ASCII', errors='ignore').decode()    # this fixes any UNICODE errors
        response = openai.Embedding.create(input=content, engine=engine)
        vector = response['data'][0]['embedding']
        return vector 

    def save_json(self, filepath, payload):
        with open(filepath, 'w', encoding='utf-8') as outfile:
            json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)

    def load_json(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as infile:
                return json.load(infile)
        except FileNotFoundError:
            print(f"File {filepath} not found. Returning an empty dictionary.")
            return {}

    def timestamp_to_datetime(self, unix_time):
        return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B, %d, %Y at %I:%M%p %Z")

    # a function to open a file, any file. 
    # just give it a file path
    def open_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
        
    # we're using text-davinci-003 which is more expensive and not as goot as gpt-3.5-turbo
    # but it's able to be finetuned for our purposes 
    # the function takes a JSON format message from the API
    # and it extracts the text and returns it!
    def gpt3_completion(self, prompt, engine='text-davinci-003', temp = 0.7, top_p = 1.0, tokens = 900, freq_pen = 0.0, pres_pen = 0.0, stop = ['<<END>>']):
        prompt = prompt.encode(encoding='ASCII', errors = 'ignore').decode()
        response = openai.Completion.create(
            engine = engine,
            prompt = prompt,
            temperature = temp,
            max_tokens = tokens,
            top_p = top_p,
            frequency_penalty = freq_pen,
            presence_penalty = pres_pen,
            stop = stop)
        text = response['choices'][0]['text'].strip()
        return text
    
    # what is a data frame?
    # it's a long table with columns that represent a topic, the text, embedding of the text
    # if we have already have a data frame, let's use the one we have.
    # if we don't, let's create one!
    # we return a data frame that our chatbot can use like a cheatsheet.
    def get_data_frame(self):
        if self.is_data_frame(self.file_name):
            df = self.open_data_frame(self.file_name)
        else:
            df = self.create_data_frame()
        
        return df
    
    # let's check if a dataframe of some name actually exists
    def is_data_frame(self, file_name):
        is_data_frame = False
        if os.path.isfile(file_name):
            is_data_frame = True
        return is_data_frame
    
    # let's a open a data frame of a certain file name.
    def open_data_frame(self, file_name):
        df = pd.read_pickle(file_name)
        return df 
    
    # the hard-lifting of building a dataframe.
    def create_data_frame(self):
        # let's collect all our 'notes' in one place
        text_data_df = self.gather_data()
        # this is the paper where we condense all our notes in short-hand.
        embeddings = []
        
        # we load our cheat sheet with the text
        df = pd.DataFrame({"text": text_data_df})
        # we take our cheatsheet and add condensed information to help use find it when we need it
        embeddings = df.text.apply([lambda x: get_embedding(x, engine=self.embedding_model)])
        # we store these 'markers' in a separate column so they're easy to find later.
        df["embeddings"] = embeddings
        # we save our cheat sheet.
        self.save_data_frame(df, self.file_name)
        
        return df

    def save_data_frame(self, df, file_name):
        df.to_pickle(file_name)


    


    # Create an embedding of the user input to compare with the embeddings in our data frame
    def embed_user_input(self, query):
        # what does this question/input look like that I may have in my notes
        query_embed = get_embedding(query, engine=self.embedding_model)
        return query_embed
    
    # this function is like searching through a cheatsheet for the information 
    # that is most relevant to the question at hand
    def similarity_query(self, df, query_embed):
        df["similarity"] = df.embeddings.apply(lambda x: cosine_similarity(x, query_embed))
        result = df.sort_values("similarity", ascending=False, ignore_index=True)
        return result
    
    # this creates a prompt we'll give to our chatbot to help it answer the question
    # it contains the user query along with some references
    def create_prompt(self, results, user_query, conversation_history):
        prompt = f"""
        It is Spring 2023. You are a UT Dallas chatbot named Comet who specializes in admissions data and response in a helpful, informative, and friendly manner.
        You are given a query, a series of text embeddings from a paper in order of their cosine similarity to the query, and a conversational history.
        You can take the given embeddings into account and return an informative, precise, and accurate summary of the data, but only in so far as it is relevant to the question.
        You should take the conversational history into account but only in so far as it is relevant to the question.
        Do not make mention of your inner workings, such as the conversation history or embeddings in your response.
        Do not include information about the embeddings if it is not relevant to the user's input/question.

        Given the question: {user_query}

        The previous conversation history is as follows:
        {conversation_history}

        and the following embeddings as data:

        1.{results.iloc[0]['text'][:1500]}
        2.{results.iloc[1]['text'][:1500]}
        3.{results.iloc[2]['text'][:1500]}

        Return an answer based on the conversation history and the embeddings. 
        Make sure the response is natural and not overly based on the data you are given if it isn't relevant.
        """
        return prompt
    
    def gather_data(self):
        text_data = []
        for filename in os.listdir(self.folder_path):
            with open(os.path.join(self.folder_path, filename), "r", encoding="utf-8") as f:
                text_data.append(f.read())
                print("adding text file...")
        
        return text_data
    
    def save_conversation(self, message_id, message_text):
       
        message = {'id': message_id, 'time': time(), 'message': message_text}
        self.save_json('nexus/%s.json' % message_id, message)
        vector = self.gpt3_embedding(message_text)
        payload = list()
        payload.append((message_id, vector))
        self.vdb.upsert(payload)

    def search_routine(self, user_input):
        # Get the cheatsheet
        data_frame = self.get_data_frame()
        
        # Encode the question so it's understandable and searchable
        embed_input = self.embed_user_input(user_input)
        
        # Find which info on the cheatsheet the question is most similar to
        result = self.similarity_query(data_frame, embed_input)
        
        # Retrieve conversation history
        conversation = self.retrieve_conversation_history(user_input)
        
        # Create the prompt for GPT-3
        prompt = self.create_prompt(result, user_input, conversation)
        
        # Get the response from GPT-3
        response_text = self.gpt3_completion(prompt)
        
        # Save the conversation history and chatbot response
        self.update_conversation_history(user_input, response_text)

        # Return the answer to the API interface
        return response_text

    def retrieve_conversation_history(self, user_input):
        convo_length = 3
        vector = self.gpt3_embedding(user_input)
        results_convo = self.vdb.query(vector=vector, top_k=convo_length, include_values=True, include_metadata=True)

        # Check if there is any conversation history
        if results_convo['matches']:
            conversation = self.load_conversation(results_convo)
        else:
            conversation = ""

        return conversation

    def update_conversation_history(self, user_input, response_text):
        # Save the conversation history
        conversation_id = str(uuid4())
        self.save_conversation(conversation_id, user_input)

        # Save the chatbot response
        response_id = str(uuid4())
        self.save_conversation(response_id, response_text)

    def clear_conversation_history(self):
        nexus_dir = "nexus"
        for filename in os.listdir(nexus_dir):
            file_path = os.path.join(nexus_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def clear_existing_vectors(self):
        try:
            vector_ids = self.vdb.fetch_ids()
            self.vdb.delete(vector_ids)
        except Exception as e:
            print(f"Failed to delete existing vectors. Reason: {e}")