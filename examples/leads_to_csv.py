"""Local business leads for one city, in a CSV ready for outreach.

    python leads_to_csv.py "dentist" --location "Austin, TX" --country us --max 200

Each lead carries its Google Maps listing (name, category, rating, address,
phone, website) plus the emails, phones and social profiles found on its own
website. By default only leads with at least one email or phone are kept; add
--all to keep every business the map returns.
"""

import argparse

from quanticdata_google_maps_scraper import GoogleMapsScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("query", help='business type, e.g. "dentist"')
    parser.add_argument("--location", required=True, help='city or area, e.g. "Austin, TX"')
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", help="interface language, e.g. en, it, de")
    parser.add_argument("--max", type=int, default=100, help="leads to deliver (max 500)")
    parser.add_argument("--deep", action="store_true",
                        help="when a homepage shows no email, also read up to three more pages of the site")
    parser.add_argument("--all", action="store_true", help="keep businesses with no email or phone too")
    parser.add_argument("--out", default="leads.csv")
    args = parser.parse_args()

    maps = GoogleMapsScraper()
    run = maps.leads(args.query, location=args.location, country=args.country, lang=args.lang,
                     only_with_contacts=not args.all, deep_contacts=args.deep, max_results=args.max)

    with_email = sum(1 for lead in run if lead.get("emails"))
    with_social = sum(1 for lead in run if lead.get("socials"))
    write(run, args.out)
    print(f"{len(run)} leads written to {args.out}: {with_email} with an email, {with_social} with a social profile")


if __name__ == "__main__":
    main()
