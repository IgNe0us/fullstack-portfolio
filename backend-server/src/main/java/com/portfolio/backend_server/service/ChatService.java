package com.portfolio.backend_server.service; // service 패키지 경로

import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

// DTO를 ChatController에서 가져옵니다.
import com.portfolio.backend_server.controller.ChatController.ChatRequest;
import com.portfolio.backend_server.controller.ChatController.ChatResponse;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;
import org.springframework.beans.factory.annotation.Value;

@Service
@RequiredArgsConstructor
public class ChatService {

    private final WebClient webClient;
    
    @Value("${ai.server.url}")
    private String aiServerUrl;

    public Mono<String> getAiResponse(String question) {
        ChatRequest aiRequest = new ChatRequest();
        aiRequest.setQuestion(question);

        return webClient.post()
                .uri(aiServerUrl + "/chat/rag") // Python 서버 주소
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(aiRequest)
                .retrieve()
                .bodyToMono(ChatResponse.class) // 받은 JSON을 ChatResponse 객체로 변환
                .map(ChatResponse::getAnswer); // 'answer' 필드만 추출
    }
}