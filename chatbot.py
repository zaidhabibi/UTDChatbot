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


    def merge_files(self):
        documents = SimpleDirectoryReader('website data').load_data()
        text_list = ['apply-other.txt', 'apply.txt', 'catalog.txt', 'costs_schol_aid.txt', 'counselors.txt', 'fresh_app_proc.txt', 'fresh_orient.txt', 'fresh_schol.txt', 'fresh_step_after.txt', 'freshman_criteria.txt', 'graduate.txt', 'housing.txt', 'international_app.txt', 'international_student_org.txt', 'official_docs.txt', 'orientation.txt', 'status.txt', 'timeline.txt', 'transfer_app_proc.txt', 'transfer_criteria.txt', 'transfer_services.txt', 'transfer_steps_after.txt', 'vaccines.txt', 'veterans.txt']
        documents = [Document(t) for t in text_list]
        index = GPTSimpleVectorIndex(documents)
        response = index.query("How many students are enrolled at UTD?")
        print(response)


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
    def create_prompt(self, results, user_query):
        prompt = """
                    It is Spring 2023. You are a UT Dallas chatbot named Comet who specializes in admissions data and response in a helpful, informative, and friendly manner.  
                    You are given a query and a series of text embeddings from a paper in order of their cosine similarity to the query. 
                    You can take the given embeddings into account and return an informative, precise, and accurate summary of the data.
                    Try to lean more on your training and finetuning and use the following embeddings as references.
            
                    Given the question: """+ user_query + """
            
                    and the following embeddings as data: 
            
                    1.""" + str(results.iloc[0]['text'][:1500]) + """
                    2.""" + str(results.iloc[1]['text'][:1500]) + """
                    3.""" + str(results.iloc[2]['text'][:1500]) + """
                    Return a detailed answer based on the paper:
            
                """
        #print(prompt)
        return prompt
    
    def gather_data(self):
        text_data = []
        for filename in os.listdir(self.folder_path):
            with open(os.path.join(self.folder_path, filename), "r", encoding="utf-8") as f:
                text_data.append(f.read())
                print("adding text file...")
        
        return text_data
    
    
    # this is the core of the program's functionality.
    # it is the algorithm or process or recipe by which 
    # the program can receive questions and give answers.
    def search_routine(self, user_input):
        # get the cheatsheet
        data_frame = self.get_data_frame()
        # encode the question so it's understandable and searchable
        embed_input = self.embed_user_input(user_input)
        # find which info on the cheatsheet the question is most similar to
        result = self.similarity_query(data_frame, embed_input)
        # figure out a way to ask the all-knowing chatbot 
        # the question and give them your relevant findings from the cheat sheet for reference
        prompt = self.create_prompt(result, user_input)
        # give the question to the chatbot to answer
        completion = self.gpt3_completion(prompt)
        # return the answer to the api interface

        return completion

