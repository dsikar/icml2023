# Semantic Scholar Wrapper
Using the [Semantic Scholar](https://www.semanticscholar.org/) API to perform Literature Surveys.
 
The API provides scientific publication data/metadata, such as abstract, bibtex citation, number of references, references, number of citations, authors. The article pdf file download link may be inferred from the arxivId key values, when present, and downloaded, when available, from [arxiv.org](https://arxiv.org/).

## Usage

A plain text file containing a list of articles, such as [icml2020-2023papers.txt](data/icml2020-2023papers.txt) from e.g. a conference website.

In [scripts/semantic_scholar_runner.py](scripts/semantic_scholar_runner.py) set conference and paperlist variables.

```
    conference = "icml"

    paper_list = "icml2020-2023papers.txt"
```
In the example given where the list contains approximately 5.5k paper titles, the execution times recorded are between 5 and 11 hours, depending on bandwidth and latency. Results are held in a dictionary, stored in a pickle file.

## Data Structure

Two lists of dictionaries hold the query results.
1. Master list
A list of dictionaries where each dictionary represents a paper, whether is is an accepted conference paper, or a paper cited by the conference paper.
```
# Structure:
# [
#     {
#         "title": "Paper Title",
#         "paperID": "unique_paper_id",
#         "arxivId": "arxiv_id",
#         "publication_year": "year_of_publication",
#     },
#     ... (more papers)
# ]
```
2. Paper list
A list of dictionaries where each dictionary represents an accepted conference paper and its references.
```
# Structure:
# [
#     {
#       "paperID": paperID,
#       "abstract": abstract,
#       "bibtex": bibtex,
#       "references": references,
#       "referenceCount": referenceCount,
#       "citationCount": citationCount
#     },
#     ... (more papers with their references)
# ]
```
## Output
Output is saved as a pickle file, named:
```
semantic_data_{suffix}_{counter}_{identifier}_files.pkl
```
The pickle file may then be used offline for processing.
