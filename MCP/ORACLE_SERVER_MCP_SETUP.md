# Oracle 서버 — KIS Code Assistant MCP 연결 가이드

## 구성 요약

```
Claude Code (oracle 서버)
    ↓
~/.claude/settings.json       ← MCP 서버 이름 활성화
~/theprepared/.mcp.json       ← 실제 연결 주소 (http://172.17.0.2:8081/mcp)
    ↓
Docker 컨테이너 (kis-code 이미지)
  컨테이너명: practical_hugle
  내부 IP:   172.17.0.2:8081
```

---

## 파일별 역할

### `~/.claude/settings.json`
```json
{
  "enabledMcpjsonServers": ["kis-code-assistant"]
}
```
Claude Code가 `.mcp.json`에서 `kis-code-assistant` 항목을 읽도록 활성화.

### `~/theprepared/.mcp.json`
```json
{
  "mcpServers": {
    "kis-code-assistant": {
      "type": "http",
      "url": "http://172.17.0.2:8081/mcp"
    }
  }
}
```
- `type`: `http` (Streamable HTTP — 이 서버는 SSE가 아님, `sse`로 쓰면 연결 안 됨)
- `url`: Docker 브리지 네트워크 내부 IP

---

## 최초 설치 (처음 세팅할 때)

```bash
# 1. 이미지 빌드
cd ~/theprepared/kis-mcp/MCP/KIS\ Code\ Assistant\ MCP
docker build -t kis-code .

# 2. 컨테이너 실행 (자동 재시작 포함)
docker run -d --restart=always --name kis-code-assistant-mcp kis-code

# 3. IP 확인
docker inspect kis-code-assistant-mcp --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# 4. .mcp.json 에 해당 IP 반영 (기본값은 172.17.0.2)
```

---

## 끊겼을 때 복구

```bash
# 1. 컨테이너 상태 확인
docker ps | grep kis

# 2. 죽어있으면 재시작
docker start practical_hugle

# 3. 재시작 후 IP 확인 (바뀌었을 수 있음)
docker inspect practical_hugle --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# 4. IP가 바뀌었으면 .mcp.json 수정
nano ~/theprepared/.mcp.json
# → "url" 값의 IP를 새 IP로 변경

# 5. 헬스 체크
curl http://172.17.0.2:8081/health
# 정상: {"status":"healthy","server":"kis-code-assistant-mcp","version":"0.1.0",...}
```

---

## 자동 재시작 설정 (서버 재부팅 대비)

현재 컨테이너에 restart 정책이 없다면:
```bash
docker update --restart=always practical_hugle
```

---

## IP가 자주 바뀌는 경우 — localhost 사용 권장

컨테이너 실행 시 포트를 호스트에 바인딩하면 IP 변경 문제 없음:
```bash
docker run -d --restart=always -p 8081:8081 --name kis-code-assistant-mcp kis-code
```

그 후 `.mcp.json` URL을 `http://localhost:8081/mcp` 로 변경.

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `Failed to reconnect to kis-code-assistant` | 컨테이너 중지됨 | `docker start practical_hugle` |
| 연결되지만 도구 안 보임 | `type: "sse"` 설정 오류 | `.mcp.json`에서 `"type": "http"` 로 변경 |
| IP 연결 불가 | 컨테이너 재시작 후 IP 변경 | `docker inspect`로 IP 재확인 후 `.mcp.json` 수정 |
| Claude Code 재시작 후 MCP 없어짐 | `.mcp.json`이 프로젝트 디렉터리에 없음 | `~/theprepared/.mcp.json` 존재 여부 확인 |
