#!/bin/sh -e
quizr="/home/pi/src/quizr/app.py"
if [ -f "$quizr" ]; then
  logger -t QuizR -p user.info "[>>> Launching QuizR <<<]"
  python3 "$quizr" &
else
  logger -t QuizR -p user.error "[>>> QuizR not found <<<]"
fi
