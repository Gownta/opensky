# opensky

Aviation data analysis


# PRC Data Challenge

https://ansperformance.eu/study/data-challenge/

AI challenge to predict Actual Take-Off Weight

Hosted in partnership with OpenSky Network


# Data Sources

List of airports: https://ourairports.com/data/

List of Airlines: https://planefinder.net/
- website > Data > Airlines
- I downloaded the source for A-Z, then parsed the source to extract the airlines, in routes/

Flight API: https://www.flightaware.com/aeroapi/portal
- website > Products > AeroAPI
- Sign up for a personal plan, $5 free queires per month


# Setup

```
python3 -m venv python_venv
source python_venv/bin/activate
pip3 install pyopensky
pip3 install requests
```
