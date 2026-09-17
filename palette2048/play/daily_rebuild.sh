#!/bin/zsh
# Palette 웹 데일리판 매일 재빌드 — launchd com.kkiruk.palette-web (매일 00:20).
# 새로 출제가 끝난 명화의 팔레트 페이지를 추가하고 sitemap 을 갱신해 푸시한다.
# 검색엔진 통보는 09:40 com.kkiruk.indexnow 가 라이브 sitemap 을 읽어 처리한다.
# 다른 터미널의 미커밋 작업을 건드리지 않도록 palette2048/ 와 sitemap.xml 만 커밋한다.
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd "$HOME/kkirukstudio-site"
echo "=== $(date '+%F %T')"

python3 palette2048/play/build.py
git add palette2048 sitemap.xml
if git diff --cached --quiet; then
  echo "변경 없음"
  exit 0
fi
git commit -q -m "palette: 웹 데일리 재빌드 $(date +%F)"
if ! git push -q origin main; then
  git -c rebase.autoStash=true pull -q --rebase origin main
  git push -q origin main
fi
git log -1 --format='pushed %h %s'
