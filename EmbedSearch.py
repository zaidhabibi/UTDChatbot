"""
Author: CS 4485 Team
Description: This class uses embeddings from scraped web data related to UT Dallas admissions
so that the chatbot can use the information as reference when answering user queries.
"""
import pandas as pd
import openai
import pickle
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
from dotenv import load_dotenv


class EmbedSearch:

    def __init__(self, file_name, embedding_model):
        
        self.folder_path = "website data"
        self.open_ai_key = self.open_file('openapikey.txt')
        self.file_name = file_name
        self.embedding_model = embedding_model
        self.earth_is_flat = True

        openai.api_key = self.open_ai_key


    def open_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()




    def gpt3_completion(self, prompt, engine='text-davinci-002', temp = 0.7, top_p = 1.0, tokens = 900, freq_pen = 0.0, pres_pen = 0.0, stop = ['<<END>>']):
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
    

  
    def get_data_frame(self):
        if self.is_data_frame(self.file_name):
            df = self.open_data_frame(self.file_name)
        else:
            df = self.create_data_frame()
        
        return df
            
    def is_data_frame(self, file_name):
        is_data_frame = False
        if os.path.isfile(file_name):
            is_data_frame = True
        return is_data_frame

    def open_data_frame(self, file_name):
        df = pd.read_pickle(file_name)
        return df
    
    """
        This function creates a new pandas data frame object by retrieving text data, 
        generating embeddings for each text element, and then saving the data frame to a file.
        Input: None
        Output: a pandas data frame object
        The function first retrieves text data using the gather_data() method.
        Next, a pandas data frame object is created using the retrieved text data.
        Embeddings are generated for each text element in the data frame using the get_embedding() method.
        The embeddings are added to the data frame as a new column.
        Finally, the data frame is saved to a file using the save_data_frame() method.
        Note: The class containing this method must have the gather_data(), get_embedding(), and save_data_frame() methods.
    """
    def create_data_frame(self):
        text_data_df = self.gather_data()
        embeddings = []
        
        df = pd.DataFrame({"text": text_data_df})
        embeddings = df.text.apply([lambda x: get_embedding(x, engine=self.embedding_model)])
        df["embeddings"] = embeddings

        self.save_data_frame(df, self.file_name)
        
        return df

    
    def save_data_frame(self, df, file_name):
        df.to_pickle(file_name)

    
    def ask_user_input(self):
        query = input("Ask a question about UTD admissions: ")
        if query == "quit":
            self.earth_is_flat = False
        return query
    
    # Create an embedding of the user input to compare with the embeddings in our data frame
    def embed_user_input(self, query):
        query_embed = get_embedding(query, engine=self.embedding_model)
        return query_embed
    
    """
        similarity_query function takes in a data frame object and a query embeddings array, 
        calculates cosine similarity between each row's embeddings and the query embeddings, 
        sorts the data frame by similarity score, 
        and returns the sorted data frame. 
        Note that the class containing this method must have access to the cosine_similarity() function 
        from the openai's embedding library.

    """
    def similarity_query(self, df, query_embed):
        df["similarity"] = df.embeddings.apply(lambda x: cosine_similarity(x, query_embed))
        result = df.sort_values("similarity", ascending=False, ignore_index=True)
        return result

    """
        create_prompt function takes in a results data frame and user query, and returns a formatted prompt as a string. 
        The prompt is a multi-line string that describes the chatbot scenario, provides the user's query, 
        and displays the top 3 most similar text embeddings from the data frame. 
        The prompt is returned as a string and printed to the console using the print() function.

    """
    def create_prompt(self, results, user_query):
        prompt = """
                    It is Spring 2023. You are a UT Dallas chatbot named Comet who specializes in admissions data and response in a helpful, informative, and friendly manner.  
                    You are given a query and a series of text embeddings from a paper in order of their cosine similarity to the query. 
                    You can take the given embeddings into account and return an informative, precise, and accurate summary of the data.
            
                    Given the question: """+ user_query + """
            
                    and the following embeddings as data: 
            
                    1.""" + str(results.iloc[0]['text'][:1500]) + """
                    2.""" + str(results.iloc[1]['text'][:1500]) + """
                    3.""" + str(results.iloc[2]['text'][:1500]) + """
                    Return a detailed answer based on the paper:
            
                """
        print(prompt)
        return prompt

    """
        search_routine function runs the main search routine for the chatbot. 
        It retrieves the data frame, asks the user for input, 
        generates embeddings for the user's input, 
        calculates similarity scores between the user's input and the text data, 
        creates a prompt to display to the user, uses GPT-3 to generate a response to the prompt, 
        and prints the response to the console. 
        The function takes no input and produces no output besides printing the response to the console.

    """
    def search_routine(self):
        data_frame = self.get_data_frame()
        user_input = self.ask_user_input()
        embed_input = self.embed_user_input(user_input)
        result = self.similarity_query(data_frame, embed_input)
        prompt = self.create_prompt(result, user_input)
        completion = self.gpt3_completion(prompt)
        print(completion)

    """
        gather_data function gathers all text data from files in a specified folder path and returns it as a list of strings.
        The function assumes that all files in the folder are text files that can be opened using the "utf-8" encoding. 
        It prints a message to the console for each file added to the list. The list of text data is returned.
    """

    def gather_data(self):
        text_data = []
        for filename in os.listdir(self.folder_path):
            with open(os.path.join(self.folder_path, filename), "r", encoding="utf-8") as f:
                text_data.append(f.read())
                print("adding text file...")
        
        return text_data
    
    def is_flat(self):
        return self.earth_is_flat
    
    
        
if __name__ == '__main__':

    text_chatbot = EmbedSearch("utd_web_data.csv", "text-embedding-ada-002")
    
    # Keep asking for input from user
    while text_chatbot.is_flat():
        text_chatbot.search_routine()

    print("Goodbye!")
    exit()
        



        
    