# Content Aggregator
This application is mainly built on top of  [Build a Content Aggregator in Python](https://realpython.com/build-a-content-aggregator-python/ "Build a Content Aggregator in Python") by Real Python but witth additional features and deployed on Heroku.

## Additional Features
- User accounts that support registration/login
- Can subscribe to the interested feeds (now only got 5 topics which are Python, Data Science, Machine Learning, Frontend, Backend)
- Can like the content and added into favorite list

## How to use
Before you run the application, you have to make the code inside podcasts/forms.py be like this:
```python
# queryset_genre = Category.objects.all()
# GENRES_CHOICES = [(obj.id, obj.title) for obj in queryset_genre]
# uncomment the following line
GENRES_CHOICES = [
    (1,'Python'),
    (3,'Backend'),
    (4,'Frontend'),
    (5,'Data Science'),
    (6,'Machine Learning'),
]
```
Then u can run `python manage.py makemigrations` and `python manage.py migrate` then `python manage.py runserver`.
Now you can add the categories that you want inside the admin panel and change the podcasts/forms.py like below:

    queryset_genre = Category.objects.all()
    GENRES_CHOICES = [(obj.id, obj.title) for obj in queryset_genre]
    # GENRES_CHOICES = [
    #     (1,'Python'),
    #     (3,'Backend'),
    #     (4,'Frontend'),
    #     (5,'Data Science'),
    #     (6,'Machine Learning'),
    # ]
And now should be okay to go!
