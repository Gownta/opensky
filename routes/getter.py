# TODO
#
# Get an API Key for FlightAware > Products > AeroAPI
# API Key located on https://www.flightaware.com/aeroapi/portal/
# On the Personal Plan, you can query for 10 pages (15 results each) every minute
# The queries cost $0.015 per page, max 10 pages per reply; $5 free per month
#
# Change the dates

import requests
import time
import json
import sys
from pathlib import Path
from itertools import count
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Flight:
    iata: str
    ident_iata: str
    src_iata: str
    dst_iata: str
    sched_out: str

    @classmethod
    def from_sched(cls, sched):
        iata = sched.get("operator_iata", None)
        ident_iata = sched.get("ident_iata", None)
        src_iata = (sched.get("origin", {}) or {}).get("code_iata", None)
        dst_iata = (sched.get("destination", {}) or {}).get("code_iata", None)
        sched_out = sched.get("scheduled_out", None)
        if iata and ident_iata and src_iata and dst_iata and sched_out:
            return cls(iata, ident_iata, src_iata, dst_iata, sched_out)
        return None


# Get all 3-letter airline ICAO codes
def get_airlines_3():
    with open("all_airlines_2024.txt", "r") as f:
        lines = f.readlines()
        return [line.split()[0] for line in lines]


# Load one page of data from aeroapi
def load_one(code, start, end):
    # From https://www.flightaware.com/commercial/aeroapi/#per-query-fee-section
    # this API costs $0.015 per result set. "a 'result set' is defined as 15 results"
    # Each page contains one result set
    url = f"https://aeroapi.flightaware.com/aeroapi/operators/{code}/flights/scheduled"
    headers = {
        "Accept": "application/json; charset=UTF-8",
        "x-apikey": "", # TODO enter your API key here
    }
    params = {
        "start": start,
        "end": end,
        "max_pages": "10",
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()


# Get the path where the data should be stored
def fpath(code, page):
    return Path(f"data/{code}_{page}")


def parse_flights(js):
    ret = []
    for sched in js.get("scheduled", []):
        flight = Flight.from_sched(sched)
        if flight:
            ret.append(flight)
    return ret


def get_flights(codes):
    npages = 0
    flights = []
    try:
        print("\n\n=== Starting ===\n\n")
        for code in codes:
            print(f"Getting data for {code}")
            start = "2024-09-01T00:00:00Z" # TODO change these dates
            end = "2024-09-02T00:00:00Z"
            for i in count(1):
                path = fpath(code, i)
                if path.exists():
                    print(f"  Loading data for {code}_{i}")
                    with path.open() as f:
                        js = json.loads(f.read())
                else:
                    print(f"  Downloading data for {code}_{i} (start={start})...", end="")
                    js = load_one(code, start, end)
                    with path.open("w") as fh:
                        fh.write(json.dumps(js, indent=4) + "\n")
                    npages += js["num_pages"]
                    print(" done")
                    time.sleep(65)

                iflys = parse_flights(js)
                flights.extend(iflys)
                if not js.get("links", None):
                    break

                assert iflys
                last = iflys[-1]
                new_start = last.sched_out
                assert new_start.endswith("0Z")
                new_start = f"{new_start[:-2]}1Z"
                assert new_start > start, f"{start} -> {new_start}"
                start = new_start
    finally:
        print(f"npages = {npages}, costing {npages * 0.015}")
    return flights


def topo(flights):
    a_to_bs = defaultdict(list)
    for f in flights:
        a_to_bs[f.src_iata].append(f)

    gmax = []
    maxls = defaultdict(list)
    airports = sorted(list(a_to_bs.keys()))
    for ap in reversed(airports):
        apm = []
        for f in a_to_bs[ap]:
            if f.dst_iata > ap:
                dmaxl = maxls[f.dst_iata]
                if len(dmaxl) >= len(apm):
                    apm = [f"{f.src_iata} -> {f.dst_iata} on {f.ident_iata}"] + dmaxl
        print(f"From airport {ap}, the longest number of hops is {len(apm)}")
        for f in apm:
            print("  " + f)
        maxls[ap] = apm
        if len(apm) > len(gmax):
            gmax = apm

    print(f"The longest route is {len(gmax)} flights:")
    for f in gmax:
        print("  " + f)


def main():
    airlines = sorted(get_airlines_3())
    flights = get_flights(airlines)
    topo(flights)

main()
