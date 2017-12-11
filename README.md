## Ring Test Task

### How to start application

Have pip and python >= 3.6 installed

```
pip install -r requirements.txt
python app.py
```

### Main idea

Once map of the city is submitted, compute Floyd–Warshall algorithm in order to save 'intermediary' matrix which would allow us to compute routes between any two nodes in the city with ease.

SQLite was chosen as a simple persistence mechanism.


### Estimated complexity

City creation - O(n^3) where n - amount of nodes in the city

Route search - O(m * log(n)) where m - number of cameras that have detected thief, n - amount of nodes (although, I am not sure)


### What could be improved

* Tests
* Validation
* Caching

In real-world app it would also be usefull to analyzae how many city creation and how many route search requests are made. This would help us to understand how our application is used. Once we do this we might want to tweak something, e.g. while preparing this solution I was assuming that find-route requests would be much more frequent than create-city requests.
