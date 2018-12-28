# LinkedIn Scraping

This is an automative scraping&profiling tools for given urls

## Files Layout

```
html/ 				source profile in html format
login/				util function for login

profile*/			cookies for each profile	
url.json			Target url list
parse.json			Result in json format
...
```



## Usage

#### Scrape profile webpage 

```shell
$ python scrape_profile.py -h
usage: scrape_profile.py [-h] name start end

positional arguments:
  name        an integer for the accumulator
  start       The start index in url.json
  end         The end index in url.json

optional arguments:
  -h, --help  show this help message and exit
```



#### Parse the html file

```shell
python scrape_profile.py
```

