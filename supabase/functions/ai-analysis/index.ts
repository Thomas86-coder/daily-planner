// Supabase Edge Function: ai-analysis
// Receives userMessage, calls Claude API, returns { result }

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const SYSTEM_PROMPT = `
You are a helpful and professional Korean life coach.

If the user message starts with "[2026년 연간 목표 AI 피드백 요청]", you must respond strictly in the following format. Replace the bracketed text with your analysis and specific phrasing:

📋 연간 목표 피드백

📚 자기계발
[입력한 목표 분석 한 줄]
✅ 구체화 제안:
- [구체적 목표 1] (예: 매일 아침 7시 30분 영어 앱 20분)
- [구체적 목표 2]
- [측정 방법]: 어떻게 달성 여부를 확인할지

💜 가족/관계
[입력한 목표 분석 한 줄]
✅ 구체화 제안:
- [구체적 목표 1]
- [구체적 목표 2]
- [측정 방법]

💼 업무/재정
[입력한 목표 분석 한 줄]
✅ 구체화 제안:
- [구체적 목표 1]
- [구체적 목표 2]
- [측정 방법]

🎯 핵심 조언
[세 가지 목표를 연결하는 한 줄 조언]


If the user message does NOT start with "[2026년 연간 목표 AI 피드백 요청]", assume it is a daily reflection. Analyze the user's daily data and respond in Korean with sections for: performance summary, two good points, two areas to improve, two suggestions for tomorrow, and one encouraging message. Use this exact structure in your response: Start with the performance summary section labeled with a chart symbol and the text for today's performance, then a section for two things done well, then a section for two areas that could be improved, then a section for two suggestions for tomorrow, and finally one short encouraging sentence. Each section should be clearly separated. 

Respond entirely in Korean. DO NOT include extra pleasantries outside of these formats.
`;

Deno.serve(async (req: Request): Promise<Response> => {
  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: CORS_HEADERS });
  }

  // Only allow POST
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  try {
    // Parse request body
    const body = await req.json();
    const userMessage: string = body.userMessage ?? "";

    if (!userMessage) {
      return new Response(
        JSON.stringify({ error: "userMessage is required" }),
        {
          status: 400,
          headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
        }
      );
    }

    // Read API key from environment
    const apiKey = Deno.env.get("CLAUDE_API_KEY");
    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "CLAUDE_API_KEY is not configured" }),
        {
          status: 500,
          headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
        }
      );
    }

    // Call Claude API
    const claudeRes = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 800,
        system: SYSTEM_PROMPT,
        messages: [
          {
            role: "user",
            content: userMessage,
          },
        ],
      }),
    });

    if (!claudeRes.ok) {
      const errText = await claudeRes.text();
      console.error("Claude API error:", claudeRes.status, errText);
      return new Response(
        JSON.stringify({
          error: "Claude API request failed",
          status: claudeRes.status,
        }),
        {
          status: 502,
          headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
        }
      );
    }

    const claudeData = await claudeRes.json();
    const result: string = claudeData.content?.[0]?.text ?? "";

    return new Response(JSON.stringify({ result }), {
      status: 200,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("Unhandled error:", message);
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }
});