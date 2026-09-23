// Supabase Edge Function: ai-analysis
// Receives userMessage, calls Claude API, returns { result }
const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS"
};
Deno.serve(async (req)=>{
  if (req.method === "OPTIONS") {
    return new Response("ok", {
      headers: CORS_HEADERS
    });
  }
  try {
    const body = await req.json();
    const userMessage = body.userMessage ?? "";
    const responseType = body.responseType ?? "";
    if (!userMessage) {
      return new Response(JSON.stringify({
        error: "userMessage is required"
      }), {
        status: 400,
        headers: {
          ...CORS_HEADERS,
          "Content-Type": "application/json"
        }
      });
    }
    const apiKey = Deno.env.get("CLAUDE_API_KEY");
    if (!apiKey) {
      return new Response(JSON.stringify({
        error: "CLAUDE_API_KEY is not configured"
      }), {
        status: 500,
        headers: {
          ...CORS_HEADERS,
          "Content-Type": "application/json"
        }
      });
    }
    const maxTokens = body.max_tokens ?? 1500;
    let systemPrompt = "";
    if (responseType === "annualGoalFeedback") {
      systemPrompt = "You are a Korean life coach. Analyze the annual goals and provide specific suggestions. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"selfDev\":[\"suggestion1\",\"suggestion2\"],\"family\":[\"suggestion1\",\"suggestion2\"],\"work\":[\"suggestion1\",\"suggestion2\"]}";
    } else if (responseType === "monthlyPlan") {
      systemPrompt = "You are a Korean life coach. Suggest monthly action plans based on annual goals. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"selfDev\":\"monthly plan content\",\"family\":\"monthly plan content\",\"work\":\"monthly plan content\"}";
    } else if (responseType === "monthlyOneThingSuggest") {
      systemPrompt = "You are a Korean life coach specializing in the ONE Thing methodology. The user provides their annual ONE Things for four life areas with keys: work, job, growth, personal. For EACH area, based on its annual ONE Thing, suggest ONE focused monthly goal that—if achieved this month—would most move that annual goal forward. Narrow each to the single most important thing (do NOT list multiple items). Each value must be a single concrete, measurable, actionable Korean sentence. If an area's annual input is empty, return an empty string for that key. You MUST respond ONLY with valid JSON in this exact format, no other text: {\"work\":\"...\",\"job\":\"...\",\"growth\":\"...\",\"personal\":\"...\"}";
    } else if (responseType === "weeklyReview") {
      systemPrompt = "You are a Korean productivity coach. Based on the user's weekly data, write a natural Korean weekly retrospective as free-flowing prose. Do NOT use any fixed template, section headers, or labels such as [오늘의 성과], [잘한 점], [아쉬운 점]. Write about 4-6 sentences covering how the week went overall, what was done well, what to improve, and a short encouragement at the end. Warm and concise.";
    } else if (responseType === "monthlyResult") {
      systemPrompt = "You are a Korean life coach writing a month-end retrospective for ONE goal category. Based on the monthly action plan and what was actually completed, write a concise retrospective in Korean PLAIN TEXT only (no JSON, no markdown, no bracket labels). Maximum 2 short sentences, 개조식 톤. Mention 계획 대비 실제 실행, and one 다음 달 보완점. Use monthly framing; NEVER use the words '오늘' or '내일'.";
    } else if (responseType === "dailyAnalysis") {
      systemPrompt = "You are a Korean productivity & learning coach. Respond in Korean only, as readable plain text with emoji section headers (no JSON, no markdown tables). Use exactly these sections in order:\n\n💬 오늘 성찰 코멘트\nBased on the user's daily reflection (감사/잘한일/아쉬운점/다짐), give warm encouragement and 1-2 short pattern comments. 2-4 sentences.\n\n📚 오늘 배운 것 정리\nIf learning notes are provided, organize them into:\n① 핵심 개념: 배운 내용을 간결히 정리\n② 모호하거나 오해했을 수 있는 부분: 빠졌거나 헷갈릴 수 있는 지점 짚기\n③ 더 알면 좋은 것: 이어서 알아두면 좋은 1-2가지\n\n🎯 한 줄 요약\n중학생도 이해할 한 문장으로 오늘 배운 것을 요약.\n\nIf NO learning notes are provided, skip the 📚 and 🎯 sections and give only the 💬 section. Keep it concise and warm.";
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
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001",
        max_tokens: maxTokens,
        system: systemPrompt,
        messages: [
          {
            role: "user",
            content: userMessage
          }
        ]
      })
    });
    if (!claudeRes.ok) {
      const errText = await claudeRes.text();
      console.error("Claude API error:", claudeRes.status, errText);
      return new Response(JSON.stringify({
        error: "Claude API request failed",
        status: claudeRes.status
      }), {
        status: 502,
        headers: {
          ...CORS_HEADERS,
          "Content-Type": "application/json"
        }
      });
    }
    const claudeData = await claudeRes.json();
    const result = claudeData.content?.[0]?.text ?? "오류가 발생했어요";
    return new Response(JSON.stringify({
      result
    }), {
      status: 200,
      headers: {
        ...CORS_HEADERS,
        "Content-Type": "application/json"
      }
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("Unhandled error:", message);
    return new Response(JSON.stringify({
      error: message
    }), {
      status: 500,
      headers: {
        ...CORS_HEADERS,
        "Content-Type": "application/json"
      }
    });
  }
});
