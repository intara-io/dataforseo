# DataForSEOClient

`DataForSEOClient` is a Python client for interacting with the DataForSEO API. This client allows you to fetch SERP (Search Engine Results Page) data and other SEO-related metrics.

## Installation

To install the package, use the following command:

### pip
```bash
pip install git+https://github.com/intara-io/dataforseo
```

### poetry

```bash
poetry add git+https://github.com/intara-io/dataforseo
```

## Usage

### Initialization

To initialize `DataForSEOClient`, you need an API key. You can also specify whether to use the sandbox environment.

```python
from dataforseo.client import DataForSEOClient

api_key = "your_api_key_here"
client = DataForSEOClient(api_key, sandbox=True)
```

### Methods

#### `serp`

Fetches SERP (Search Engine Results Page) data from the DataForSEO API.

```python
def serp(self, keyword: str | list[str], location_code: int = 2840, live: bool = False, task_id: str = None, **kwargs) -> dict:
    """
    Fetches SERP (Search Engine Results Page) data from the DataForSEO API.
    Args:
        keyword (str | list[str]): A keyword or a list of keywords to search for.
        location_code (int, optional): The location code for the search. Defaults to 2840 (USA).
        live (bool, optional): Whether to fetch live data. Defaults to False.
        task_id (str, optional): The task ID for the search. Defaults to None.
        **kwargs: Additional parameters to include in the payload.
    Returns:
        dict: The JSON response from the DataForSEO API.
    Docs:
        https://docs.dataforseo.com/v3/serp/overview/
    """
```

**Example:**

```python
In [1]: from dataforseo.client import DataForSEOClient

In [2]: client = DataForSEOClient(api_key="<api_key>", sandbox=False)

In [3]: res = client.serp("seo consulting")

In [4]: res["tasks"][0]["result"]
Out[4]:
[{'keyword': 'seo consulting',
  'type': 'organic',
  'se_domain': 'google.com',
  'location_code': 2840,
  'language_code': 'en',
  'check_url': 'https://www.google.com/search?q=seo%20consulting&num=100&hl=en&gl=US&gws_rd=cr&ie=UTF-8&oe=UTF-8&glp=1&uule=w+CAIQIFISCQs2MuSEtepUEUK33kOSuTsc',
  'datetime': '2024-09-11 09:44:26 +00:00',
  'spell': None,
  'item_types': ['organic', 'people_also_ask', 'images', 'related_searches'],
  'se_results_count': 43500000,
  'items_count': 102,
  'items': [{'type': 'organic',
    'rank_group': 1,
    'rank_absolute': 1,
    'position': 'left',
    'xpath': '/html[1]/body[1]/div[3]/div[1]/div[13]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]',
    'domain': 'www.coursera.org',
    'title': 'What Is an SEO Consultant and Do You Need One?',
    'url': 'https://www.coursera.org/articles/seo-consultant',
    'cache_url': None,
    'related_search_url': None,
    'breadcrumb': 'https://www.coursera.org › ... › Business › Marketing',
    'website_name': 'Coursera',
    'is_image': False,
    'is_video': False,
    'is_featured_snippet': False,
    'is_malicious': False,
    'is_web_story': False,
    'description': "An SEO consultant helps businesses improve their websites' ranking in search engine results. An SEO consultant's goal is to make it easier for\xa0...",
    'pre_snippet': '11/29/2023 00:00:00',
    'extended_snippet': None,
    'images': None,
    'amp_version': False,
    'rating': None,
    'price': None,
    'highlighted': ['SEO consultant', "SEO consultant's"],
    'links': None,
    'faq': None,
    'extended_people_also_search': None,
    'about_this_result': None,
    'related_result': None,
    'timestamp': '2023-11-29 00:00:00 +00:00',
    'rectangle': None},
...
```


#### `msv`

Fetches Monthly Search Volume (MSV) data from the DataForSEO API.

```python
def msv(self, keyword: str | list[str], location_code: int = 2840, date_from: str = None, date_to: str = None, live: bool = False, task_id: str = None, **kwargs) -> dict:
    """
    Fetches monthly search volume (MSV) data for given keywords from the DataForSEO API.
    Args:
        keyword (str | list[str]): A single keyword or a list of keywords to fetch MSV data for.
        location_code (int, optional): The location code for the search volume data. Defaults to 2840 (USA).
        date_from (str, optional): The start date for the search volume data in 'YYYY-MM-DD' format. Defaults to None.
        date_to (str, optional): The end date for the search volume data in 'YYYY-MM-DD' format. Defaults to None.
        live (bool, optional): Whether to fetch live data. Defaults to False.
        task_id (str, optional): The task ID for the search. Defaults to None.
        **kwargs: Additional keyword arguments to include in the payload.
    Returns:
        dict: The response from the DataForSEO API containing the MSV data.
    Docs:
        https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live/
    """
```

**Example:**

