"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class GoogleMapsPlacesRow(TypedDict, total=False):
    """One row of `google-maps-scraper places` (google_maps_places v1.1.0)."""

    rank: int
    """1-based position across the merged pages."""
    name: str
    """Business name."""
    rating: Optional[float]
    """Star rating (1–5)."""
    reviews: Optional[int]
    """Review count."""
    category: Optional[str]
    """Google category, e.g. "Pizza restaurant"."""
    price_level: Optional[str]
    """Price level as shown ($$, $10–20)."""
    address: Optional[str]
    """Street address as shown."""
    phone: Optional[str]
    """Phone number as shown."""
    website: Optional[str]
    """Website URL or domain."""
    hours: Optional[str]
    """Opening hours as text, "Monday: 9 AM–5 PM; Tuesday: …" (one day only when the weekly table is not available)."""
    weekly_hours: Dict[str, Any]
    """Opening hours per day, {"Monday": "9 AM–5 PM", …}, in the run's language."""
    open_state: Optional[str]
    """Live state as shown at run time ("Open · Closes 11 pm")."""
    service_options: Optional[str]
    """Dine-in · Takeout · Delivery…"""
    thumbnail: Optional[str]
    """Photo thumbnail URL."""
    maps_url: Optional[str]
    """Google Maps link."""
    latitude: Optional[float]
    """GPS latitude."""
    longitude: Optional[float]
    """GPS longitude."""
    place_id: Optional[str]
    """Google place id (ChIJ… or 0x…:0x…)."""
    data_id: Optional[str]
    """Feature id 0x…:0x… — input for Place reviews."""
    description: Optional[str]
    """Editorial blurb when Google shows one."""
    found_by: str
    """The Google query that surfaced this place."""

class PlaceReviewsRow(TypedDict, total=False):
    """One row of `google-maps-scraper reviews` (place_reviews v1.1.0)."""

    rank: int
    """1-based position."""
    review_id: Optional[str]
    """Google's review id."""
    rating: Optional[float]
    """Stars (1–5)."""
    date: Optional[str]
    """Relative date as shown ("2 months ago")."""
    iso_date: Optional[str]
    """ISO 8601 timestamp when exposed."""
    text: Optional[str]
    """Review body."""
    author: Optional[str]
    """Reviewer display name."""
    author_url: Optional[str]
    """Reviewer's Maps contributor page."""
    author_thumbnail: Optional[str]
    """Reviewer photo URL."""
    link: Optional[str]
    """Direct link to the review."""
    source: Optional[str]
    """Review source (Google, Tripadvisor…)."""
    images: List[str]
    """Photos attached to the review."""
    owner_response_date: Optional[str]
    """Owner reply date."""
    owner_response_text: Optional[str]
    """Owner reply text."""
    data_id: str
    """The place's data_id the review belongs to."""
    place_name: Optional[str]
    """Place name when resolved from query."""
    author_id: Optional[str]
    """Reviewer's Maps contributor id."""
    has_owner_response: bool
    """True when the owner replied."""
    text_length: int
    """Length of the review text in characters (0 for a rating-only review)."""
    image_count: int
    """How many photos the review carries."""

