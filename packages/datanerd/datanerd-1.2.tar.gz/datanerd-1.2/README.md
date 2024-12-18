# DataNerd

This package provides various functions for data analysis, statistical calculations, database operations, and sending notifications.

## Installation

To use these functions, you need to have Python installed on your system. You also need to install the required libraries. You can install them using pip:

```
pip install pandas numpy sqlalchemy requests
```

## Functions

### 1. stats()

This function provides statistical summary of a given dataframe.

#### Parameters:
- `df` (pandas.DataFrame): The input dataframe

#### Returns:
- A dataframe containing various statistics for each column

#### Statistics provided:
- count
- mean
- std
- min
- 10th, 20th, 25th, 30th, 40th, 50th (median), 60th, 70th, 75th, 80th, 90th, 95th, 99th percentiles
- max
- % of missing values
- number of unique values

#### Usage:

```python
import pandas as pd
import datanerd as dn

df = pd.read_csv('titanic.csv')
summary_stats = dn.stats(df)
```

### 2. iv_woe()

This function calculates the Weight of Evidence (WoE) and Information Value (IV) for a given dataframe.

#### Parameters:
- `data` (pandas.DataFrame): The input dataframe
- `target` (str): The name of the target variable
- `bins` (int): The number of bins to use for discretizing continuous variables
- `optimize` (bool): Whether to optimize the binning of continuous variables
- `threshold` (float): The minimum percentage of non-events in each bin for optimization

#### Returns:
- A tuple containing two dataframes: (iv, woe)

#### Usage:

```python
import pandas as pd
import datanerd as dn

df = pd.read_csv('cancer.csv')
iv, woe = dn.iv_woe(data=df, target='Diagnosis', bins=20, optimize=True, threshold=0.05)
```

### 3. pushdb()

This function pushes a Pandas dataframe to a Microsoft SQL Server database.

#### Parameters:
- `data` (pandas.DataFrame): The dataframe to be pushed
- `tablename` (str): The name of the table in the database
- `server` (str): The name of the SQL Server
- `database` (str): The name of the database
- `schema` (str): The name of the schema

#### Usage:

```python
import pandas as pd
import datanerd as dn

df = pd.read_csv('day.csv')
dn.pushdb(df, tablename='day', server='SQL', database='schedule', schema='analysis')
```

### 4. teams_webhook()

This function sends a formatted message to a Microsoft Teams channel using a webhook URL.

#### Parameters:
- `webhook_url` (str): The webhook URL for the Teams channel
- `title` (str): The title of the message
- `message` (str): The body of the message

#### Usage:

```python
import datanerd as dn

webhook_url = "https://outlook.office.com/webhook/..."
title = "Important Notification"
message = "This is a test message sent from Python!"

dn.teams_webhook(webhook_url, title, message)
```

### 5. ntfy()

This function sends a notification message to an ntfy.sh server.

#### Parameters:
- `server` (str): The name of the ntfy.sh server/topic to send the message to
- `message` (str): The message to be sent


#### Usage:

```python
import datanerd as dn

server = "your_server_name"
message = "This is a test notification from Python!"

dn.ntfy(server, message)
```



