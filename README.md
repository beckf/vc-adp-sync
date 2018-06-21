![Alt text](screenshots/adp-vc-logo.png?raw=true "Logo")

## ADP VCSync
This is the beginning of Veracross to ADP Sync using respective API's
and PyQT. The goal is to sync demographic information stored in Veracross
with ADP Payroll. Employees are matched by their Veracross PersonPK stored
in both systems.

PyQT was selected for it's portability between both MacOS and Windows.

## Quick start to development
1) Install Python >= 3.6.5 from Python.org
2) Clone the project using Git or download zip.
3) (Optional) Create a new virtualenv and activate it.
3) While in the repo directory, type: pip install -r requirements
4) (Optional) Switch to the development branch for the latest and greatest: git checkout development
5) To run, type: python main.py
6) Enter your settings on Settings Tab:\
    a) VC API username\
    b) VC API password\
    c) VC API URL (example: https://api.veracross.com/XX/v2)\
    d) ADP network username\
    e) ADP network secret\
    f) Custom Field Name for VC ID in ADP\
    g) Path to certificate signed by ADP\
    h) Path to key for ADP certificate
7) Enter field mappings on the Map Fields tab using JSON format. Each key is a Veracross API field mapped to a
ADP API field.\
`
﻿{'first_name': 'person/legalName/givenName', 
'last_name': 'person/legalName/familyName1',
'address_1': 'person/legalAddress/lineOne',
'city': 'person/legalAddress/cityName',
'state_province': 'person/legalAddress/countrySubdivisionLevel1/shortName',
'postal_code': 'person/legalAddress/postalCode'}
`


![Alt text](screenshots/sync.png?raw=true "Sync Tab")


![Alt text](screenshots/results.png?raw=true "Results Tab")


![Alt text](screenshots/map_fields.png?raw=true "Map Fields Tab")


![Alt text](screenshots/settings.png?raw=true "Settings Tab")


![Alt text](screenshots/debug.png?raw=true "Debug Tab")