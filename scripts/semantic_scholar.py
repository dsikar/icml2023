import requests
import os
import pickle
import time

# Semantic Scholar API documentation: https://api.semanticscholar.org/graph/v1
# https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers

class SemanticScholar:
    def __init__(self, debug=False):
        self.debug = debug
        # master_list: A list of dictionaries where each dictionary represents a paper's details.
        # Structure:
        # [
        #     {
        #         "title": "Paper Title",
        #         "paperID": "unique_paper_id",
        #         "arxivId": "arxiv_id",
        #         "publication_year": "year_of_publication",
        #         "abstract": "Abstract of the paper"
        #     },
        #     ... (more papers)
        # ]
        self.master_list = []

        # papers_list: A list of dictionaries where each dictionary represents a paper and its references.
        # Structure:
        # [
        #     {
        #         "paperID": "unique_paper_id",
        #         "references": ["ref_paper1_id", "ref_paper2_id", ...]
        #     },
        #     ... (more papers with their references)
        # ]
        self.papers_list = []


    def get_paper_id_by_title(self, title):
        # Define the search endpoint with the given title
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}"
        
        # Send the request
        response = requests.get(url)
        data = response.json()
        
        # Extract the paperId from the first result (if available)
        if 'data' in data and data['data']:
            paper_id = data['data'][0]['paperId']
            return paper_id
        else:
            if self.debug: 
                print("No papers found with the given title.")
            return None


    def fetch_and_store_references(self, paper_id):
        # Define the paper details endpoint
        url = f"https://api.semanticscholar.org/v1/paper/{paper_id}"
        
        # Send the request
        response = requests.get(url)
        data = response.json()
        references = data.get('references', [])

        # List to hold the paperIds of the references
        reference_ids = []  

        # Iterate through the references and add them to the master_list
        for ref in references:
            paperId = ref.get('paperId')
            title = ref.get('title')
            abstract = ref.get('abstract')
            year = ref.get('year')
            arxivId = ref.get('arxivId', None)  # arxivId may not be present for all references

            # Add the reference details to the master_list
            self.add_to_master_list(title, paperId, arxivId, year, abstract)

            # Append the paperId to the reference_ids list
            reference_ids.append(paperId)

        # Return the list of paperIds of the references
        return reference_ids

    def get_paper_details(self, paperID):
        """Retrieve details of a paper including BibTeX, ArXiv ID, and publication year."""
        import os
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path to the API key file
        # api_key_file = os.path.join(script_dir, 'ss_api_key.txt')

        # Read the API key from the file
        # with open(api_key_file, 'r') as file:
            # api_key = file.read().strip()

        # Set the headers with the API key
        # headers = {
        #     'x-api-key': api_key
        # }

        # s = requests.Session()
        # s.timeout = 15
        # Make a POST request to retrieve paper details
        # r = requests.post(
        #     'https://api.semanticscholar.org/graph/v1/paper/batch',
        #     params="{'fields': 'referenceCount,citationCount,title,citationStyles,openAccessPdf,externalIds,publicationDate,abstract'}",
        #     json={"ids": [paperID]}
        # )
        # r = requests.post(
        #     f'https://api.semanticscholar.org/graph/v1/paper/paper/{paperID}?fields=referenceCount,citationCount,title,citationStyles,openAccessPdf,externalIds,publicationDate,abstract'
        # )        

        #output = r.json()

        url = f'https://api.semanticscholar.org/graph/v1/paper/{paperID}?fields=referenceCount,citationCount,title,citationStyles,openAccessPdf,externalIds,publicationDate,abstract'
        response = requests.get(url)

        # initialise return variables
        output = None
        arxiv_id = None
        publication_year = None
        abstract = None
        bibtex = None

        if response.status_code == 200:
            output = response.json()
        else:
            print("Error: Failed to retrieve data from the API.")        

        # Extract the desired fields
        if 'citationStyles' in output and 'bibtex' in output['citationStyles']:
            bibtex = output['citationStyles']['bibtex']
        if 'externalIds' in output and 'ArXiv' in output['externalIds']:
            arxiv_id = output['externalIds']['ArXiv']
        if 'publicationDate' in output and output['publicationDate'] is not None:
            publication_year = output['publicationDate'].split('-')[0]  # Extract the year from the date
        if 'abstract' in output:
            abstract = output['abstract']
            
        return bibtex, arxiv_id, publication_year, abstract


    def add_to_master_list(self, title, paperID, arxivId, publication_year, abstract):
        """Add a paper's details to the master list if it doesn't already exist."""
        # Check if the entry with the given paperID already exists
        if not any(paper['paperID'] == paperID for paper in self.master_list):
            self.master_list.append({
                "title": title,
                "paperID": paperID,
                "arxivId": arxivId,
                "publication_year": publication_year,
                "abstract": abstract
            })
            if self.debug:            
                print(f"Entry for paperID '{paperID}' added to master list.")
        else:
            if self.debug:
                print(f"Entry for paperID '{paperID}' already exists in master list.")


    def add_to_papers_list(self, paperID, abstract, bibtex, references):
        """Add a paper and its references to the papers_list."""
        # Check if the entry with the given paperID already exists in papers_list
        if not any(paper['paperID'] == paperID for paper in self.papers_list):
            self.papers_list.append({
                "paperID": paperID,
                "abstract": abstract,
                "bibtex": bibtex,
                "references": references
            })
            if self.debug:            
                print(f"Entry for paperID '{paperID}' added to papers list.")
        else:
            if self.debug:
                print(f"Entry for paperID '{paperID}' already exists in papers list.")

   
    def download_arxiv_pdf(self, arxiv_id, directory_path="."):
        """Download the PDF for the given ArXiv ID and save it to the specified directory."""
        # Build the URL
        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        # Ensure the directory exists; create it if it doesn't
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Construct the full path for saving the PDF
        save_path = os.path.join(directory_path, f"{arxiv_id}.pdf")

        # Download the PDF
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            if self.debug:
                print(f"Downloaded and saved as {save_path}")
        else:
            if self.debug:
                print(f"Failed to download the PDF for ArXiv ID: {arxiv_id}")


    def store_data_as_pickle(self, filename, filepath="."):
        """Store master_list and papers_list as a pickle file."""
        # Construct the full path for saving the pickle file
        save_path = os.path.join(filepath, filename)

        # Ensure the directory exists; create it if it doesn't
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        # Serialize and save the data
        with open(save_path, 'wb') as file:
            pickle.dump({"master_list": self.master_list, "papers_list": self.papers_list}, file)
        if self.debug:
            print(f"Data saved as {save_path}")


    def load_data_from_pickle(self, filename, filepath="."):
        """Load master_list and papers_list from a pickle file."""
        # Construct the full path for reading the pickle file
        load_path = os.path.join(filepath, filename)

        # Ensure the file exists
        if not os.path.exists(load_path):
            if self.debug:
                print(f"File {load_path} not found!")
            return None, None

        # Deserialize and load the data
        with open(load_path, 'rb') as file:
            data = pickle.load(file)
            master_list = data.get("master_list", [])
            papers_list = data.get("papers_list", [])

        return master_list, papers_list


