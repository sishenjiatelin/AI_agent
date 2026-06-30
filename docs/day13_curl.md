## 1. 启动服务
   uvicorn app.main:app --reload
## 2. 上传 txt 文件
  curl -X POST "http://127.0.0.1:8000/documents/upload" \
  -F "file=@data/sample_job.txt"
## 3. 查看资料列表
  curl "http://127.0.0.1:8000/documents"
## 4. 读取资料内容
  curl "http://127.0.0.1:8000/documents/1/content"
## 5. 非法后缀测试
  echo "bad file" > data/bad.exe
  curl -X POST "http://127.0.0.1:8000/documents/upload" \
  -F "file=@data/bad.exe"