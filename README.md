
# Threat Intelligence ETL Pipeline

## How to Run

### 1. Clone the Repository



cd threatIntelligenceETLPipeline101

2. Create Virtual Environment


Windows:

```
python -m venv .venv

.venv\Scripts\activate
```

Mac/Linux:

```
python3 -m venv .venv

source .venv/bin/activate
```

3. Install Dependencies
python -m pip install -r requirements.txt

4. Check Available Options
python main.py --help

6. Check Version
python main.py --version

8. Run the ETL Pipeline
python main.py

Pipeline:

Extract → Transform → Enrich → Load


7. Run Tests

```
python -m pytest -v
```


8. Run with Docker

Build the image:
```
docker compose build
```

Run the pipeline:

```
docker compose up
```

View logs:

```
docker compose logs -f
```

Stop the container:

```
docker compose down
```


9. Logs
Logs are printed in the terminal and saved to:

logs/pipeline.log

10. Output

SQLite database:

data/threat_intelligence.db

Downloaded URLHaus data:

data/raw/urlhaus.csv
