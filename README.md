# Google Maps Scraper

[![ci](https://github.com/quantumproxies/google-maps-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/google-maps-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Google Maps from Python or the command line: businesses for a keyword and a location, the Google reviews of any place, and local business leads with the emails, phones and social profiles found on their websites, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/google-maps-scraper
google-maps-scraper login
google-maps-scraper places "pizza restaurants" --location "Brooklyn, NY" --country us --max-results 100 -o pizza.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `google-maps-scraper places` | keyword and location | Name, rating, address, phone, website, coordinates, 21 fields per row ([fields and price](https://quanticdata.io/collectors/google-maps-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper)) | up to 300 |
| `google-maps-scraper reviews` | place name and location | Rating, date, text, author, owner reply, 20 fields per row ([fields and price](https://quanticdata.io/collectors/google-reviews-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper)) | up to 100 |
| `google-maps-scraper leads` | keyword and location | Businesses for a keyword + location enriched with emails, phones and socials from their websites, 46 fields per row ([fields and price](https://quanticdata.io/collectors/lead-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper)) | up to 500 |

`--country` takes an ISO 3166-1 alpha-2 code (`us`, `gb`, `de`, `it`...) and sets the Google locale; `--lang` sets the interface language (`en`, `it`, `de`...), which is also the language of the opening hours. For Italian businesses, `leads` can add the listings of Pagine Gialle and Pagine Bianche (`--directories`), the professionals who practise at each address (`--professionals`) and the VAT number, registered office and latest published revenue (`--company-data`).

## Sample output

A real row from `google-maps-scraper places "pizza restaurants" --location Brooklyn --country us --max-results 3` (2026-10-22):

```json
{
  "name": "Dellarocco's Brick Oven Pizza",
  "rank": 1,
  "hours": "Thursday: 12–10 PM; Friday: 12–10:30 PM; Saturday: 12–10:30 PM; Sunday: 12–10 PM; Monday: 12–10 PM; Tuesday: 12–10 PM; Wednesday: 12–10 PM",
  "phone": "(718) 858-1010",
  "rating": 4.6,
  "address": "214 Hicks St, Brooklyn Heights, NY 11201",
  "data_id": "0x89c25a4634938a45:0x229fa22c7b1623b9",
  "reviews": 1390,
  "website": "dellaroccospizza.com",
  "category": "Pizza restaurant",
  "found_by": "pizza restaurants Brooklyn",
  "latitude": 40.6950091,
  "maps_url": "https://www.google.com/maps/search/?api=1&query=Dellarocco's%20Brick%20Oven%20Pizza%20214%20Hicks%20St%2C%20Brooklyn%20Heights%2C%20NY%2011201",
  "place_id": "0x89c25a4634938a45:0x229fa22c7b1623b9",
  "longitude": -73.9961082,
  "thumbnail": "https://lh3.googleusercontent.com/grass-cs/AABkmLdEyx5B5Vwzf2xYOznGZ7AGav3QkGfd3Ao9R-6aKtpH0jsh7C7zp2IXChEAQxKIGAxB2cvRRqDRi0D1dFXwkmR7PSfwdoH48JoOrMTfEj9PaPEYokXMDm3I1k6nEcVI4kYLkXm2iVTOc5e6=w129-h86-k-no",
  "open_state": "Open · Closes 10 PM",
  "description": "Thin-crust, brick-oven pizza with a gluten-free option, plus tap beers in an airy, minimalist space.",
  "price_level": null,
  "weekly_hours": {
    "Friday": "12–10:30 PM",
    "Monday": "12–10 PM",
    "Sunday": "12–10 PM",
    "Tuesday": "12–10 PM",
    "Saturday": "12–10:30 PM",
    "Thursday": "12–10 PM",
    "Wednesday": "12–10 PM"
  },
  "service_options": null
}
```

## Python

```python
from quanticdata_google_maps_scraper import GoogleMapsScraper

maps = GoogleMapsScraper()  # saved login, or QUANTICDATA_API_KEY

pizza = maps.places("pizza restaurants", location="Brooklyn, NY", country="us", max_results=50)
for p in pizza:
    print(p["name"], p["rating"], p["reviews"], p["phone"], p["website"])

reviews = maps.reviews("Dellarocco's Brick Oven Pizza", location="Brooklyn, NY", sort_by="newest", max_results=20)
for r in reviews:
    print(r["rating"], r["date"], r["has_owner_response"], (r["text"] or "")[:80])

leads = maps.leads("dentist", location="Austin, TX", country="us", only_with_contacts=True, max_results=100)
print(sum(1 for lead in leads if lead["emails"]), "leads with an email")
leads.to_csv("dentists_austin.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Lead lists for a city**: Turn a business type and a city into a CSV of leads with website, emails, phones and social profiles read from each business's own site, keeping only the ones you can contact. See [`examples/leads_to_csv.py`](examples/leads_to_csv.py).
- **Review monitoring**: Read the newest Google reviews of a list of places every day and append only the ones you have not seen yet to a CSV, with rating, date and owner reply. See [`examples/reviews_monitor.py`](examples/reviews_monitor.py).
- **Local market mapping**: Run several keywords across several cities and get one deduplicated CSV of places with category, rating, review count and coordinates. See [`examples/places_grid.py`](examples/places_grid.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `google-maps-scraper run <id> -o out.csv` collects it later.

### `google-maps-scraper places`

Businesses for a keyword in a location — name, rating, address, phone, website, coordinates.

```
google-maps-scraper places QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Business type or keyword, e.g. "pizza restaurants", "dentist". |
| `--location` | string |  | City / area / address, e.g. "Brooklyn, NY" or "Milano". Required. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | Interface language (hl), e.g. en, it, de. |
| `--max-results` | integer | `20` | How many places to deliver at most (1–300). You pay only for delivered places. |
| `--enrich-details` | boolean | `True` | Look each place up to fill the weekly opening hours and the review count when Google's list leaves them out. Same price per place; set false for the list fields only (faster). |

### `google-maps-scraper reviews`

Google reviews of one place — rating, date, text, author, owner reply.

```
google-maps-scraper reviews [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `--data-id` | string |  | Feature id "0x…:0x…" from Google Maps places (preferred). |
| `--place-id` | string |  | Google place id (ChIJ…), alternative to data_id. |
| `QUERY` | string |  | Alternative to ids: business name, resolved to the first place found. |
| `--location` | string |  | Where to look the name up (with query). |
| `--sort-by` | relevance / newest / highest_rating / lowest_rating | `relevance` | Review ordering. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | Interface language (hl), e.g. en, it, de. |
| `--max-results` | integer | `20` | How many reviews to deliver at most (1–100). You pay only for delivered reviews. |

### `google-maps-scraper leads`

Businesses for a keyword + location enriched with emails, phones and socials from their websites.

```
google-maps-scraper leads QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Business type, e.g. "dentist", "officina meccanica". |
| `--location` | string |  | City / area, e.g. "Austin, TX". Required. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--lang` | string |  | Interface language (hl), e.g. en, it, de. |
| `--only-with-contacts` | boolean | `False` | Deliver only leads with at least one email or phone. |
| `--directories` | paginegialle / paginebianche |  | Add businesses listed in these Italian directories that Google Maps did not return — the operators with no web presence. Off by default: it delivers, and bills, more rows. |
| `--cross-check` | boolean | `False` | Resolve the same business across the channels into one record instead of delivering it twice. Matching is on the phone number, on street+civic plus a distinctive word of the name, or on the name alone when it carries two distinctive words. Adds sources, sources_count, matched_by and address_confirmed to every row. Off by default: it changes the shape of the delivered rows. |
| `--verify-emails` | boolean | `False` | Add email_check to each row: syntax, whether the domain has a mail server that accepts delivery (MX), whether the address is a role mailbox (info@, segreteria@) and whether the same address appears on other rows of the run. No SMTP probe per mailbox — see the field description. |
| `--deep-contacts` | boolean | `False` | When the homepage shows no email, try up to three of the site's own pages instead of one — contatti, dove siamo, and the privacy notice, which in Italy has to name the data controller with an address. Stops at the first page that yields an email, so it only costs more on the sites that were going to come back empty. |
| `--serp-emails` | boolean | `False` | For businesses whose site showed no email, run one web search on their domain and keep any address the search engine quotes in its snippets — only when it is on the business's own domain. Cheaper than another page fetch and works when the site is slow or blocks. One search per such business, plus one with the comune for a business whose only mailbox is named after another comune. |
| `--professionals` | boolean | `False` | Read MioDottore for the same category and place and attach the professionals who practise at each business — name, specialty, profile and published prices. Maps gives you the practice and its website; this gives you the person to address the letter to. Matched by phone, or by street and civic number in the same comune, never by name: a dentist is not called like the clinic. |
| `--professional-phones` | boolean | `False` | Open each professional's profile to read their phone numbers too. One extra request per professional; only meaningful with professionals. |
| `--professionals-as-leads` | boolean | `True` | With professionals: the practices MioDottore lists at addresses that Maps and the directories did not return become rows of their own (source: miodottore, sources_count 1) instead of being dropped — measured on six cities, about a hundred addresses per city the other channels did not have. Set false to only attach professionals to the businesses already found. |
| `--enrich-details` | boolean | `False` | Look up the place card of every business the map listed without its weekly hours or its review count, and fill them in (it can also add a website or phone the list row lacked). One small extra lookup per such business; off by default. |
| `--company-data` | boolean | `False` | For every lead that passed the contact filters: VAT number and tax code (from the site's footer and structured data, the Pagine Gialle listing, or one search on its domain), registered office, and the latest revenue published by public company-registry aggregators, with its year and source. A figure is read only from a result that carries the same VAT number, so a company with the same name elsewhere is never mixed in. Banks and financial intermediaries, whose statements have no revenue line, get their net banking income (margine di intermediazione). 1 to 3 extra searches per lead; off by default. |
| `--min-revenue-eur` | number |  | Keep only the leads whose verified revenue (or net banking income) is at least this amount; turns on company_data. Leads whose revenue could not be verified are dropped unless keep_unknown_revenue is set, and the run notes count the dropped leads by reason. |
| `--keep-unknown-revenue` | boolean | `False` | With min_revenue_eur: keep the leads whose revenue could not be verified, with the reason in company_note, instead of dropping them. |
| `--hq-in-area-only` | boolean | `False` | Drop the local offices of companies registered in another province (hq_in_area false); turns on company_data. Off by default: the local office of a national company is often the lead a buyer wants. |
| `--max-results` | integer | `10` | How many leads to deliver at most (1–500). You pay only for delivered leads. |

## Output fields

<details><summary><code>google-maps-scraper places</code>: 21 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position across the merged pages. |
| `name` | string | Business name. |
| `rating` | number or null | Star rating (1–5). |
| `reviews` | integer or null | Review count. |
| `category` | string or null | Google category, e.g. "Pizza restaurant". |
| `price_level` | string or null | Price level as shown ($$, $10–20). |
| `address` | string or null | Street address as shown. |
| `phone` | string or null | Phone number as shown. |
| `website` | string or null | Website URL or domain. |
| `hours` | string or null | Opening hours as text, "Monday: 9 AM–5 PM; Tuesday: …" (one day only when the weekly table is not available). |
| `weekly_hours` | object or null | Opening hours per day, {"Monday": "9 AM–5 PM", …}, in the run's language. |
| `open_state` | string or null | Live state as shown at run time ("Open · Closes 11 pm"). |
| `service_options` | string or null | Dine-in · Takeout · Delivery… |
| `thumbnail` | string or null | Photo thumbnail URL. |
| `maps_url` | string or null | Google Maps link. |
| `latitude` | number or null | GPS latitude. |
| `longitude` | number or null | GPS longitude. |
| `place_id` | string or null | Google place id (ChIJ… or 0x…:0x…). |
| `data_id` | string or null | Feature id 0x…:0x… — input for Place reviews. |
| `description` | string or null | Editorial blurb when Google shows one. |
| `found_by` | string | The Google query that surfaced this place. |

</details>

<details><summary><code>google-maps-scraper reviews</code>: 20 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `review_id` | string or null | Google's review id. |
| `rating` | number or null | Stars (1–5). |
| `date` | string or null | Relative date as shown ("2 months ago"). |
| `iso_date` | string or null | ISO 8601 timestamp when exposed. |
| `text` | string or null | Review body. |
| `author` | string or null | Reviewer display name. |
| `author_url` | string or null | Reviewer's Maps contributor page. |
| `author_thumbnail` | string or null | Reviewer photo URL. |
| `link` | string or null | Direct link to the review. |
| `source` | string or null | Review source (Google, Tripadvisor…). |
| `images` | string[] | Photos attached to the review. |
| `owner_response_date` | string or null | Owner reply date. |
| `owner_response_text` | string or null | Owner reply text. |
| `data_id` | string | The place's data_id the review belongs to. |
| `place_name` | string or null | Place name when resolved from query. |
| `author_id` | string or null | Reviewer's Maps contributor id. |
| `has_owner_response` | boolean | True when the owner replied. |
| `text_length` | integer | Length of the review text in characters (0 for a rating-only review). |
| `image_count` | integer | How many photos the review carries. |

</details>

<details><summary><code>google-maps-scraper leads</code>: 46 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `name` | string | Business name. |
| `category` | string or null | Google category. |
| `rating` | number or null | Star rating. |
| `reviews` | integer or null | Review count. |
| `address` | string or null | Address. |
| `phone` | string or null | Phone from Google. |
| `website` | string or null | Website URL. |
| `emails` | string[] | Emails found on the site (mailto, Cloudflare-obfuscated mailto, JSON-LD, page text), ordered by usefulness: the contact mailbox first, personal ones next, PEC/DPO/privacy last — all real, but not all addresses you write a proposal to. When a network publishes one mailbox per branch, the one named after the row's comune comes first and those named after other comuni come after the neutral ones. |
| `phones` | string[] | Phones found on the site (tel: links) + Google phone. |
| `socials` | object | { facebook, instagram, linkedin, twitter, youtube, tiktok } URLs when found. |
| `maps_url` | string or null | Google Maps link. |
| `place_id` | string or null | Google place id. |
| `data_id` | string or null | Feature id. |
| `source_pages` | string[] | Website pages that were scanned. |
| `site_status` | string | scanned \| no_website \| unreachable \| blocked |
| `email_source` | string or null | With serp_emails: "search_snippet" when the address came from a search result rather than from the site itself. |
| `source` | string | Which channel delivered the row: "google_maps" or the directory name. |
| `sources` | string[] or null | With cross_check: every channel that listed this business. |
| `sources_count` | integer or null | With cross_check: how many independent channels agreed on it. A buyer checking a sample checks this column first. |
| `matched_by` | string[] or null | With cross_check: how the channels were tied together — "phone", "address" (same street and civic plus a distinctive word) or "name". |
| `address_confirmed` | boolean or null | With cross_check: two channels printed the same street and civic number, not merely the same name. |
| `names` | string[] or null | With cross_check: the other spellings the channels used — the legal name next to the signage. |
| `addresses` | string[] or null | With cross_check: the addresses the channels printed, when they differ. |
| `professionals` | object[] or null | With professionals: who practises at this address, as { name, specialty, url, phone, prices }. The business card says "Poliambulatorio X"; this says which fifteen doctors receive there. |
| `email_check` | object[] or null | With verify_emails: per address { email, status: ok \| no_mx \| duplicate \| invalid, mx, shared_with, role, other_branch }. "duplicate" means the same address is on other rows — a chain's head office, not a practice. other_branch: the mailbox is named after another comune than the row's (roma@ on the Milano office) — delivered, flagged so a list can leave it out. There is deliberately no per-mailbox SMTP probe: from a single exit it gets the range greylisted and most Italian servers answer "accept all" regardless, so the tick would mean nothing. |
| `hours` | string or null | Opening hours as the map shows them: today's line, or the whole week ("Monday: 9 AM–6 PM; …") when the weekly table is known. |
| `weekly_hours` | object or null | Weekly opening hours as { day: hours }, when the map has them (always looked up with enrich_details). |
| `open_state` | string or null | Open state as the map states it ("Open", "Closed", "Temporarily closed"…). |
| `latitude` | number or null | Latitude of the place. |
| `longitude` | number or null | Longitude of the place. |
| `price_level` | string or null | Price level as shown on the map ($, $$, €€…). |
| `checked_at` | string or null | Date (YYYY-MM-DD) the row was last checked: the end of this run. |
| `email_type` | string or null | First email of the row: "generic" for a role mailbox (info@, segreteria@, the same rule as email_check.role), "personal" otherwise, null without an email. |
| `legal_name` | string or null | With company_data: the registered company name as the public registry prints it. |
| `vat_id` | string or null | With company_data: the VAT number (partita IVA) the business publishes. For a member of an Italian VAT group, the group's number, which is the one valid on invoices and in VIES (see vat_group). |
| `tax_id` | string or null | With company_data: the company's own tax code (codice fiscale), the key of the business register. It differs from vat_id for members of a VAT group. |
| `vat_group` | boolean or null | With company_data: true when the business publishes its VAT number as a VAT group's ("Gruppo IVA …", "P.IVA Gruppo …"), false otherwise, null without a VAT number. Revenue is looked up by tax_id, never by the group's number. |
| `registered_city` | string or null | With company_data: municipality of the registered office. |
| `registered_province` | string or null | With company_data: province code of the registered office (RM, MI…). |
| `hq_in_area` | boolean or null | With company_data: the registered office is in the same province as this address. false = a local office of a company registered elsewhere; null when either province is unknown. |
| `revenue_eur` | number or null | With company_data: the latest revenue published for this VAT number, in euro. For banks and financial intermediaries, the net banking income (see revenue_metric). |
| `revenue_year` | integer or null | With company_data: the financial year of revenue_eur. |
| `revenue_metric` | string or null | With company_data: "fatturato" (revenue) or "margine_di_intermediazione" (net banking income of banks and financial intermediaries). |
| `revenue_source` | object or null | With company_data: { domain, url } of the page the figure was read from. |
| `company_note` | string or null | With company_data: why a field is empty (VAT number not found, revenue not published…) or how a figure was read (VAT group, consolidated figure, latest financial year found). |

</details>

## Sign-in and API keys

- `google-maps-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `google-maps-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `google-maps-scraper login --api-key`.
- `google-maps-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/google_maps_places/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "pizza restaurants", "location": "Brooklyn", "country": "us", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Google Maps scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a keyword and a location, or the name of a place, and get rows back; the requests run on QuanticData's side.

**Does it scrape Google reviews too?**

Yes. google-maps-scraper reviews takes a place name and its --location and returns its reviews with rating, date, text, reviewer and the owner's reply, sorted by relevance, newest, highest or lowest rating.

**How many results can one run return?**

Up to 300 places, 100 reviews or 500 leads per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Nested fields such as weekly hours and social profiles become dotted columns and lists such as emails are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/reviews_monitor.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [LinkedIn Scraper](https://github.com/quantumproxies/linkedin-scraper): LinkedIn scraper for Python and the command line.
- [Zillow Scraper](https://github.com/quantumproxies/zillow-scraper): Zillow scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=google-maps-scraper).
