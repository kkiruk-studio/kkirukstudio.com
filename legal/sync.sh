#!/bin/sh
# /legal/ 의 약관·개인정보 문서는 통합 문서(github.io 두 repo)의 사본이다.
# 원본을 고친 뒤 이 스크립트를 돌려 도메인 쪽 사본을 맞춘다.
# github.io 쪽도 계속 살아 있다 — 기존 앱들의 스토어·인앱 링크가 거기를 가리킨다.
#   원본 위치: LEGAL_SRC 환경변수로 변경 가능
set -e
SRC="${LEGAL_SRC:-$HOME/Find Local/LegalPages}"
HERE=$(cd "$(dirname "$0")" && pwd)

cp "$SRC/terms-of-service-app/index.html" "$HERE/terms/index.html"
cp "$SRC/privacy-policy-app/index.html" "$HERE/privacy/index.html"

# 도메인 안에서는 도메인 문서끼리 잇는다 (문서 간 상호 링크)
sed -i '' 's|https://kkiruk-studio.github.io/privacy-policy-app/|/legal/privacy/|g' "$HERE/terms/index.html"
sed -i '' 's|https://kkiruk-studio.github.io/terms-of-service-app/|/legal/terms/|g' "$HERE/privacy/index.html"

echo "synced from $SRC"
