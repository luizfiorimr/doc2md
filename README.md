
```bash
curl -X POST -F "file=@file.xlsx" http://localhost:5000/convert
```

```bash
docker login -u felipefontoura
docker build -t felipefontoura/doc2md .
docker push felipefontoura/doc2md:latest
```