# # Example usage:
# ss = SemanticScholar()

# # Get paperID by title
# title = "SlowMo: Improving Communication-Efficient Distributed SGD with Slow Momentum"
# paperID = ss.get_paper_id_by_title(title)

# # Get paper details
# bibtex, arxiv_id, publication_year, abstract = ss.get_paper_details(paperID)

# # Fetch and store references
# reference_ids = ss.fetch_and_store_references(paperID)

# # Add the paper and its references to the papers_list
# ss.add_to_papers_list(paperID, reference_ids)

# # Construct the directory name
# directory_name = "iclr_" + publication_year

# # Download the ArXiv PDF and save it to the specified directory
# ss.download_arxiv_pdf(arxiv_id, directory_name)

# # Store the master_list and papers_list data as a pickle file
# # This will save the data to a file named 'semantic_data.pkl' in the 'saved_data' directory.
# ss.store_data_as_pickle("semantic_data.pkl", "./saved_data")

# # retrieve the data
# master_list_2, papers_list_2 = ss.load_data_from_pickle("semantic_data.pkl", "./saved_data")

# todo - add key. NOTE 1 second between requests

# Dear Daniel,

# Thank you for requesting a Semantic Scholar API key! Your request has been approved. Here are the details:

#     S2 API Key: liZFgbFNYaJPLwGQVEXr4Qzx4MoCky21t3p3TCEc
#     Rate limit:
#         1 request per second for the following endpoints:
#             /paper/batch
#             /paper/search
#             /recommendations
#         10 requests / second for all other calls

# Please set your rate limit to below this threshold to avoid rejected requests.

 

# The API key needs to be sent in the header of the request as x-api-key directed at https://api.semanticscholar.org/ or via curl -Hx-api-key:$S2_API_KEY if coding in python.