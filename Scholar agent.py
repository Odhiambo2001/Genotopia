from gentopia.tools import summarize_paper
from gentopia.tools import search_cite_paper

paper_summary = summarize_paper("GenTopia: A collaborative platform for tool-augmented LLMs")
print(paper_summary)
citing_papers = search_cite_paper("GenTopia: A collaborative platform for tool-augmented LLMs")
print(citing_papers)
