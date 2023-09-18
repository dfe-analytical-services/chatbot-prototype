import argparse
import requests
import os
import sys


class DataIngestionClient:
    API_BASE_URLS = {
        "local": "http://localhost:8000/api"
    }

    def __init__(self, env: str, timeout: float):
        self.env = (env,)
        self.api_base_url = DataIngestionClient.API_BASE_URLS[env]
        self.timeout = timeout

    def build_methodologies(self) -> str:
        r = requests.post(f"{self.api_base_url}/maintenance/methodologies/build", timeout=self.timeout)
        return r.json()

    def build_publications(self) -> str:
        r = requests.post(f"{self.api_base_url}/maintenance/publications/build", timeout=self.timeout)
        return r.json()

    def clear(self) -> None:
        requests.delete(f"{self.api_base_url}/maintenance/clear", timeout=self.timeout)

    def update_methodology(self, slug: str) -> str:
        r = requests.post(f"{self.api_base_url}/methodologies/{slug}/update", timeout=self.timeout)
        return r.json()

    def update_publication(self, slug: str) -> str:
        r = requests.post(f"{self.api_base_url}/publications/{slug}/update", timeout=self.timeout)
        return r.json()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        prog=f"pipenv run python {os.path.basename(__file__)}",
        description="Make data ingestion requests to build and maintain the database.",
    )

    action_group = ap.add_mutually_exclusive_group(required=True)

    ap.add_argument(
        "--env",
        dest="env",
        default="local",
        choices=["local"],
        help="The environment to run against",
        type=str,
        required=False,
    )

    ap.add_argument(
        "--timeout",
        dest="timeout",
        default=30.0,
        nargs="?",
        help="Timout for the request in number of seconds",
        type=float,
        required=False,
    )

    action_group.add_argument('--clear',
                              help="Clear the vector database",
                              action='store_true')
    action_group.add_argument('--build-methodologies',
                              help="Build all methodologies",
                              action='store_true')
    action_group.add_argument('--build-publications',
                              help="Build all publications",
                              action='store_true')
    action_group.add_argument('--update-methodology',
                              help="Update a specific methodology. Use in conjunction with --slug",
                              action='store_true')
    action_group.add_argument('--update-publication',
                              help="Update a specific publication. Use in conjunction with --slug",
                              action='store_true')

    ap.add_argument('--slug',
                    type=str,
                    required='--update-methodology' in sys.argv or '--update-publication' in sys.argv,
                    help='Slug parameter required when using --update-methodology or --update-publication')

    args = ap.parse_args()

    client = DataIngestionClient(
        env=args.env, timeout=args.timeout
    )

    if args.clear:
        res = client.clear()
    elif args.build_methodologies:
        res = client.build_methodologies()
    elif args.build_publications:
        res = client.build_publications()
    elif args.update_methodology:
        res = client.update_methodology(slug=args.slug)
    elif args.update_publication:
        res = client.update_publication(slug=args.slug)

    if (res is not None):
        print(res)
