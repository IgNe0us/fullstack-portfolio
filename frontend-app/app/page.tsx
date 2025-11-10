// "use client"는 이 파일이 서버가 아닌, 사용자 브라우저(클라이언트)에서
// 동작하는 React 컴포넌트임을 Next.js에게 알려줍니다. (useState 사용 시 필수)
"use client";

import { useState } from "react";

// React의 '상태(State)'로 채팅 메시지를 관리합니다.
// { role: "user" | "assistant", content: string }
interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  // 채팅 메시지 목록을 저장할 상태
  const [messages, setMessages] = useState<Message[]>([]);
  // 사용자가 입력 중인 메시지를 저장할 상태
  const [input, setInput] = useState("");
  // AI가 답변 중인지 여부를 저장할 상태 (로딩 표시용)
  const [isLoading, setIsLoading] = useState(false);

  // 전송 버튼을 누르거나 Enter를 쳤을 때 호출될 함수
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // 폼 전송 시 페이지가 새로고침되는 것을 막음
    if (!input.trim()) return; // 빈 메시지는 전송 안 함

    const userInput: Message = { role: "user", content: input };
    // 사용자의 메시지를 채팅 목록에 추가
    setMessages((prev) => [...prev, userInput]);
    setInput(""); // 입력창 비우기
    setIsLoading(true); // 로딩 시작

    try {
      // --- [매우 중요] Spring Boot 서버와 통신 ---
      // React(Next.js)는 3000번 포트, Spring Boot는 8080번 포트입니다.
      // 포트가 달라서 'CORS' 에러가 발생하므로, Next.js의 'Route Handler'를 이용해 우회합니다.
      // (이 설정은 3단계에서 합니다)
      // 지금은 우선 '/api/chat'이라는 주소로 요청을 보냅니다.
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // Spring Boot가 받을 형식: { "question": "..." }
        body: JSON.stringify({
          question: input,
        }),
      });

      if (!response.ok) {
        throw new Error("Spring Boot 서버에서 오류가 발생했습니다.");
      }

      // Spring Boot가 보낸 형식: { "answer": "..." }
      const data = await response.json();

      // AI의 답변을 채팅 목록에 추가
      const aiResponse: Message = { role: "assistant", content: data.answer };
      setMessages((prev) => [...prev, aiResponse]);
    } catch (error) {
      console.error(error);
      const errorResponse: Message = {
        role: "assistant",
        content: "죄송합니다. 답변을 가져오는 중 오류가 발생했습니다.",
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false); // 로딩 끝
    }
  };

  // --- UI (Tailwind CSS로 스타일링) ---
  return (
    <div className="flex flex-col w-full max-w-2xl mx-auto h-screen bg-white">
      {/* 채팅 메시지 영역 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-3 rounded-lg ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-black"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {/* 로딩 중일 때 '...' 표시 */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="p-3 rounded-lg bg-gray-200 text-black">...</div>
          </div>
        )}
      </div>

      {/* 하단 입력창 영역 */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="청소기 설명서에 대해 질문해보세요..."
            className="flex-1 p-2 border rounded-lg text-black"
          />
          <button
            type="submit"
            className="p-2 bg-blue-500 text-white rounded-lg"
            disabled={isLoading} // 로딩 중일 때 버튼 비활성화
          >
            전송
          </button>
        </div>
      </form>
    </div>
  );
}