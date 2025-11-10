import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_ollama.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# --- (앱 시작 시 1회 실행) 모델 및 벡터DB 로드 ---
print("서버 시작... AI 모델 및 벡터DB 로드 중...")

# 1. 임베딩 모델 로드
model_name = "jhgan/ko-sbert-nli"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# 2. 로컬에 저장된 벡터DB 로드
vectorstore = FAISS.load_local(
    "faiss_index_vacuum", 
    embeddings,
    allow_dangerous_deserialization=True 
)

# 3. LLM (답변 생성 모델) 로드
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

print(f"Ollama 서버에 연결 시도: {OLLAMA_BASE_URL}") # 로그 추가

llm = ChatOllama(
    base_url=OLLAMA_BASE_URL, # [수정 2] base_url 지정
    model="qwen2:7b", 
    temperature=0
)

# 4. 검색기(Retriever) 정의
# 이력서 DB에서 질문과 유사한 문서를 3개 찾아오도록 설정
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. 프롬프트 템플릿 정의 (LCEL 방식)
# AI에게 "맥락(context)"과 "질문(question)"을 어떻게 전달할지 정의
template = """
당신은 'LG 싸이킹청소기 사용설명서'를 바탕으로 질문에 답변하는 A/S 봇이야.
제공된 '맥락(Context)'을 바탕으로만 답변해야 합니다. 맥락에 없는 내용은 절대 지어내지 말고, "사용설명서에 해당 내용이 없습니다."라고 답변하세요.

Context:
{context}

Question:
{question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

# 6. RAG 체인 생성 (LCEL 방식)
# 이것이 바로 'langchain.chains'를 사용하지 않는 새로운 방식입니다.
# 파이프(|) 연산자로 각 단계를 연결합니다.
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("✅ AI 모델 및 벡터DB 로드 완료. (LCEL 방식) API 서버 준비 완료.")
# --- (여기까지 앱 시작 시 1회 실행) ---


# FastAPI 앱 생성
app = FastAPI()

# 사용자가 질문할 때 사용할 데이터 형식(Schema) 정의
class Query(BaseModel):
    question: str

# API 엔드포인트 생성
@app.post("/chat/rag")
def ask_rag(query: Query):
    """
    RAG 챗봇에게 질문하는 API 엔드포인트
    """
    print(f"질문 수신: {query.question}")
    
    # 6단계에서 만든 새 RAG 체인을 실행 (입력값이 query.question 문자열 자체)
    result = rag_chain.invoke(query.question)
    
    print(f"답변 생성: {result}")
    return {"answer": result}