## :camera: Dumpr

Bulk download all of your Flickr images.

### Why?

Flickr's data download service does not preserve albums or filenames. If you have thousands of images curated in albums, you'll probably want to preserve that structure. Flickr provides multiple zip files, roughly one per 500 photos, containing your photos, *unordered* and named in this nondescript format: 

```
50011347486_7c1402ece1_o.jpg

{server-id}/{id}_{o-secret}_o.{o-format}
```

### Config

You must set the variables in auth.py.
```
user_id = ''
api_key = ''
api_secret = ''
access_token = ''
url_extension = 'username/albums/'
```

### Usage
```
python3 download.py
```
