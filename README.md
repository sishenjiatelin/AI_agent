```
ai_agent
├─  logs
│  └─ day07_llm.logs
├─ README.md
├─ app
│  ├─ __init__.py
│  ├─ clients
│  │  ├─ __init__.py
│  │  └─ llm_client.py
│  ├─ core
│  │  ├─ __init__.py
│  │  └─ config.py
│  ├─ job_parser_core.py
│  ├─ main.py
│  ├─ schemas
│  │  ├─ __init__.py
│  │  └─ job.py
│  └─ utils
│     ├─ __init__.py
│     ├─ io.py
│     └─ logger.py
├─ data
│  ├─ day02_result.json
│  ├─ day05_validated_jobs.json
│  ├─ extracted_job_example.json
│  ├─ jobs.csv
│  ├─ jobs.json
│  ├─ parsed_job.json
│  └─ sample_job.txt
├─ docs
│  ├─ day09_health_response.json
│  ├─ day09_parse_response.json
│  └─ screenshots
│     ├─ day09_health.png
│     └─ day09_jobs_parse.png
├─ logs
│  ├─ day01.log
│  ├─ day03.log
│  ├─ day05_validate.log
│  ├─ day06_parse.log
│  ├─ day08_cli.log
│  └─ day09_api.log
├─ main.py
├─ pytest.ini
├─ requirements.txt
├─ scripts
│  ├─ day02_text_tools.py
│  ├─ day03_load_jobs.py
│  ├─ extract_job_with_llm.py
│  ├─ job_parser_cli.py
│  └─ validate_jobs.py
└─ tests
   ├─ test_day09_api.py
   ├─ test_io.py
   ├─ test_job_parser_cli.py
   ├─ test_job_parser_core.py
   └─ test_llm_client.py

```