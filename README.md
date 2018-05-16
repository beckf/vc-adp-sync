![Alt text](screenshots/adp-vc-logo.png?raw=true "Logo")

## ADP VCSync
This is the beginning of Veracross to ADP Sync using PyQT.

PyQT was selected for it's portability between MacOS and Windows.

## Quick start to development
1) Install Python 3.6.5 from Python.org
2) Clone the project using Git or download zip.
3) While in the repo directory from GitHub, type: pip install -r requirements
4) Optional: Switch to the development branch for the latest and greatest.
5) To run, type: python main.py
6) Enter your settings on Settings Tab:\
    a) VC API Username\
    b) VC API Password\
    c) VC API URL (example: https://api.veracross.com/XX/v2)
7) Enter field mappings on the Map Fields tab using JSON format\
`{\
"employee_number": "adp_emp_num",\
"last_name": "adp_last_name",\
"first_name": "adp_first_name",\
"nick_name": "adp_nick_name",\
"middle_name": "adp_middle_name",\
"mobile_phone": "adp_mobile_phone",\
"home_phone": "adp_home_phone",\
"work_phone": "adp_work_phone",\
"email_1": "adp_email_1",\
"address_1": "adp_address_1",\
"address_2": "adp_address_2",\
"city": "adp_city",\
"state_province": "adp_state",\
"postal_code": "adp_postal"\
}`


![Alt text](screenshots/sync.png?raw=true "Sync Tab")


![Alt text](screenshots/settings.png?raw=true "Settings Tab")


![Alt text](screenshots/debug.png?raw=true "Debug Tab")