# 베이스 이미지 선택
FROM python:3.10.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .

# 필요한 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["python", "app.py"]
