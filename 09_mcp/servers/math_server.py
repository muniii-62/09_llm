"""두 수를 더하는 Tool을 제공하는 MCP Server"""



# python MCP SDK - V2 : FastMcp
# python MCP SDK - V2 : MCPServer
from mcp.server import MCPServer

# "math_tools"라는 이름을 갖는 MCPServer 인스턴스를 생성
# - Host(AI 클라이언트 == Claude Code, Codex, PyCharm 등) 연결 시
#   노출되는 Tools, Resources, Prompt를 등록하고 관리하는 역할을 함
mcp = MCPServer("math_tools")


@mcp.tool() # 해당 함수를 MCP Tool 규격으로 자동 변환
            # () 내 "도구명"을 적지 않으면 함수명이 도구명이 된다
def add(a: float, b: float) -> float:
    """두 숫자 a와 b를 받아 두 수를 더한 후 곱하기 10 해서 반환한다."""
    return (a + b) * 10

@mcp.tool()
def minus(a: float, b: float) -> float:
    """두 숫자 a와 b를 받아 두 수를 뺀 후 제곱해서 반환한다."""
    return (a - b) ** 2



# 현재 py 파일이 실행 중인 상태라면
if __name__ == "__main__":
    try:
        mcp.run(
            transport="streamable-http",
            host="127.0.0.1", # 서버 host == 서버 주소
            port=8001, # 웹 요청 시 프로그램 구분 번호
            streamable_http_path="/mcp"
        )
    except KeyboardInterrupt:
        # CTRL + C (종료) 시 SDK가 출력하는 메시지 숨기기
        pass

async def main() -> None:
    """MCP 연결을 확인하고 허용된 경우 원본의 두 Agent 질의를 실행한다."""
    weather_payload = await request_weather_without_model("Seoul")
    print("local MCP result:", weather_payload)

    run_paid_agent = os.getenv("RUN_PAID_AGENT", "false").lower() == "true"
    if not run_paid_agent:
        print("RUN_PAID_AGENT=false: 유료 Agent 호출을 실행하지 않았다.")
        return

    agent = await build_agent()
    await demo_queries(agent)


if __name__ == "__main__":
    asyncio.run(main())