class LocalBusinessLeadsRow(TypedDict, total=False):
    """One row of `google-maps-scraper leads` (local_business_leads v1.8.1)."""

    rank: int
    """1-based position."""
    name: str
    """Business name."""
    category: Optional[str]
    """Google category."""
    rating: Optional[float]
    """Star rating."""
    reviews: Optional[int]
    """Review count."""
    address: Optional[str]
    """Address."""
    phone: Optional[str]
    """Phone from Google."""
    website: Optional[str]
    """Website URL."""
    emails: List[str]
    """Emails found on the site (mailto, Cloudflare-obfuscated mailto, JSON-LD, page text), ordered by usefulness: the contact mailbox first, personal ones next, PEC/DPO/privacy last — all real, but not all addresses you write a proposal to. When a network publishes one mailbox per branch, the one named after the row's comune comes first and those named after other comuni come after the neutral ones."""
    phones: List[str]
    """Phones found on the site (tel: links) + Google phone."""
    socials: Dict[str, Any]
    """{ facebook, instagram, linkedin, twitter, youtube, tiktok } URLs when found."""
    maps_url: Optional[str]
    """Google Maps link."""
    place_id: Optional[str]
    """Google place id."""
    data_id: Optional[str]
    """Feature id."""
    source_pages: List[str]
    """Website pages that were scanned."""
    site_status: str
    """scanned | no_website | unreachable | blocked"""
    email_source: Optional[str]
    """With serp_emails: "search_snippet" when the address came from a search result rather than from the site itself."""
    source: str
    """Which channel delivered the row: "google_maps" or the directory name."""
    sources: Optional[List[str]]
    """With cross_check: every channel that listed this business."""
    sources_count: Optional[int]
    """With cross_check: how many independent channels agreed on it. A buyer checking a sample checks this column first."""
    matched_by: Optional[List[str]]
    """With cross_check: how the channels were tied together — "phone", "address" (same street and civic plus a distinctive word) or "name"."""
    address_confirmed: Optional[bool]
    """With cross_check: two channels printed the same street and civic number, not merely the same name."""
    names: Optional[List[str]]
    """With cross_check: the other spellings the channels used — the legal name next to the signage."""
    addresses: Optional[List[str]]
    """With cross_check: the addresses the channels printed, when they differ."""
    professionals: Optional[List[Dict[str, Any]]]
    """With professionals: who practises at this address, as { name, specialty, url, phone, prices }. The business card says "Poliambulatorio X"; this says which fifteen doctors receive there."""
    email_check: Optional[List[Dict[str, Any]]]
    """With verify_emails: per address { email, status: ok | no_mx | duplicate | invalid, mx, shared_with, role, other_branch }. "duplicate" means the same address is on other rows — a chain's head office, not a practice. other_branch: the mailbox is named after another comune than the row's (roma@ on the Milano office) — delivered, flagged so a list can leave it out. There is deliberately no per-mailbox SMTP probe: from a single exit it gets the range greylisted and most Italian servers answer "accept all" regardless, so the tick would mean nothing."""
    hours: Optional[str]
    """Opening hours as the map shows them: today's line, or the whole week ("Monday: 9 AM–6 PM; …") when the weekly table is known."""
    weekly_hours: Dict[str, Any]
    """Weekly opening hours as { day: hours }, when the map has them (always looked up with enrich_details)."""
    open_state: Optional[str]
    """Open state as the map states it ("Open", "Closed", "Temporarily closed"…)."""
    latitude: Optional[float]
    """Latitude of the place."""
    longitude: Optional[float]
    """Longitude of the place."""
    price_level: Optional[str]
    """Price level as shown on the map ($, $$, €€…)."""
    checked_at: Optional[str]
    """Date (YYYY-MM-DD) the row was last checked: the end of this run."""
    email_type: Optional[str]
    """First email of the row: "generic" for a role mailbox (info@, segreteria@, the same rule as email_check.role), "personal" otherwise, null without an email."""
    legal_name: Optional[str]
    """With company_data: the registered company name as the public registry prints it."""
    vat_id: Optional[str]
    """With company_data: the VAT number (partita IVA) the business publishes. For a member of an Italian VAT group, the group's number, which is the one valid on invoices and in VIES (see vat_group)."""
    tax_id: Optional[str]
    """With company_data: the company's own tax code (codice fiscale), the key of the business register. It differs from vat_id for members of a VAT group."""
    vat_group: Optional[bool]
    """With company_data: true when the business publishes its VAT number as a VAT group's ("Gruppo IVA …", "P.IVA Gruppo …"), false otherwise, null without a VAT number. Revenue is looked up by tax_id, never by the group's number."""
    registered_city: Optional[str]
    """With company_data: municipality of the registered office."""
    registered_province: Optional[str]
    """With company_data: province code of the registered office (RM, MI…)."""
    hq_in_area: Optional[bool]
    """With company_data: the registered office is in the same province as this address. false = a local office of a company registered elsewhere; null when either province is unknown."""
    revenue_eur: Optional[float]
    """With company_data: the latest revenue published for this VAT number, in euro. For banks and financial intermediaries, the net banking income (see revenue_metric)."""
    revenue_year: Optional[int]
    """With company_data: the financial year of revenue_eur."""
    revenue_metric: Optional[str]
    """With company_data: "fatturato" (revenue) or "margine_di_intermediazione" (net banking income of banks and financial intermediaries)."""
    revenue_source: Dict[str, Any]
    """With company_data: { domain, url } of the page the figure was read from."""
    company_note: Optional[str]
    """With company_data: why a field is empty (VAT number not found, revenue not published…) or how a figure was read (VAT group, consolidated figure, latest financial year found)."""
