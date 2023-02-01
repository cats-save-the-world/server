# server

## Run
```
docker-compose up
```

## Apply migrations
```
docker-compose run server aerich upgrade
```

## Check code-style
```
docker-compose run server flake8 .
```

## Check types
```
docker-compose run server mypy .
```

## Run tests
```
docker-compose run server pytest
```
