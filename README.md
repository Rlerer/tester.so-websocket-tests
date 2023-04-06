tester.so-websocket-tests
This repository contains tests for a WebSocket service.

Usage
Start the application in a container: sh start_docker_container.sh
Run the tests: pytest
Generate a report of the tests: allure serve ./allure-results
Unfortunately, the application is not yet dockerized, so running it requires additional setup.

Good luck with the tests! :)
