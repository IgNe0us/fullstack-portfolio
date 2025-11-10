# --- 1단계: 빌드(Build) 스테이지 ---
# 님의 로컬 버전과 동일한 'node:24.11.0-alpine'을 사용합니다.
FROM node:24.11.0-alpine AS builder

# 작업 폴더 설정
WORKDIR /app

# 1. 의존성 설치
# package.json과 package-lock.json을 먼저 복사
COPY package*.json ./
# npm ci는 package-lock.json을 기반으로 더 빠르고 일관되게 설치합니다.
RUN npm ci

# 2. 소스 코드 복사 및 빌드
# 나머지 소스 코드를 복사 (이때 .dockerignore가 적용됨)
COPY . .
# next.config.mjs의 'output: standalone' 설정에 따라
# .next/standalone 폴더에 최적화된 결과물이 생성됨
RUN npm run build

# --- 2단계: 프로덕션(Production) 스테이지 ---
# 실제 서버를 실행할 환경도 'node:24.11.0-alpine'으로 통일합니다.
FROM node:24.11.0-alpine AS runner

WORKDIR /app

# 프로덕션 환경임을 명시
ENV NODE_ENV production

# 1. 빌드 스테이지에서 생성된 '독립 실행' 파일들을 복사
# .next/standalone 폴더는 필요한 node_modules와 server.js를 포함합니다.
COPY --from=builder /app/.next/standalone ./

# 2. public 폴더와 .next/static(이미지, CSS) 폴더 복사
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static

# 3. Next.js 서버가 3000번 포트를 사용하도록 노출
EXPOSE 3000

# 4. 컨테이너가 시작될 때 실행할 명령어
# 'node server.js'를 실행하여 Next.js 서버를 시작합니다.
CMD ["node", "server.js"]