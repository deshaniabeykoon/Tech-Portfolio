import argparse
from backend.services.yelp_service import load_and_store_yelp_data

def main():
    parser = argparse.ArgumentParser(description="Fetch and store Yelp data")
    parser.add_argument("--term", type=str, default="indian", help="Search term like 'indian'")
    parser.add_argument("--location", type=str, default="Auckland", help="Location like 'Auckland'")
    args = parser.parse_args()

    print(f"Fetching Yelp data for '{args.term}' in '{args.location}'...")
    load_and_store_yelp_data(args.term, args.location)
    print("Done.")

if __name__ == "__main__":
    main()
