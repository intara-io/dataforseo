# DataForSEOClient

`DataForSEOClient` is a Python client for interacting with the DataForSEO API. This client allows you to fetch SERP (Search Engine Results Page) data and other SEO-related metrics.

## Installation

To install the package, use the following command:

### pip
```bash
pip install git+https://github.com/Tre-Jones-Consulting/dataforseo
```

### poetry

```bash
poetry add git+https://github.com/Tre-Jones-Consulting/dataforseo
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
def serp(self, keyword: str | list[str], location_code: int = 2840, **kwargs) -> dict:
    """
    Fetches SERP (Search Engine Results Page) data from the DataForSEO API.
    Args:
        keyword (str | list[str]): A keyword or a list of keywords to search for.
        location_code (int, optional): The location code for the search. Defaults to 2840 (USA).
        **kwargs: Additional parameters to include in the payload.
    Returns:
        dict: The JSON response from the DataForSEO API.
    Docs:
        https://docs.dataforseo.com/v3/serp/overview/
    """
```

**Example:**

```python
response = client.serp(keyword="python programming")
print(response)
```

#### `msv`

Fetches Monthly Search Volume (MSV) data from the DataForSEO API.

```python
def msv(self, keyword: str | list[str], location_code: int = 2840, date_from: str = None, date_to: str = None, **kwargs) -> dict:
    """
    Fetches monthly search volume (MSV) data for given keywords from the DataForSEO API.
    Args:
        keyword (str | list[str]): A single keyword or a list of keywords to fetch MSV data for.
        location_code (int, optional): The location code for the search volume data. Defaults to 2840 (USA).
        date_from (str, optional): The start date for the search volume data in 'YYYY-MM-DD' format. Defaults to None.
        date_to (str, optional): The end date for the search volume data in 'YYYY-MM-DD' format. Defaults to None.
        **kwargs: Additional keyword arguments to include in the payload.
    Returns:
        dict: The response from the DataForSEO API containing the MSV data.
    Docs:
        https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live/
    """
```

**Example:**

```python
response = client.msv(keyword="python programming")
print(response)
```

#### `keywords_for_site`

Fetches keywords for a given site from the DataForSEO API.

```python
def keywords_for_site(self, site: str, location_code: int = 2840, date_from: str = None, date_to: str = None, **kwargs) -> dict:
    """
    Fetches keywords for a given site from the DataForSEO API.
    Args:
        site (str | list[str]): A single site/domain or a list of sites/domains to fetch keywords for.
        location_code (int): The location code for the keyword data. Defaults to 2840 (USA).
        date_from (str): The start date for the keyword data in 'YYYY-MM-DD' format.
        date_to (str): The end date for the keyword data in 'YYYY-MM-DD' format.
        **kwargs: Additional keyword arguments to include in the payload.
    Returns:
        dict: The response from the DataForSEO API containing the keyword data.
    Docs:
        https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/live/
    """
```

**Example:**

```python
response = client.keywords_for_site(site="example.com")
print(response)
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
response = client.domain_pages(domain="example.com")
print(response)
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
response = client.domain_pages_summary(domain="example.com")
print(response)
```

## Locations

A list of location codes can be found in the following files:

- [locations_us.csv](locations_us.csv)
- [locations_world.csv](locations_world.csv)