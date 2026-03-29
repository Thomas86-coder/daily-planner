#!/bin/bash
# deploy.sh — 변경사항 저장 후 GitHub Pages 배포
# 사용법: bash deploy.sh "커밋 메시지"

MSG="${1:-update: 내용 업데이트}"

echo ""
echo "🚀 GitHub Pages 배포 시작..."
echo "📝 커밋 메시지: $MSG"
echo ""

cd "$(dirname "$0")"

# 변경사항 확인
if [ -z "$(git status --porcelain)" ]; then
  echo "✅ 변경사항이 없어요 (이미 최신 상태)"
  exit 0
fi

# Git add → commit → push
git add -A
git commit -m "$MSG"
git push origin main

echo ""
echo "✅ 배포 완료!"
echo "🌐 사이트: https://thomas86-coder.github.io/daily-planner/"
echo "⏱  GitHub Pages 반영까지 약 30초~1분 소요"
echo ""
echo "  배포 상태 확인:"
echo "  https://github.com/Thomas86-coder/daily-planner/actions"
