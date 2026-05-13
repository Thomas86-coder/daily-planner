// Supabase Edge Function: ai-analysis
// Receives userMessage, calls Claude API, returns { result }

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req: Request): Promise<Response> => {
  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: CORS_HEADERS });
  }

  try {
    // Parse request body
    const body = await req.json();
    const userMessage: string = body.userMessage ?? "";
    const responseType: string = body.responseType ?? "";

    if (!userMessage) {
      return new Response(
        JSON.stringify({ error: "userMessage is required" }),
        { status: 400, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    // Read API key from environment
    const apiKey = Deno.env.get("CLAUDE_API_KEY");
    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "CLAUDE_API_KEY is not configured" }),
        { status: 500, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    const maxTokens: number = body.max_tokens ?? 1500;

    // responseType에 따라 시스템 프롬프트 분기
    let systemPrompt = "";

    if (responseType === "annualGoalFeedback") {
      systemPrompt = "You are a Korean life coach. Analyze the annual goals and provide specific suggestions. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"selfDev\":[\"suggestion1\",\"suggestion2\"],\"family\":[\"suggestion1\",\"suggestion2\"],\"work\":[\"suggestion1\",\"suggestion2\"]}";
    } else if (responseType === "monthlyPlan") {
      systemPrompt = "You are a Korean life coach. Suggest monthly action plans based on annual goals. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"selfDev\":\"monthly plan content\",\"family\":\"monthly plan content\",\"work\":\"monthly plan content\"}";
    } else {
      // 기존 일일 분석 프롬프트 유지
      systemPrompt = "You are a Korean productivity coach. Always respond in Korean with this exact format: [오늘의 성과] completion rate summary [잘한 점] 1. 2. [아쉬운 점] 1. 2. [내일 개선 제안] 1. 2. [응원 한마디] one encouraging sentence";
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
        max_tokens: maxTokens,
        system: systemPrompt,
        messages: [{ role: "user", content: userMessage }],
      }),
    });

    if (!claudeRes.ok) {
      const errText = await claudeRes.text();
      console.error("Claude API error:", claudeRes.status, errText);
      return new Response(
        JSON.stringify({ error: "Claude API request failed", status: claudeRes.status }),
        { status: 502, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    const claudeData = await claudeRes.json();
    const result: string = claudeData.content?.[0]?.text ?? "오류가 발생했어요";

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