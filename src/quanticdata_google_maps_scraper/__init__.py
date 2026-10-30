"""Google Maps Scraper: Google Maps scraper for Python and the command line: businesses for a keyword and location, Google reviews of any place, and local business leads with emails, phones and socials, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_google_maps_scraper import GoogleMapsScraper

    scraper = GoogleMapsScraper()   # saved login (`google-maps-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.places(...)   # Google Maps businesses for a keyword in a location
    run = scraper.reviews(...)   # Google reviews of one place
    run = scraper.leads(...)   # local businesses with the emails, phones and socials on their websites
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["GoogleMapsScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class GoogleMapsScraper:
    """Google Maps Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="google-maps-scraper/0.1.0 (+https://github.com/quantumproxies/google-maps-scraper)", timeout=timeout)

    def places(
        self, query: str,
        *,
        location: str,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        max_results: Optional[int] = None,
        enrich_details: Optional[bool] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Businesses for a keyword in a location — name, rating, address, phone, website, coordinates.

        Args:
            query: Business type or keyword, e.g. "pizza restaurants", "dentist".
            location: City / area / address, e.g. "Brooklyn, NY" or "Milano".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: Interface language (hl), e.g. en, it, de.
            max_results: How many places to deliver at most (1–300). You pay only for delivered places.
            enrich_details: Look each place up to fill the weekly opening hours and the review count when Google's list leaves them out. Same price per place; set false for the list fields only (faster).
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 300 rows, one per place: see ``types.GoogleMapsPlacesRow``.
        """
        payload = {
            "query": query,
            "location": location,
            "country": country,
            "lang": lang,
            "max_results": max_results,
            "enrich_details": enrich_details,
        }
        return self.client.run_collector("google_maps_places", payload, wait=wait, timeout=timeout)

    def reviews(
        self, query: Optional[str] = None,
        *,
        data_id: Optional[str] = None,
        place_id: Optional[str] = None,
        location: Optional[str] = None,
        sort_by: Optional[str] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Google reviews of one place — rating, date, text, author, owner reply.

        Args:
            query: Alternative to ids: business name, resolved to the first place found.
            data_id: Feature id "0x…:0x…" from Google Maps places (preferred).
            place_id: Google place id (ChIJ…), alternative to data_id.
            location: Where to look the name up (with query).
            sort_by: Review ordering. One of: relevance, newest, highest_rating, lowest_rating.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: Interface language (hl), e.g. en, it, de.
            max_results: How many reviews to deliver at most (1–100). You pay only for delivered reviews.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per review: see ``types.PlaceReviewsRow``.
        """
        payload = {
            "query": query,
            "data_id": data_id,
            "place_id": place_id,
            "location": location,
            "sort_by": sort_by,
            "country": country,
            "lang": lang,
            "max_results": max_results,
        }
        return self.client.run_collector("place_reviews", payload, wait=wait, timeout=timeout)

    def leads(
        self, query: str,
        *,
        location: str,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        only_with_contacts: Optional[bool] = None,
        directories: Optional[Union[str, Sequence[str]]] = None,
        cross_check: Optional[bool] = None,
        verify_emails: Optional[bool] = None,
        deep_contacts: Optional[bool] = None,
        serp_emails: Optional[bool] = None,
        professionals: Optional[bool] = None,
        professional_phones: Optional[bool] = None,
        professionals_as_leads: Optional[bool] = None,
        enrich_details: Optional[bool] = None,
        company_data: Optional[bool] = None,
        min_revenue_eur: Optional[float] = None,
        keep_unknown_revenue: Optional[bool] = None,
        hq_in_area_only: Optional[bool] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Businesses for a keyword + location enriched with emails, phones and socials from their websites.

        Args:
            query: Business type, e.g. "dentist", "officina meccanica".
            location: City / area, e.g. "Austin, TX".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            lang: Interface language (hl), e.g. en, it, de.
            only_with_contacts: Deliver only leads with at least one email or phone.
            directories: Add businesses listed in these Italian directories that Google Maps did not return — the operators with no web presence. Off by default: it delivers, and bills, more rows. One of: paginegialle, paginebianche.
            cross_check: Resolve the same business across the channels into one record instead of delivering it twice. Matching is on the phone number, on street+civic plus a distinctive word of the name, or on the name alone when it carries two distinctive words. Adds sources, sources_count, matched_by and address_confirmed to every row. Off by default: it changes the shape of the delivered rows.
            verify_emails: Add email_check to each row: syntax, whether the domain has a mail server that accepts delivery (MX), whether the address is a role mailbox (info@, segreteria@) and whether the same address appears on other rows of the run. No SMTP probe per mailbox — see the field description.
            deep_contacts: When the homepage shows no email, try up to three of the site's own pages instead of one — contatti, dove siamo, and the privacy notice, which in Italy has to name the data controller with an address. Stops at the first page that yields an email, so it only costs more on the sites that were going to come back empty.
            serp_emails: For businesses whose site showed no email, run one web search on their domain and keep any address the search engine quotes in its snippets — only when it is on the business's own domain. Cheaper than another page fetch and works when the site is slow or blocks. One search per such business, plus one with the comune for a business whose only mailbox is named after another comune.
            professionals: Read MioDottore for the same category and place and attach the professionals who practise at each business — name, specialty, profile and published prices. Maps gives you the practice and its website; this gives you the person to address the letter to. Matched by phone, or by street and civic number in the same comune, never by name: a dentist is not called like the clinic.
            professional_phones: Open each professional's profile to read their phone numbers too. One extra request per professional; only meaningful with professionals.
            professionals_as_leads: With professionals: the practices MioDottore lists at addresses that Maps and the directories did not return become rows of their own (source: miodottore, sources_count 1) instead of being dropped — measured on six cities, about a hundred addresses per city the other channels did not have. Set false to only attach professionals to the businesses already found.
            enrich_details: Look up the place card of every business the map listed without its weekly hours or its review count, and fill them in (it can also add a website or phone the list row lacked). One small extra lookup per such business; off by default.
            company_data: For every lead that passed the contact filters: VAT number and tax code (from the site's footer and structured data, the Pagine Gialle listing, or one search on its domain), registered office, and the latest revenue published by public company-registry aggregators, with its year and source. A figure is read only from a result that carries the same VAT number, so a company with the same name elsewhere is never mixed in. Banks and financial intermediaries, whose statements have no revenue line, get their net banking income (margine di intermediazione). 1 to 3 extra searches per lead; off by default.
            min_revenue_eur: Keep only the leads whose verified revenue (or net banking income) is at least this amount; turns on company_data. Leads whose revenue could not be verified are dropped unless keep_unknown_revenue is set, and the run notes count the dropped leads by reason.
            keep_unknown_revenue: With min_revenue_eur: keep the leads whose revenue could not be verified, with the reason in company_note, instead of dropping them.
            hq_in_area_only: Drop the local offices of companies registered in another province (hq_in_area false); turns on company_data. Off by default: the local office of a national company is often the lead a buyer wants.
            max_results: How many leads to deliver at most (1–500). You pay only for delivered leads.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 500 rows, one per lead: see ``types.LocalBusinessLeadsRow``.
        """
        payload = {
            "query": query,
            "location": location,
            "country": country,
            "lang": lang,
            "only_with_contacts": only_with_contacts,
            "directories": _as_list(directories),
            "cross_check": cross_check,
            "verify_emails": verify_emails,
            "deep_contacts": deep_contacts,
            "serp_emails": serp_emails,
            "professionals": professionals,
            "professional_phones": professional_phones,
            "professionals_as_leads": professionals_as_leads,
            "enrich_details": enrich_details,
            "company_data": company_data,
            "min_revenue_eur": min_revenue_eur,
            "keep_unknown_revenue": keep_unknown_revenue,
            "hq_in_area_only": hq_in_area_only,
            "max_results": max_results,
        }
        return self.client.run_collector("local_business_leads", payload, wait=wait, timeout=timeout)
