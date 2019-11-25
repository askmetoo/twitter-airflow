### How to start 

* Set locale (otherwise airflow will  fail with 'ValueError('unknown locale: %s' % localename" 
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

* fill variables.py with your values
* run airflow:
```
airflow initdb           
airflow webserver      
airflow scheduler        
```

### DAGs
twitter_model: will train model, should as a first one
twitter_sentiment: will download tweets daily, calculate sentiment and data-mart

### Hint
sentiment and data-mart are calculated for all available tweets so in case of model improvements historical data can change  
