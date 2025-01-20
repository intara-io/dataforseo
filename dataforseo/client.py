import base64
import re

import requests


def contains_invalid_chars(input_string):
    invalid_chars_pattern = (
        r"[\u0000-\u001F]|[\u0021]|[\u0025]|[\u0028-\u002A]|[\u002C]|"
        r"[\u003B-\u0040]|[\u005C]|[\u005E]|[\u0060]|[\u007B-\u009F]|"
        r"[\u00A1-\u00A2]|[\u00A4-\u00A9]|[\u00AB-\u00B4]|[\u00B6]|"
        r"[\u00B8-\u00B9]|[\u00BB-\u00BF]|[\u00D7]|[\u00F7]|[\u0250-\u0258]|"
        r"[\u025A-\u02AF]|[\u02C2-\u02C5]|[\u02D2-\u02DF]|[\u02E5-\u02EB]|"
        r"[\u02ED]|[\u02EF-\u02FF]|[\u0375]|[\u037E]|[\u0384-\u0385]|"
        r"[\u0387]|[\u03F6]|[\u0482]|[\u0488-\u0489]|[\u055A-\u0560]|"
        r"[\u0588-\u058F]|[\u05BE]|[\u05C0]|[\u05C3]|[\u05C6]|[\u05EF]|"
        r"[\u05F3-\u060F]|[\u061B-\u061F]|[\u066A-\u066D]|[\u06D4]|"
        r"[\u06DD-\u06DE]|[\u06E9]|[\u06FD-\u06FE]|[\u0700-\u070F]|"
        r"[\u07F6-\u07F9]|[\u07FD-\u07FF]|[\u0830-\u083E]|[\u085E]|"
        r"[\u0870-\u089F]|[\u08B5]|[\u08BE-\u08D3]|[\u08E2]|[\u0964-\u0965]|"
        r"[\u0970]|[\u09F2-\u09FB]|[\u09FD-\u09FE]|[\u0A76]|[\u0AF0-\u0AF1]|"
        r"[\u0B55]|[\u0B70]|[\u0B72-\u0B77]|[\u0BF0-\u0BFA]|[\u0C04]|"
        r"[\u0C3C]|[\u0C5D]|[\u0C77-\u0C7F]|[\u0C84]|[\u0CDD]|[\u0D04]|"
        r"[\u0D4F]|[\u0D58-\u0D5E]|[\u0D70-\u0D79]|[\u0D81]|[\u0DF4]|"
        r"[\u0E3F]|[\u0E4F]|[\u0E5A-\u0E5B]|[\u0E86]|[\u0E89]|[\u0E8C]|"
        r"[\u0E8E-\u0E93]|[\u0E98]|[\u0EA0]|[\u0EA8-\u0EA9]|[\u0EAC]|"
        r"[\u0EBA]|[\u0F01-\u0F17]|[\u0F1A-\u0F1F]|[\u0F2A-\u0F34]|"
        r"[\u0F36]|[\u0F38]|[\u0F3A-\u0F3D]|[\u0F85]|[\u0FBE-\u0FC5]|"
        r"[\u0FC7-\u0FDA]|[\u104A-\u104F]|[\u109E-\u109F]|[\u10FB]"
    )

    return bool(re.search(invalid_chars_pattern, input_string))


