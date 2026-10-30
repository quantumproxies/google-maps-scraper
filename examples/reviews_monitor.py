"""New Google reviews of a list of places, appended to one CSV.

Reads places.txt, one place per line as "name | location" (the location can be
left out when --location is given), reads the newest reviews of each place and
appends only the reviews that are not in the CSV yet. Run it daily from cron:

    0 8 * * *  cd /path/to/here && python reviews_monitor.py --location "Brooklyn, NY"

Needs a login (`google-maps-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_google_maps_scraper import GoogleMapsScraper

FIELDS = ["checked_at", "place_name", "data_id", "review_id", "rating", "iso_date", "date", "author",
          "text", "has_owner_response", "owner_response_text", "link"]


def read_places(path, default_location):
    places = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, _, location = line.partition("|")
            places.append((name.strip(), location.strip() or default_location))
    return places


def seen_ids(path):
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["review_id"] for row in csv.DictReader(fh) if row.get("review_id")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--places", default="places.txt", help='file with one "name | location" per line')
    parser.add_argument("--location", help="location for the lines that do not name one")
    parser.add_argument("--country", default="us")
    parser.add_argument("--per-place", type=int, default=20, help="newest reviews to read per place (max 100)")
    parser.add_argument("--out", default="reviews.csv")
    args = parser.parse_args()

    maps = GoogleMapsScraper()
    seen = seen_ids(args.out)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    added = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        for name, location in read_places(args.places, args.location):
            run = maps.reviews(name, location=location, country=args.country, sort_by="newest",
                               max_results=args.per_place)
            fresh = [r for r in run if not r.get("review_id") or r["review_id"] not in seen]
            for review in fresh:
                writer.writerow({"checked_at": checked_at, **review})
                if review.get("review_id"):
                    seen.add(review["review_id"])
            low = sum(1 for r in fresh if r.get("rating") is not None and r["rating"] <= 2)
            print(f"{name}: {len(fresh)} new reviews, {low} of them at 1 or 2 stars")
            added += len(fresh)
    print(f"{added} new reviews appended to {args.out}")


if __name__ == "__main__":
    main()
