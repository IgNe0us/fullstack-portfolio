import sys
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. 임베딩 모델 로드 (main.py와 동일)
print("임베딩 모델(Ko-SBERT) 로드 중...")
model_name = "jhgan/ko-sbert-nli"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
print("✅ 임베딩 모델 로드 완료.")

# 2. 로컬에 저장된 '청소기 DB' 로드
try:
    vectorstore = FAISS.load_local(
        "faiss_index_vacuum", 
        embeddings,
        allow_dangerous_deserialization=True 
    )
    print("✅ 'faiss_index_vacuum' DB 로드 완료.")
except Exception as e:
    print(f"❌ DB 로드 실패: {e}")
    print("'faiss_index_vacuum' 폴더가 있는지, rag_builder.py를 올바르게 실행했는지 확인하세요.")
    sys.exit() # 프로그램 종료

# 3. 검색기(Retriever) 정의
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # 3개 검색

# 4. 테스트 질문
question = "안전을 위한 주의사항 알려줘"
print(f"\n--- [테스트 질문] --- \n{question}")

# 5. DB에서 유사 문서 검색
# AI가 답변하기 직전에 보는 'Context'를 여기서 확인합니다.
docs = retriever.invoke(question)

print("\n--- [DB 검색 결과 (Context)] ---")
if not docs:
    print("!! 검색 결과 없음 !! (DB가 비어있거나, 관련 내용이 전혀 없습니다)")
else:
    for i, doc in enumerate(docs):
        print(f"\n[검색된 문서 조각 #{i+1}]")
        print(doc.page_content) # 검색된 문서 조각의 내용을 출력
        print("---")