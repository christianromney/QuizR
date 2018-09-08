#!/bin/bash
rsync -Crthzv --stats --progress --executability --exclude="__pycache__" --exclude=".git" . romneypi:~/src/quizr/