class InvalidParameterError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code


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
        self,
        keyword: str | list[str] | list[tuple] = None,
        location_code: int = 2840,
        live: bool = True,
        task_id: str = None,
        debug: bool = False,
        **kwargs,
    ) -> dict | list[dict]:
        """
        Fetches SERP (Search Engine Results Page) data from the DataForSEO API.
        Args:
            keyword (str | list[str] | list[tuple]): A keyword or list of keywords to search for. If tuples, the second element should be the location code.
            location_code (int, optional): The location code for the search. Defaults to 2840 (USA).
            live (bool, optional): If True, fetch the data live. Otherwise, create a task. Defaults to True.
            task_id (str, optional): The ID of the task for which to retrieve SERP data. Defaults to None.
            **kwargs: Additional parameters to include in the payload.
        Returns:
            dict: The JSON response from the DataForSEO API.
        Docs:
            https://docs.dataforseo.com/v3/serp/overview/
        """
        if task_id:
            url = self.api_url + f"serp/google/organic/task_get/advanced/{task_id}"
            response = self.client.get(url)
            json_response = response.json()
            if json_response["tasks_error"] > 0:
                raise InvalidParameterError(
                    json_response["tasks"][0].get("status_message"),
                    error_code=json_response["tasks"][0].get("status_code"),
                )
            if debug:
                try:
                    print(
                        "Total request cost:",
                        sum([item["cost"] for item in json_response["tasks"]]),
                    )
                except:
                    print("Could not calculate total request cost")
                    pass
            return (
                json_response["tasks"][0]["result"]
                if "tasks" in json_response
                else None
            )

        if not keyword:
            raise ValueError("You must provide a keyword or list of keywords.")

        if isinstance(keyword, str):
            keyword = [keyword]

        if live:
            url = self.api_url + "serp/google/organic/live/advanced"
        else:
            url = self.api_url + "serp/google/organic/task_post"

        if isinstance(keyword[0], tuple):
            payload = [
                {
                    **{
                        "keyword": kw[0],
                        "location_code": kw[1],
                        "language_code": "en",
                        "device": "desktop",
                        "os": "windows",
                        "depth": 100,
                    },
                    **kwargs,
                }
                for kw in keyword
            ]
        else:
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

        response = response.json()
        if response["tasks_error"] > 0:
            raise InvalidParameterError(
                response["tasks"][0].get("status_message"),
                error_code=response["tasks"][0].get("status_code"),
            )

        if debug:
            try:
                print(
                    "Total request cost:",
                    sum([item["cost"] for item in response["tasks"]]),
                )
            except:
                print("Could not calculate total request cost")
                pass

        if live:
            return response

        return [
            {
                "task_id": task["id"],
                "keyword": task["data"]["keyword"],
                "location_code": task["data"]["location_code"],
            }
            for task in response["tasks"]
        ]

    def msv(
        self,
        keyword: str | list[str] | list[tuple] = None,
        location_code: int = 2840,
        date_from: str = None,
        date_to: str = None,
        live: bool = True,
        task_id: str = None,
        debug: bool = False,
        **kwargs,
    ) -> dict | list[dict]:
        """
        Fetches monthly search volume (MSV) data for given keywords from the DataForSEO API.
        Args:
            keyword (str | list[str] | list[tuple]): A keyword or list of keywords to search for. If tuples, the second element should be the location code.
            location_code (int, optional): The location code for the search volume data. Defaults to 2840 (USA).
            date_from (str, optional): The start date for the search volume data in 'YYYY-MM-DD' format. Defaults to None.
            date_to (str, optional): The end date for the search volume data in 'YYYY-MM-DD' format. Defaults to None.
            live (bool, optional): If True, fetch the data live. Otherwise, create a task. Defaults to True.
            task_id (str, optional): The ID of the task for which to retrieve MSV data. Defaults to None.
            **kwargs: Additional keyword arguments to include in the payload.
        Returns:
            dict: The response from the DataForSEO API containing the MSV data.
        Docs:
            https://docs.dataforseo.com/v3/keywords_data/google_ads/search_volume/live/
        """
        if task_id:
            url = (
                self.api_url
                + f"keywords_data/google_ads/search_volume/task_get/{task_id}"
            )
            response = self.client.get(url)
            json_response = response.json()
            if json_response["tasks_error"] > 0:
                raise InvalidParameterError(
                    json_response["tasks"][0].get("status_message"),
                    error_code=json_response["tasks"][0].get("status_code"),
                )

            if debug:
                try:
                    print(
                        "Total request cost:",
                        sum([item["cost"] for item in json_response["tasks"]]),
                    )
                except:
                    print("Could not calculate total request cost")
                    pass

            return (
                json_response["tasks"][0]["result"]
                if "tasks" in json_response
                else None
            )

        if not keyword:
            raise ValueError("You must provide a keyword or list of keywords.")

        if isinstance(keyword, str):
            keyword = [keyword]

        if isinstance(keyword[0], tuple):
            clean_keywords = [
                {"keyword": kw[0], "location_code": kw[1]}
                for kw in keyword
                if not contains_invalid_chars(kw[0])
            ]
            # group by location code
            clean_keywords = [
                {
                    "keywords": [
                        kw["keyword"]
                        for kw in clean_keywords
                        if kw["location_code"] == loc
                    ],
                    "location_code": loc,
                }
                for loc in set([kw["location_code"] for kw in clean_keywords])
            ]
        else:
            clean_keywords = [kw for kw in keyword if not contains_invalid_chars(kw)]

        if total_dropped := len(keyword) - len(clean_keywords):
            print("Dropped", total_dropped, "invalid keywords")

        if live:
            url = self.api_url + "keywords_data/google_ads/search_volume/live"
        else:
            url = self.api_url + "keywords_data/google_ads/search_volume/task_post"
        if isinstance(keyword[0], tuple):
            payload = [
                {
                    **{
                        "keywords": kw["keywords"],
                        "location_code": kw["location_code"],
                        "language_code": "en",
                        "date_from": date_from,
                        "date_to": date_to,
                    },
                    **kwargs,
                }
                for kw in clean_keywords
            ]
        else:
            payload = [
                {
                    **{
                        "keywords": clean_keywords,
                        "location_code": location_code,
                        "language_code": "en",
                        "date_from": date_from,
                        "date_to": date_to,
                    },
                    **kwargs,
                }
            ]
        response = self.client.post(url, json=payload)

        response = response.json()
        if response["tasks_error"] > 0:
            raise InvalidParameterError(
                response["tasks"][0].get("status_message"),
                error_code=response["tasks"][0].get("status_code"),
            )

        if debug:
            try:
                print(
                    "Total request cost:",
                    sum([item["cost"] for item in response["tasks"]]),
                )
            except:
                print("Could not calculate total request cost")
                pass

        if live:
            return response

        return [
            {
                "task_id": task["id"],
                "keywords": task["data"]["keywords"],
                "location_code": task["data"]["location_code"],
            }
            for task in response["tasks"]
        ]

    def keywords_for_site(
        self,
        site: str | list[str] = None,
        location_code: int = 2840,
        date_from: str = None,
        date_to: str = None,
        live: bool = True,
        task_id: str = None,
        **kwargs,
    ) -> dict:
        """
        Fetches keywords for a given site from the DataForSEO API.
        Args:
            site (str | list[str]): A single site/domain or a list of sites/domains to fetch keywords for.
            location_code (int): The location code for the keyword data. Defaults to 2840 (USA).
            date_from (str): The start date for the keyword data in 'YYYY-MM-DD' format.
            date_to (str): The end date for the keyword data in 'YYYY-MM-DD' format.
            live (bool): If True, fetch the data live. Otherwise, create a task. Defaults to True.
            task_id (str): The ID of the task for which to retrieve keyword data.
            **kwargs: Additional keyword arguments to include in the payload.
        Returns:
            dict: The response from the DataForSEO API containing the keyword data.
        Docs:
            https://docs.dataforseo.com/v3/keywords_data/google_ads/keywords_for_site/live/
        """
        if task_id:
            url = (
                self.api_url
                + f"keywords_data/google_ads/keywords_for_site/task_get/{task_id}"
            )
            response = self.client.get(url)
            json_response = response.json()
            if json_response["tasks_error"] > 0:
                raise InvalidParameterError(
                    json_response["tasks"][0].get("status_message"),
                    error_code=json_response["tasks"][0].get("status_code"),
                )

            return (
                json_response["tasks"][0]["result"]
                if "tasks" in json_response
                else None
            )

        if not site:
            raise ValueError("You must provide a site or list of sites.")

        if live:
            url = self.api_url + "keywords_data/google_ads/keywords_for_site/live"
        else:
            url = self.api_url + "keywords_data/google_ads/keywords_for_site/task_post"

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

        response = response.json()
        if response["tasks_error"] > 0:
            raise InvalidParameterError(
                response["tasks"][0].get("status_message"),
                error_code=response["tasks"][0].get("status_code"),
            )

        if live:
            return response

        return [
            {
                "task_id": task["id"],
                "target": task["data"]["target"],
                "location_code": task["data"]["location_code"],
            }
            for task in response["tasks"]
        ]

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
