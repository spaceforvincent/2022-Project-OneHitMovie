# pull 받고 제일 먼저 해야할 일

```bash
$ source venv/scripts/activate

$ python manage.py migrate
```



# 데이터베이스로 로드

model을 확장한 경우, 확장된 데이터를 지우고 load.



```bash
$ python manage.py loaddata users.json advertisements.json advertisementcomments.json moviecomments.json movies.json
```



# 작업 중 새로운 데이터 추가했을 경우(중요)



- accounts의 user 모델에 새로운 데이터 추가했을 경우

```bash
$ python -Xutf8 manage.py dumpdata --indent 4 accounts.user > users.json
```

- community의 advertisement 모델에 새로운 데이터 추가했을 경우

```bash
$ python -Xutf8 manage.py dumpdata --indent 4 community.advertisement > advertisements.json
```

- community의 advertisementcomment 모델에 새로운 데이터 추가했을 경우

```bash
$ python -Xutf8 manage.py dumpdata --indent 4 community.advertisementcomment > advertisementcomments.json
```

- movies의 moviecomments 모델에 새로운 데이터 추가했을 경우

```bash
$ python -Xutf8 manage.py dumpdata --indent 4 movies.moviecomment > moviecomments.json
```

- movies의 movie 모델에 새로운 데이터 추가했을 경우

```bash
$ python -Xutf8 manage.py dumpdata --indent 4 movies.movie > movies.json
```