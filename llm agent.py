#from typing import AnyStr, List, Type, Optional
from pydantic import BaseModel, Field
from scholarly import scholarly
from itertools import islice
from typing import Any, AnyStr, List, Type, Optional



class BaseTool:
    """
    Base class for all tools.
    """
    name: str
    description: str
    args_schema: Optional[Type[BaseModel]]

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Method to run the tool synchronously.
        """
        raise NotImplementedError

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        """
        Method to run the tool asynchronously.
        """
        raise NotImplementedError


class SearchAuthorByNameArgs(BaseModel):
    """
    Pydantic model for arguments schema for searching author by name tool.
    """
    author: str = Field(..., description="Author name with the institute name (optional), e.g., Tan Lee")
    top_k: int = Field(..., description="Number of results to display. 5 is preferred.")


class SearchAuthorByName(BaseTool):
    """
    Tool to search an author with Google Scholar using their name.
    """
    name = "search_author_by_name"
    description = ("Search an author with Google Scholar."
                   "Input a name, return a list of authors with info (including UID)."
                   "You can repeat calling the function to get next results."
                   )
    args_schema: Optional[Type[BaseModel]] = SearchAuthorByNameArgs

    def _run(self, author: AnyStr, top_k: int = 5) -> str:
        results = scholarly.search_author(author)
        ans = []
        for it in islice(results, top_k):
            ans.append(str({
                'name': it["name"],
                'uid': it["scholar_id"],
                'affiliation': it["affiliation"],
                'interests': it['interests'],
                'citation': it['citedby'],
            }))
        if not ans:
            return "No further information available"
        return '\n\n'.join(ans)


class SearchAuthorByInterestsArgs(BaseModel):
    """
    Pydantic model for arguments schema for searching author by interests tool.
    """
    interests: str = Field(..., description="Research interests separated by comma, e.g., 'crowdsourcing,privacy'")
    top_k: int = Field(..., description="Number of results to display. 5 is preferred.")


class SearchAuthorByInterests(BaseTool):
    """
    Tool to search authors given keywords of research interests.
    """
    name = "search_author_by_interests"
    description = ("Search authors given keywords of research interests."
                   "Input interests, return a list of authors."
                   "You can repeat calling the function to get next results."
                   )
    args_schema: Optional[Type[BaseModel]] = SearchAuthorByInterestsArgs

    def _run(self, interests: AnyStr, top_k: int = 5) -> str:
        results = scholarly.search_keywords(interests.split(','))
        ans = []
        for it in islice(results, top_k):
            ans.append(str({
                'name': it["name"],
                'uid': it['scholar_id'],
                'affiliation': it['affiliation'],
                'interests': it['interests'],
                'citation': it['citedby'],
            }))
        if not ans:
            return "No further information available"
        return '\n\n'.join(ans)


class AuthorUID2PaperArgs(BaseModel):
    """
    Pydantic model for arguments schema for searching papers by author UID tool.
    """
    uid: str = Field(..., description="A unique identifier assigned to author in Google Scholar")
    sort_by: str = Field(..., description="Either 'citedby' or 'year'.")
    top_k: int = Field(..., description="Number of results to display. 5 is preferred.")


class AuthorUID2Paper(BaseTool):
    """
    Tool to search the papers given the UID of an author.
    """
    name = "author_uid2paper"
    description = ("Search the papers given the UID of an author."
                   "You can use search_author first to get UID."
                   "You can repeat calling the function to get next results."
                   )
    args_schema: Optional[Type[BaseModel]] = AuthorUID2PaperArgs

    def _run(self, uid: AnyStr, sort_by: AnyStr, top_k: int = 5) -> str:
        author = scholarly.search_author_id(uid)
        author = scholarly.fill(author, sortby=sort_by)
        ans = []
        for it in islice(author['publications'], top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['citation'],
                'citation': it['num_citations'],
            }))
        if not ans:
            return "No further information available"
        return '\n\n'.join(ans)


class SearchPaperArgs(BaseModel):
    """
    Pydantic model for arguments schema for searching papers by title tool.
    """
    title: str = Field(..., description="Title name")
    sort_by: str = Field(..., description="Either 'relevance' or 'date'.")
    top_k: int = Field(..., description="Number of results to display. 5 is preferred. Set to 1 if given the complete title")


class SearchPaper(BaseTool):
    """
    Tool to search a paper with the title relevant to the input text.
    """
    name = "search_paper"
    description = ("Search a paper with the title relevant to the input text."
                   "Input text query, return a list of papers."
                   "You can repeat calling the function to get next results."
                   )
    args_schema: Optional[Type[BaseModel]] = SearchPaperArgs

    def _run(self, title: AnyStr, sort_by: AnyStr, top_k: int = 5) -> str:
        results = scholarly.search_pubs(title, sort_by=sort_by)
        ans = []
        for it in islice(results, top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'author': it['bib']['author'],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['venue'],
                "abstract": it['bib']['abstract'],
                'url': it['pub_url'],
                'citation': it['num_citations'],
            }))
        if not ans:
            return "No further information available"
        return '\n\n'.join(ans)


class SearchSinglePaper(BaseTool):
    """
    Tool to search a paper with the title matching the input text.
    """
    name = "search_single_paper"
    description = ("Search a paper with the title matching the input text."
                   "Input text query, return a single paper."
                   )

    def _run(self, title: AnyStr, top_k: int = 1) -> str:
        paper = scholarly.search_single_pub(title)
        ans = []
        for it in islice([paper], top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'author': it['bib']['author'],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['venue'],
                "abstract": it['bib']['abstract'],
                'url': it['pub_url'],
                'citation': it['num_citations'],
            }))
        if not ans:
            return "No further information available"
        return '\n\n'.join(ans)


class SearchRelatedPaper(BaseTool):
    """
    Tool to search the papers related to the target one.
    """
    name = "search_related_paper"
    description = ("Search the papers related to the target one."
                   "Input the complete paper title, return a list of relevant papers."
                   "You can repeat calling the function to get next results."
                   )

    def _run(self, title: AnyStr, top_k: int = 5) -> str:
        paper = scholarly.search_single_pub(title)
        results = scholarly.get_related_articles(paper)
        ans = []
        for it in islice(results, top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'author': it['bib']['author'],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['venue'],
                "abstract": it['bib']['abstract'],
                'url': it['pub_url'],
                'citation': it['num_citations'],
            }))
        if not ans:
            return "No further information available"
        return '\n\n'.join(ans)


class SearchCitePaper(BaseTool):
    """
    Tool to search the papers citing to the target one.
    """
    name = "search_cite_paper"
    description = ("Search the papers citing to the target one."
                   "Input the complete paper title, return a list of papers citing the one."
                   "You can repeat calling the function to get next results."
                   )

    def _run(self, title: AnyStr, top_k: int = 5) -> str:
        paper = scholarly.search_single_pub(title)
        results = scholarly.citedby(paper)
        ans = []
        for it in islice(results, top_k):
            ans.append(str({
                'title': it['bib']["title"],
                'author': it['bib']['author'],
                'pub_year': it['bib']['pub_year'],
                'venue': it['bib']['venue'],
                "abstract": it['bib']['abstract'],
                'url': it['pub_url'],
                'citation': it['num_citations'],
            }))
        if not ans:
            return "No further information available"
        return '\n\n'.join(ans)


if __name__ == "__main__":
    search_tool = SearchSinglePaper()
    paper_title = "Large language model cascades with mixture of thoughts representations for cost-efficient reasoning"
    response = search_tool._run(paper_title)
    print(response)
