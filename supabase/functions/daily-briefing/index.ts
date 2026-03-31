import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// ────────────────────────────────────────
// 환경 변수
// ────────────────────────────────────────
const SUPABASE_URL       = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_KEY")!;
const CLAUDE_API_KEY     = Deno.env.get("CLAUDE_API_KEY")!;
const TELEGRAM_BOT_TOKEN = Deno.env.get("TELEGRAM_BOT_TOKEN")!;
const TELEGRAM_CHAT_ID   = Deno.env.get("TELEGRAM_CHAT_ID")!;

// ────────────────────────────────────────
// 타입
// ────────────────────────────────────────
interface Todo {
  id: string;
  text: string;
  category: "work" | "job" | "growth" | "personal";
  done: boolean;
  log_date: string;
}

const CAT_LABEL: Record<string, string> = {
  work: "업무",
  job: "직무",
  growth: "성장",
  personal: "개인",
};

// ────────────────────────────────────────
// 유틸: 오늘 KST 날짜 문자열 (YYYY-MM-DD)
// ────────────────────────────────────────
function getTodayKST(): string {
  const now = new Date();
  // UTC+9 보정
  const kst = new Date(now.getTime() + 9 * 60 * 60 * 1000);
  const y = kst.getUTCFullYear();
  const m = String(kst.getUTCMonth() + 1).padStart(2, "0");
  const d = String(kst.getUTCDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

// ────────────────────────────────────────
// Claude API 호출
// ────────────────────────────────────────
async function callClaude(prompt: string): Promise<string> {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": CLAUDE_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Claude API 오류: ${res.status} - ${err}`);
  }

  const data = await res.json();
  return data.content?.[0]?.text ?? "(Claude 응답 없음)";
}

// ────────────────────────────────────────
// 텔레그램 메시지 전송 (MarkdownV2)
// ────────────────────────────────────────
async function sendTelegram(text: string): Promise<void> {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: TELEGRAM_CHAT_ID,
      text,
      parse_mode: "HTML",
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`텔레그램 전송 오류: ${res.status} - ${err}`);
  }
}

// ────────────────────────────────────────
// 할일 목록 → 텍스트 포맷 (Claude 프롬프트용)
// ────────────────────────────────────────
function formatTodoList(todos: Todo[]): string {
  if (todos.length === 0) return "  (없음)";
  return todos
    .map((t) => `  - [${CAT_LABEL[t.category] ?? t.category}] ${t.text}`)
    .join("\n");
}

// ────────────────────────────────────────
// 메인 핸들러
// ────────────────────────────────────────
Deno.serve(async (_req) => {
  try {
    const today = getTodayKST();
    console.log(`[daily-briefing] 실행 날짜(KST): ${today}`);

    // ── 1) Supabase에서 오늘 할일 조회 ──
    const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

    const { data: todoData, error: todoErr } = await sb
      .from("todos")
      .select("id, text, category, done, log_date")
      .eq("log_date", today)
      .order("category");

    if (todoErr) throw new Error(`할일 조회 실패: ${todoErr.message}`);

    const todos: Todo[] = todoData ?? [];

    // ── 2) 완료 / 미완료 분리 ──
    const doneTodos   = todos.filter((t) => t.done);
    const undoneTodos = todos.filter((t) => !t.done);

    console.log(`[daily-briefing] 완료: ${doneTodos.length}개 / 미완료: ${undoneTodos.length}개`);

    // ── 3) Claude 브리핑 생성 ──
    const dateLabel = `${today.replace(/-/g, "년 ").replace("-", "월 ") + "일"}`;

    const prompt = `
당신은 인생관리 시스템의 AI 비서입니다.
오늘(${dateLabel}) 하루를 마무리하며 사용자에게 따뜻하고 동기부여가 되는 저녁 브리핑 메시지를 작성해주세요.

[오늘 완료한 할일 (${doneTodos.length}개)]
${formatTodoList(doneTodos)}

[오늘 미완료 할일 (${undoneTodos.length}개)]
${formatTodoList(undoneTodos)}

작성 규칙:
1. 텔레그램 HTML 포맷 사용 (<b>굵게</b>, <i>기울기</i>, <code>코드</code> 등)
2. 이모지를 적절히 활용하여 친근하게
3. 완료한 일은 칭찬하고 구체적인 격려 한 마디 포함
4. 미완료 항목이 있으면 "내일로 이월할까요?" 라고 물어보는 문장 자연스럽게 포함
5. 미완료 항목이 없으면 오늘 모두 완수했다는 축하 메시지
6. 전체 길이는 500자 이내로 간결하게
7. 마지막에 내일도 화이팅이라는 짧은 응원 메시지

메시지만 출력하세요 (설명 없이).
`.trim();

    const briefing = await callClaude(prompt);
    console.log("[daily-briefing] 브리핑 생성 완료");

    // ── 4) 텔레그램 전송 ──
    const header = `🌙 <b>오늘의 저녁 브리핑</b> · ${today}\n\n`;
    await sendTelegram(header + briefing);
    console.log("[daily-briefing] 텔레그램 전송 완료");

    return new Response(
      JSON.stringify({
        success: true,
        date: today,
        done: doneTodos.length,
        undone: undoneTodos.length,
      }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("[daily-briefing] 오류:", message);
    return new Response(
      JSON.stringify({ success: false, error: message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
});
