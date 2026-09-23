// ⚠️ 이 파일은 참고용입니다. 자동 배포되지 않습니다.
// Supabase 대시보드(daily-planner 프로젝트, ref qxqkpgkiuzdvkdieqynf)
//   > Edge Functions > ai-analysis > Code 에서
//   이 파일 내용으로 index.ts를 교체하고 "Deploy updates"를 눌러 수동 배포하세요.
//
// 변경 범위: weeklyReview / dailyAnalysis / monthlyOneThingSuggest 3개 분기의 systemPrompt만 개선.
// 나머지 분기(annualGoalFeedback, monthlyPlan, monthlyResult, learningAnalysis, else)와
// 요청/응답 처리 로직, 모델, 스키마는 배포본과 동일하게 유지했습니다.
//
// 작성일: 2026-09-23

// Supabase Edge Function: ai-analysis
// Receives userMessage, calls Claude API, returns { result }

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req: Request): Promise<Response> => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: CORS_HEADERS });
  }

  try {
    const body = await req.json();
    const userMessage: string = body.userMessage ?? "";
    const responseType: string = body.responseType ?? "";

    if (!userMessage) {
      return new Response(
        JSON.stringify({ error: "userMessage is required" }),
        { status: 400, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    const apiKey = Deno.env.get("CLAUDE_API_KEY");
    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "CLAUDE_API_KEY is not configured" }),
        { status: 500, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    const maxTokens: number = body.max_tokens ?? 1500;

    let systemPrompt = "";

    if (responseType === "annualGoalFeedback") {
      systemPrompt = "You are a Korean life coach. Analyze the annual goals and provide specific suggestions. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"selfDev\":[\"suggestion1\",\"suggestion2\"],\"family\":[\"suggestion1\",\"suggestion2\"],\"work\":[\"suggestion1\",\"suggestion2\"]}";
    } else if (responseType === "monthlyPlan") {
      systemPrompt = "You are a Korean life coach. Suggest monthly action plans based on annual goals. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"selfDev\":\"monthly plan content\",\"family\":\"monthly plan content\",\"work\":\"monthly plan content\"}";
    } else if (responseType === "monthlyOneThingSuggest") {
      // ── [개선] 4개 영역을 모두 채우지 않고, 이번 달 최우선 영역 1개만 값을 채우고 나머지 3개는 빈 문자열 반환 ──
      systemPrompt = "You are a Korean life coach specializing in the ONE Thing methodology. The user provides their annual ONE Things for four life areas with keys: work, job, growth, personal. The core principle of ONE Thing is to concentrate on the single most important thing rather than spreading effort across many. Your job: examine all four annual ONE Things and pick EXACTLY ONE area to prioritize THIS month — the area where making progress right now is most urgent, most time-sensitive, or would have the greatest ripple effect (leverage) on the user's overall goals. For that ONE chosen area, propose a single monthly ONE Thing that, if achieved this month, would most move its annual goal forward: one concrete, measurable, actionable Korean sentence. Fill ONLY the chosen area's key with that sentence, and return an EMPTY STRING (\"\") for the other three keys. When choosing, ignore any area whose annual input is empty or missing. Do NOT fill more than one key. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"work\":\"...\",\"job\":\"...\",\"growth\":\"...\",\"personal\":\"...\"} — exactly one value is a non-empty sentence and the other three are empty strings.";
    } else if (responseType === "weeklyReview") {
      // ── [개선] 자유 산문 형식은 유지하되, 마지막 1~2문장에서 "다음 주 ONE Thing 1개"로 명확히 좁혀 결론 ──
      systemPrompt = "You are a Korean productivity coach. Based on the user's weekly data, write a natural Korean weekly retrospective as free-flowing prose. Do NOT use JSON, and do NOT invent your own rigid multi-section template or bracket labels beyond whatever the user's message itself asks for. Write warmly and concisely about how the week went overall, what was done well, and what to improve. THEN close the retrospective with a clear next-week conclusion in the last 1-2 sentences, still written as prose (no headers): narrow down to EXACTLY ONE ONE Thing to focus on next week — a single measurable result, NOT a list and NOT one item per category — briefly state in one clause WHY you chose it (connecting it to this week's activity or this month's goal), and name ONE concrete first action that can be completed within about 30 minutes on Monday. Never enumerate multiple candidates; commit to a single ONE Thing.";
    } else if (responseType === "monthlyResult") {
      systemPrompt = "You are a Korean life coach writing a month-end retrospective for ONE goal category. Based on the monthly action plan and what was actually completed, write a concise retrospective in Korean PLAIN TEXT only (no JSON, no markdown, no bracket labels). Maximum 2 short sentences, 개조식 톤. Mention 계획 대비 실제 실행, and one 다음 달 보완점. Use monthly framing; NEVER use the words '오늘' or '내일'.";
    } else if (responseType === "dailyAnalysis") {
      // ── [개선] 기존 섹션(💬 오늘 성찰 코멘트 / 📚 오늘 배운 것 정리 / 🎯 한 줄 요약)은 유지하고,
      //           💬 섹션 끝에 "🎯 내일 ONE Thing" 한 줄(완료 기준이 있는 구체적 행동 1개)을 추가 ──
      systemPrompt = "You are a Korean productivity & learning coach. Respond in Korean only, as readable plain text with emoji section headers (no JSON, no markdown tables). Keep the whole response concise and warm. Use these sections in order:\n\n💬 오늘 성찰 코멘트\nBased on the user's daily reflection (감사/잘한일/아쉬운점/다짐), give warm encouragement and 1-2 short pattern comments. 2-4 sentences. Then, at the END of this section, ALWAYS add exactly one line starting with \"🎯 내일 ONE Thing: \" followed by the single most important thing to do tomorrow — ONE concrete action with a clear completion criterion (so it is obvious when it is done). It must be exactly ONE action: never list multiple candidates, never use 'or'.\n\n📚 오늘 배운 것 정리\nIf learning notes are provided, organize them into:\n① 핵심 개념: 배운 내용을 간결히 정리\n② 모호하거나 오해했을 수 있는 부분: 빠졌거나 헷갈릴 수 있는 지점 짚기\n③ 더 알면 좋은 것: 이어서 알아두면 좋은 1-2가지\n\n🎯 한 줄 요약\n중학생도 이해할 한 문장으로 오늘 배운 것을 요약.\n\nIf NO learning notes are provided, skip the 📚 and 🎯 한 줄 요약 sections and give only the 💬 section (which still includes the 🎯 내일 ONE Thing line). Keep it concise and warm.";
    } else if (responseType === "learningAnalysis") {
      systemPrompt = "You are a Korean learning coach. The user provides short keyword memos of what they learned today. Respond in Korean only, as readable plain text with emoji section headers (no JSON, no markdown tables). Use exactly these sections in order:\n\n📚 핵심 개념 정리\n배운 핵심 개념을 명확하게 정리.\n\n🤔 모호하거나 오해했을 수 있는 부분\n빠졌거나 헷갈릴 수 있는 지점, 다시 확인하면 좋을 부분 짚기.\n\n➕ 더 알면 좋은 것\n이어서 알아두면 좋은 1-2가지.\n\n🎯 한 줄 요약\n중학생도 이해할 한 문장으로 오늘 배운 것을 요약.\n\nKeep it concise, warm, and practical.";
    } else {
      systemPrompt = "You are a Korean productivity coach. Always respond in Korean with this exact format: [오늘의 성과] completion rate summary [잘한 점] 1. 2. [아쉬운 점] 1. 2. [내일 개선 제안] 1. 2. [응원 한마디] one encouraging sentence";
    }

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
