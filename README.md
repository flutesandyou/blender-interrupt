Тестовое для Galileo Labs

Usage:
./run.sh success      — прогон без прерывания, ожидаем exit code 0
./run.sh internal     — внутреннее прерывание, ожидаем exit code 130
./run.sh sigint       — прерывание SIGINT, ожидаем exit code 130
./run.sh sigterm      — прерывание SIGTERM, ожидаем exit code 130
./run.sh all (по умолчанию) — запустить все тесты по очереди

Info:
*Обернул в базовый класс для переиспользования.
*Чистый хэндлер можно посмотреть в первом коммите.

Спасибо за внимание.
