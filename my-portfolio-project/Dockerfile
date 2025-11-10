# --- 1단계: 베이스 이미지 ---
# 님이 사용한 Python 3.11 버전에 맞게 slim(경량) 버전을 사용
FROM python:3.11-slim

# 작업 폴더 설정
WORKDIR /app

# 1. 의존성 설치
# requirements.txt 파일을 먼저 복사
COPY requirements.txt .
# pip를 업그레이드하고 requirements.txt에 있는 모든 라이브러리를 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2. 소스 코드 복사
# (이때 .dockerignore가 적용되어 venv 등은 복사되지 않음)
COPY . .

# 3. PDF 데이터 복사
# 빌드 시점에 PDF 파일이 컨테이너 안에 포함되어 있어야 함
# (만약 파일 이름이 다르다면 여기서 수정)
COPY manual.pdf .

# 4. 서버가 8000번 포트를 사용하도록 노출
EXPOSE 8000

# 5. 컨테이너가 시작될 때 실행할 명령어
# (주의!) CMD가 2개입니다.
# 첫 번째: rag_builder.py를 실행해서 'faiss_index_vacuum' DB를 생성
# 두 번째: uvicorn 서버를 실행
# (Ollama 서버가 외부(host)에 떠있다고 가정하고 0.0.0.0으로 바인딩)
CMD sh -c "python rag_builder.py && uvicorn main:app --host 0.0.0.0 --port 8000"