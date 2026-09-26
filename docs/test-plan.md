# Testing Strategy

| ID | Scenario | Input | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|
| T01 | Student registration | valid student data | 201 + token | Fill during run | |
| T02 | Teacher login | valid teacher credentials | 200 | Fill during run | |
| T03 | Invalid login | wrong password | 401 | Fill during run | |
| T04 | Student dashboard authorization | student token -> teacher-only action | 403 | Fill during run | |
| T05 | Teacher dashboard authorization | teacher token -> student submission action | 403 | Fill during run | |
| T06 | Teacher creates assignment | valid assignment | 201 | Fill during run | |
| T07 | Student views assignment | authenticated GET | 200 | Fill during run | |
| T08 | Valid PDF upload | PDF under size limit | submission created | Fill during run | |
| T09 | Invalid extension | `.exe` | 400 | Fill during run | |
| T10 | Oversized file | above configured MB | 413 | Fill during run | |
| T11 | On-time submission | current time <= deadline | SUBMITTED | Fill during run | |
| T12 | Late submission | current time > deadline | LATE or rejected | Fill during run | |
| T13 | Resubmission | second upload before grading | existing record updated | Fill during run | |
| T14 | Own submission | student requests own record | 200 | Fill during run | |
| T15 | Other student's submission | student requests another ID | 403 | Fill during run | |
| T16 | Teacher submissions | teacher owns assignment | 200 | Fill during run | |
| T17 | Grade submission | marks within max | GRADED | Fill during run | |
| T18 | Excess marks | marks > max | 400 | Fill during run | |
| T19 | Student feedback | own graded submission | feedback visible | Fill during run | |
| T20 | Unauthorized grading | student grade endpoint | 403 | Fill during run | |
| T21 | File retrieval | authorized download | file returned | Fill during run | |
| T22 | Storage failure | unavailable bucket/service | controlled error | Fill during run | |
| T23 | Database failure | unavailable DB | controlled 5xx | Fill during run | |
| T24 | Logout | remove local token | subsequent protected call fails | Fill during run | |
| T25 | Protected route after logout | no token | 401 | Fill during run | |

## Automated tests
`tests/test_api.py` covers the health endpoint and registration/login. Extend it with endpoint-level tests for every table row before a production-style deployment.
