#!/usr/bin/env bash
set -e
clear
ip=$(hostname -I)
printf "\033[34mIP: \033[30m$ip\n"
tput sgr0
quizr="/home/pi/src/quizr/app.py"
if [ -f "$quizr" ]; then
  logger -t QuizR -p user.info "[>>> Launching QuizR <<<]"
  python3 "$quizr" &
else
  logger -t QuizR -p user.error "[>>> QuizR not found <<<]"
fi
