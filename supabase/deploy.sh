#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║   daily-briefing Edge Function 배포 스크립트                    ║
# ║   실행 전: supabase CLI 설치 필요                               ║
# ║   brew install supabase/tap/supabase                            ║
# ╚══════════════════════════════════════════════════════════════════╝
set -e

PROJECT_REF="qxqkpgkiuzdvkdieqynf"

echo "🔐 환경변수(Secrets) 설정 중..."

# ── 아래 값들을 실제 값으로 교체하세요 ──
supabase secrets set \
  --project-ref "$PROJECT_REF" \
  SUPABASE_URL="https://qxqkpgkiuzdvkdieqynf.supabase.co" \
  SUPABASE_SERVICE_KEY="YOUR_SERVICE_ROLE_KEY_HERE" \
  CLAUDE_API_KEY="YOUR_CLAUDE_API_KEY_HERE" \
  TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE" \
  TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID_HERE"

echo "🚀 Edge Function 배포 중..."
supabase functions deploy daily-briefing \
  --project-ref "$PROJECT_REF" \
  --no-verify-jwt

echo "✅ 배포 완료!"
echo ""
echo "📋 배포된 함수 URL:"
echo "   https://$PROJECT_REF.supabase.co/functions/v1/daily-briefing"
echo ""
echo "🧪 테스트 실행:"
echo "   curl -X POST https://$PROJECT_REF.supabase.co/functions/v1/daily-briefing"
echo ""
echo "⏰ Cron 스케줄: 매일 13:00 UTC (22:00 KST)"
echo "   Supabase 대시보드 > Edge Functions 에서 확인 가능"
