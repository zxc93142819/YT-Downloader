#!/bin/bash

# 启动第一个 Python 脚本
python ./backend/web-server/web.py &

uvicorn backend.api-server.api:app --reload &

# 等待所有后台任务完成
wait