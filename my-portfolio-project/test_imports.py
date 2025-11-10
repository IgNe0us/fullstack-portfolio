print("스크립트 시작...")
import os
print("os 임포트 완료")

from langchain_community.document_loaders import PyPDFLoader
print("PyPDFLoader 임포트 완료")

# [이전 코드] from langchain.text_splitter import RecursiveCharacterTextSplitter
# [수정!] 이사 간 새 주소로 변경합니다.
from langchain_text_splitters import RecursiveCharacterTextSplitter
print("TextSplitter 임포트 완료")

from langchain_community.vectorstores import FAISS
print("FAISS 임포트 완료")

# 여기가 모델 다운로드 때문에 오래 걸렸던 부분입니다.
print("HuggingFaceEmbeddings 임포트 시도...")
from langchain_community.embeddings import HuggingFaceEmbeddings
print("HuggingFaceEmbeddings 임포트 완료!")

print("--- 모든 임포트 성공! ---")