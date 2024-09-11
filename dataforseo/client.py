import base64

import requests


class DataForSEOClient:
    def __init__(self, api_key: str, sandbox: bool = False) -> None:
        """
        Initializes the DataForSEO client.
        Args:
            api_key (str): The API key for authenticating with the DataForSEO service.
            sandbox (bool, optional): If True, use the sandbox environment. Defaults to False.
        """

        self.api_key = api_key
        self.api_key_b64 = base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
        if sandbox:
            self.api_url = "https://sandbox.dataforseo.com/v3/"
        else:
            self.api_url = "https://api.dataforseo.com/v3/"
        self.client = requests.Session()
        self.client.headers.update(
            {
                "Authorization": f"Basic {self.api_key_b64}",
                "Content-Type": "application/json",
            }
        )

    def serp(
        self, keyword: str | list[str], location_code: int = 2840, **kwargs
    ) -> dict:
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
        if isinstance(keyword, str):
            keyword = [keyword]

        url = self.api_url + "serp/google/organic/live/advanced"
        payload = [
            {
                **{
                    "keyword": kw,
                    "location_code": location_code,
                    "language_code": "en",
                    "device": "desktop",
                    "os": "windows",
                    "depth": 100,
                },
                **kwargs,
            }
            for kw in keyword
        ]
        response = self.client.post(url, json=payload)
        return response.json()

    def msv(
        self,
        keyword: str | list[str],
        location_code: int = 2840,
        date_from: str = None,
        date_to: str = None,
        **kwargs,
    ) -> dict:
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
        if isinstance(keyword, str):
            keyword = [keyword]

        url = self.api_url + "keywords_data/google_ads/search_volume/live"
        payload = [
            {
                **{
                    "keywords": keyword,
                    "location_code": location_code,
                    "language_code": "en",
                    "date_from": date_from,
                    "date_to": date_to,
                },
                **kwargs,
            }
        ]
        response = self.client.post(url, json=payload)
        return response.json()

    def keywords_for_site(
        self,
        site: str | list[str],
        location_code: int = 2840,
        date_from: str = None,
        date_to: str = None,
        **kwargs,
    ) -> dict:
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
        url = self.api_url + "keywords_data/google_ads/keywords_for_site/live"

        if isinstance(site, str):
            site = [site]

        payload = [
            {
                "target": s,
                "location_code": location_code,
                "date_from": date_from,
                "date_to": date_to,
                **kwargs,
            }
            for s in site
        ]
        response = self.client.post(url, json=payload)
        return response.json()

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
        url = "backlinks/domain_pages/live"

        if isinstance(domain, str):
            domain = [domain]

        payload = [{"target": d, **kwargs} for d in domain]
        response = self.client.post(self.api_url + url, json=payload)
        return response.json()

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
        url = "backlinks/domain_pages_summary/live"

        if isinstance(domain, str):
            domain = [domain]

        payload = [{"target": d, **kwargs} for d in domain]
        response = self.client.post(self.api_url + url, json=payload)
        return response.json()
