# [Spider for [bilibili](www.bilibili.com)]

This spider is **only** **for research** **in personal** to gather information of finished animes. 

It can get those details of finished animes,

```python
['title', 'views', 'bullet_comment', 'fans_num','score', 'tags', 'seiyuu', 'av_num']
```

and form a data set called 'bilibili_fin_anime.csv'

### Get the spider

```
$ git clone https://github.com/CristinaZN/-my_spider.git
```

### Environment setup

##### Libraries:

- ​	selenium
- ​	BeautifulSoup
- ​	lxml

```
pip3 install selenium bs4 lxml
```

##### Browser: Chrome + chromedriver

### Instruction

```
python3 spider.py -s <start_page> -e <end_page>
```

### TO DO

- finish  functions:

  ```python
  def download_cover_img(url)
  ```

  The spider cannot gather the cover image, because [bilibili](www.bilibili.com) optimize its page by jQuery.lazyload.

  ```python
  def gen_json(charactor,seiyuu)
  ```

  The charactors and the seiyuu of a anime is now saved as strings in the csv file. 