```python
In [1]: from dataforseo.client import DataForSEOClient

In [2]: client = DataForSEOClient(api_key="<api_key>", sandbox=False)

In [3]: res = client.msv("seo consulting")

In [4]: res["tasks"][0]["result"]
Out[4]:
[{'keyword': 'seo consulting',
  'spell': None,
  'location_code': 2840,
  'language_code': 'en',
  'search_partners': False,
  'competition': 'LOW',
  'competition_index': 9,
  'search_volume': 9900,
  'low_top_of_page_bid': 10,
  'high_top_of_page_bid': 48.04,
  'cpc': 48.04,
  'monthly_searches': [{'year': 2024, 'month': 8, 'search_volume': 8100},
   {'year': 2024, 'month': 7, 'search_volume': 8100},
   {'year': 2024, 'month': 6, 'search_volume': 6600},
   {'year': 2024, 'month': 5, 'search_volume': 18100},
   {'year': 2024, 'month': 4, 'search_volume': 8100},
   {'year': 2024, 'month': 3, 'search_volume': 9900},
   {'year': 2024, 'month': 2, 'search_volume': 8100},
   {'year': 2024, 'month': 1, 'search_volume': 12100},
   {'year': 2023, 'month': 12, 'search_volume': 8100},
   {'year': 2023, 'month': 11, 'search_volume': 9900},
   {'year': 2023, 'month': 10, 'search_volume': 8100},
   {'year': 2023, 'month': 9, 'search_volume': 8100}]}]

```

#### `keywords_for_site`

Fetches keywords for a given site from the DataForSEO API.

```python
def keywords_for_site(self, site: str, location_code: int = 2840, date_from: str = None, date_to: str = None, live: bool = False, task_id: str = None, **kwargs) -> dict:
    """
    Fetches keywords for a given site from the DataForSEO API.
    Args:
        site (str | list[str]): A single site/domain or a list of sites/domains to fetch keywords for.
        location_code (int): The location code for the keyword data. Defaults to 2840 (USA).
        date_from (str): The start date for the keyword data in 'YYYY-MM-DD' format.
        date_to (str): The end date for the keyword data in 'YYYY-MM-DD' format.
        live (bool, optional): Whether to fetch live data. Defaults to False.
        task_id (str, optional): The task ID for the search. Defaults to None.
        **kwargs: Additional keyword arguments to include in the payload.
    Returns:
        dict: The response from the DataForSEO API containing the keyword data.
    Docs:
        https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/live/
    """
```

**Example:**

```python
In [1]: from dataforseo.client import DataForSEOClient

In [2]: client = DataForSEOClient(api_key="<api_key>", sandbox=False)

In [3]: res = client.keywords_for_site("intara.io")

In [4]: res["tasks"][0]["result"]
Out[4]:
[{'keyword': 'content strategy',
  'location_code': 2840,
  'language_code': None,
  'search_partners': False,
  'competition': 'LOW',
  'competition_index': 8,
  'search_volume': 6600,
  'low_top_of_page_bid': 1.36,
  'high_top_of_page_bid': 12.88,
  'cpc': 8.05,
  'monthly_searches': [{'year': 2024, 'month': 8, 'search_volume': 5400},
   {'year': 2024, 'month': 7, 'search_volume': 6600},
   {'year': 2024, 'month': 6, 'search_volume': 5400},
   {'year': 2024, 'month': 5, 'search_volume': 6600},
   {'year': 2024, 'month': 4, 'search_volume': 6600},
   {'year': 2024, 'month': 3, 'search_volume': 6600},
   {'year': 2024, 'month': 2, 'search_volume': 6600},
   {'year': 2024, 'month': 1, 'search_volume': 8100},
   {'year': 2023, 'month': 12, 'search_volume': 5400},
   {'year': 2023, 'month': 11, 'search_volume': 6600},
   {'year': 2023, 'month': 10, 'search_volume': 8100},
   {'year': 2023, 'month': 9, 'search_volume': 6600}],
  'keyword_annotations': {'concepts': [{'name': 'strategies',
     'concept_group': {'name': 'Others', 'type': None}},
    {'name': 'Non-Brands',
     'concept_group': {'name': 'Non-Brands', 'type': 'NON_BRAND'}}]}},
 {'keyword': 'content marketing',
...
```

#### `domain_pages`

Fetches domain pages data from the DataForSEO API.

```python
def domain_pages(self, domain: str | list[str], **kwargs) -> dict:
    """
    Retrieve overview of domain pages with backlink data for each page.
    Args:
        domain (str): The domain for which to retrieve pages.
        **kwargs: Additional parameters to include in the request payload.
    Returns:
        dict: The JSON response from the API containing the domain pages data.
    Docs:
        https://docs.dataforseo.com/v3/backlinks/domain_pages/live/
    """
```

**Example:**

```python
In [1]: from dataforseo.client import DataForSEOClient

In [2]: client = DataForSEOClient(api_key="<api_key>", sandbox=False)

In [3]: res = client.domain_pages("intara.io", limit=1)
```

#### `domain_pages_summary`

Fetches domain pages summary data from the DataForSEO API.

```python
def domain_pages_summary(self, domain: str | list[str], **kwargs) -> dict:
    """
    Retrieve summary data on all backlinks and related metrics for each page of the
    target domain or subdomain you specify. If you indicate a single page as a
    target, you will get comprehensive summary data on all backlinks for that page.
    Args:
        domain (str): The domain for which to retrieve pages.
        **kwargs: Additional parameters to include in the request payload.
    Returns:
        dict: The JSON response from the API containing the domain pages data.
    Docs:
        https://docs.dataforseo.com/v3/backlinks/domain_pages_summary/live/
    """
```

**Example:**

```python
In [1]: from dataforseo.client import DataForSEOClient

In [2]: client = DataForSEOClient(api_key="<api_key>", sandbox=False)

In [3]: res = client.domain_pages_summary("intara.io")
```

## Locations

A list of location codes can be found in the following files:

- [locations_us.csv](locations_us.csv)
- [locations_world.csv](locations_world.csv)
