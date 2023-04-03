#!/bin/bash
docker run -it --rm \
-v /Users/mikhailrogov/PycharmProjects/pythonProject4/tester.so:/tester.so \
-p 4000:4000 \
ubuntu:18.04 /bin/bash -c 'chmod +x /tester.so && /tester.so 0.0.0.0 4000'