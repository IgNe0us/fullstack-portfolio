import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. 데이터 로드 (my_vacuum.pdf)
# 현재 폴더에 있는 님의 이력서 PDF를 로드합니다.
loader = PyMuPDFLoader("manual.pdf")
docs = loader.load()

print(f"✅ PDF에서 {len(docs)}개의 페이지를 로드했습니다.")

# 2. 데이터 쪼개기 (Chunking)
# PDF 내용을 1000자 단위로 쪼개고, 100자씩 겹치게 만듭니다.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

print(f"✅ 문서를 {len(splits)}개의 조각(chunk)으로 나눴습니다.")

# 3. 임베딩 모델 선택 (Ko-SBERT)
# 텍스트를 '숫자 벡터'로 변환할 모델(Ko-SBERT)을 로드합니다.
# (처음 실행 시 모델 파일을 다운로드하느라 시간이 조금 걸릴 수 있습니다.)
model_name = "jhgan/ko-sbert-nli"
model_kwargs = {'device': 'cpu'} # GPU가 있다면 'cuda'로 변경
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

print("✅ 임베딩 모델(Ko-SBERT) 로드 완료.")

# 4. 벡터 스토어 생성 및 저장 (FAISS)
# 쪼갠 문서 조각(splits)들을 모두 '숫자 벡터'로 변환하여
# 'faiss_index_vacuum' 라는 폴더에 DB로 저장합니다.
vectorstore = FAISS.from_documents(splits, embeddings)
vectorstore.save_local("faiss_index_vacuum")

print("🎉 성공: 벡터 스토어(FAISS) 생성 완료! 'faiss_index_vacuum' 폴더를 확인하세요.")