import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        host="0.0.0.0",
        port=8000,
        log_level="info",
        app="api.main:app",
        timeout_keep_alive=9999,
        ws_ping_timeout=9999,
        limit_concurrency=9999
    )