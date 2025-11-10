// src/app/api/chat/route.ts

import { NextRequest, NextResponse } from "next/server";

// React(page.tsx)가 보낸 /api/chat POST 요청을 받습니다.
export async function POST(request: NextRequest) {
  try {
    // 1. React가 보낸 JSON { "question": "..." }을 받음
    const body = await request.json();
    const question = body.question;
    const backendUrl = process.env.SPRING_BOOT_URL || "http://127.0.0.1:8080";

    // 2. 이 요청을 Spring Boot 서버 (http://127.0.0.1:8080)로 대신 전달
    const springResponse = await fetch(
      `${backendUrl}/api/chat/rag`, // [Phase 2] Spring Boot 서버 주소
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: question }), // 받은 그대로 전달
      }
    );

    if (!springResponse.ok) {
      throw new Error("Spring Boot 서버 응답 오류");
    }

    // 3. Spring Boot의 답변 { "answer": "..." }을 받음
    const data = await springResponse.json();

    // 4. 이 답변을 다시 React(page.tsx)에게 전달
    return NextResponse.json(data);
  } catch (error) {
    console.error("API Route 핸들러 오류:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}