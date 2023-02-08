# COVID19 Data Analysis

Collect and preprocess COVID data from [WorldOMeter](https://www.worldometers.info/coronavirus)

## Deployment guide

1. Setup environment

```
pip install -r requirements.txt
```

2. Crawl data

```
python crawl.py \
    --save_dir=[Directory to save data] \
    --country_path=[Path to file text contains all country names]
```

3. Preprocess data

```
python preprocess.py \
    --data_dir=[Path to data directory] \
    --save_path=[Path to save preprocessed file]
```
