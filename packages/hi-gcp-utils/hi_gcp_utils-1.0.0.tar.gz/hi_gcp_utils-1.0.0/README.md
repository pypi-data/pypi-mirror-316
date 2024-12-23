# GCP Utils

A Python package for interacting with Google BigQuery, providing easy-to-use utilities for data operations.

## Installation

```bash
pip install hi-gcp-utils
```

## Usage

```python
from gcp_utils import BigQueryClient

# Initialize the client
client = BigQueryClient(
    project_id="your-project-id",
    dataset_id="your-dataset-id"
)

# Set your credentials
client.set_key_file("path/to/your/credentials.json")

# Example: Query data
df = client.sql2df("SELECT * FROM your_table LIMIT 10")
```

## Features

- Easy BigQuery table operations
- DataFrame integration with pandas
- Secure credential management
- Table schema modifications
- Data transfer utilities

## Requirements

- Python >= 3.6
- google-cloud-bigquery
- google-cloud-storage
- pandas
- pandas-gbq
- pyarrow

## License

This project is licensed under the MIT License.
