"""Google Maps places for several keywords across several cities, in one CSV.

    python places_grid.py --keywords "coffee shop" "bakery" --cities "Austin, TX" "Dallas, TX" --country us

A place found by more than one search is written once, with every search that
found it in found_by and the city it was searched in. Useful to size a local
market or to build a prospect map before an outreach campaign.
"""

import argparse

from quanticdata_google_maps_scraper import GoogleMapsScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--keywords", nargs="+", required=True)
    parser.add_argument("--cities", nargs="+", required=True)
    parser.add_argument("--country", default="us")
    parser.add_argument("--per-search", type=int, default=50, help="places per keyword and city (max 300)")
    parser.add_argument("--out", default="places.csv")
    args = parser.parse_args()

    maps = GoogleMapsScraper()
    places = {}
    for city in args.cities:
        for keyword in args.keywords:
            run = maps.places(keyword, location=city, country=args.country, max_results=args.per_search)
            new = 0
            for place in run:
                key = place.get("data_id") or place.get("place_id") or (place["name"], place.get("address"))
                if key in places:
                    places[key]["found_by"] += "; " + place["found_by"]
                else:
                    places[key] = dict(place, city=city)
                    new += 1
            print(f"{keyword!r} in {city}: {len(run)} places, {new} not seen before")

    rows = list(places.values())
    write(rows, args.out)
    rated = [p["rating"] for p in rows if p.get("rating") is not None]
    average = sum(rated) / len(rated) if rated else 0.0
    print(f"{len(rows)} unique places written to {args.out}, average rating {average:.2f}")


if __name__ == "__main__":
    main()
