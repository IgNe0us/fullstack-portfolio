package com.portfolio.backend_server.controller; // controller 패키지 경로

// 방금 만든 ChatService를 import 합니다.
import com.portfolio.backend_server.service.ChatService; 

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class ChatController {

    // ChatService를 주입받습니다.
    private final ChatService chatService;

    // React가 보낼 질문 DTO
    public static class ChatRequest {
        private String question;
        public String getQuestion() { return question; }
        public void setQuestion(String question) { this.question = question; }
    }

    // AI의 답변을 보낼 DTO
    public static class ChatResponse {
        private String answer;
        public ChatResponse(String answer) { this.answer = answer; }
        public String getAnswer() { return answer; }
        public void setAnswer(String answer) { this.answer = answer; }
    }

    // 채팅 API 엔드포인트
    @PostMapping("/chat/rag")
    public Mono<ChatResponse> askRag(@RequestBody ChatRequest request) {
        // Service에게 질문을 넘기고, 답변을 ChatResponse로 변환
        return chatService.getAiResponse(request.getQuestion())
                .map(ChatResponse::new);
    }
}