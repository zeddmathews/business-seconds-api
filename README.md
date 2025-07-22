# recomed-backend-python-assessment
An API endpoint to calculate the total number of business seconds between two given times.  

## Usage
- http://localhost:8000/business_seconds?start_time=2025-07-22T08:00:00&end_time=2025-07-22T12:00:00

## Requirements
- The endpoint must support only/list GET requests and must take two parameters.
- Parameters are start_time and end_time.
- Parameter values will be in ISO-8601 format.
- Successful request: return a single integer value.
- Failed requests: suitable error message.
- Write a script for automated deployment.
- Include automated testing.

### Notes
- start_time is guaranteed to be before end_time.
- Do not use any packages to calculate/derive business seconds and/or holidays.
- **Create the database before attempting to spin up the server. Docker depends on the database to be up and running but does NOT create it for you**

## Key
**Business seconds:**: Defined as any whole second that elapses between the hours of `08:00` and `17:00` during a work week (Monday - Friday), exluding public holidays in the Republic of South Africa.<br/>
**ISO-8601 format**:
- International standard for date-time formats.
- (YYYY-MM-DD, hh-mm-ss)
- YYYY = Year
- MM = Month (01-12)
- DD = Day (01-31)
- hh = Hour (between 00-24)
- mm = Minute (between 00-59)
- ss = Second (between 00 and 60, where 60 is only used to denote an added leap second)
