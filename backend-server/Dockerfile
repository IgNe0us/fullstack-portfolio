# --- 1단계: 빌드(Build) 스테이지 ---
# Gradle로 Spring Boot 프로젝트를 빌드하기 위한 환경
# 님이 설치한 Java 17 버전에 맞게 'temurin:17' 이미지를 사용합니다.
FROM eclipse-temurin:17-jdk-jammy AS builder

# 작업 폴더 설정
WORKDIR /app

# 1. Gradle 래퍼 파일 복사 (Gradle 설치 없이 빌드 가능)
COPY gradlew .
COPY gradle ./gradle

# 2. 의존성 파일 복사 및 다운로드
# (소스코드 변경 없이 의존성만 변경될 때 캐시를 활용하기 위함)
COPY build.gradle .
COPY settings.gradle .
RUN ./gradlew build --no-daemon || return 0

# 3. 소스 코드 복사 및 빌드
# 나머지 소스 코드를 복사
COPY src ./src
# bootJar 태스크를 실행하여 실행 가능한 .jar 파일을 생성
RUN ./gradlew bootJar

# --- 2단계: 프로덕션(Production) 스테이지 ---
# 실제 서버를 실행하기 위한 최소한의 Java 런타임 환경
FROM eclipse-temurin:17-jre-jammy AS runner

WORKDIR /app

# 1. 빌드 스테이지에서 생성된 .jar 파일만 복사
# 빌드 결과물은 build/libs/ 안에 있습니다.
COPY --from=builder /app/build/libs/*.jar app.jar

# 2. Spring Boot 서버가 8080번 포트를 사용하도록 노출
EXPOSE 8080

# 3. 컨테이너가 시작될 때 실행할 명령어
# 'java -jar app.jar'를 실행하여 Spring Boot 서버를 시작
CMD ["java", "-jar", "app.jar"]