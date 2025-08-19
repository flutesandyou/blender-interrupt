#!/bin/sh
# POSIX sh-совместимый лаунчер и автотест прерывания Blender/Python
# Использование:
#   ./run.sh success      — прогон без прерывания, ожидаем exit code 0
#   ./run.sh internal     — внутреннее прерывание, ожидаем exit code 130
#   ./run.sh sigint       — прерывание SIGINT, ожидаем exit code 130
#   ./run.sh sigterm      — прерывание SIGTERM, ожидаем exit code 130
#   ./run.sh all (по умолчанию) — запустить все тесты по очереди

BLENDER_BIN="${BLENDER_BIN:-blender}"
SCENE="${SCENE:-scene.blend}"
SCRIPT="${SCRIPT:-task.py}"

run_success() {
    echo "[SUCCESS] Старт без прерывания…"
    "$BLENDER_BIN" -b "$SCENE" --python "$SCRIPT"
    rc=$?
    echo "[SUCCESS] Код возврата Blender: $rc"
    if [ "$rc" -eq 0 ]; then
        echo "[SUCCESS] ОК"
        return 0
    else
        echo "[SUCCESS] FAIL"
        return 1
    fi
}

run_signal() {
    sig="$1"  # INT или TERM
    echo "[SIGNAL:$sig] Старт с последующим прерыванием SIG$sig…"
    
    # запуск в фоне
    "$BLENDER_BIN" -b "$SCENE" --python "$SCRIPT" &
    pid=$!

    # ждем 5 секунд чтобы луп поработал
    sleep 5  
    
    # проверим что процесс жив и отправим сигнал
    if kill -0 "$pid" 2>/dev/null; then
        echo "[SIGNAL:$sig] Отправляем сигнал процессу $pid и всем дочерним"
        pkill -"$sig" -P "$pid" 2>/dev/null || kill -"$sig" "$pid" 2>/dev/null
    else
        echo "[SIGNAL:$sig] Процесс $pid уже завершился"
    fi

    # дождёмся завершения и проверим код
    wait "$pid"
    rc=$?

    echo "[SIGNAL:$sig] Код возврата Blender: $rc"
    if [ "$rc" -eq 130 ]; then
        echo "[SIGNAL:$sig] ОК (exit=130)"
        return 0
    else
        echo "[SIGNAL:$sig] FAIL (exit=$rc)"
        return 1
    fi
}

run_internal() {
    echo "[INTERNAL] Тест внутреннего прерывания…"
    TEST_INTERNAL_INTERRUPT=1 "$BLENDER_BIN" -b "$SCENE" --python "$SCRIPT"
    rc=$?
    
    echo "[INTERNAL] Код возврата Blender: $rc"
    if [ "$rc" -eq 130 ]; then
        echo "[INTERNAL] ОК (exit=130)"
        return 0
    else
        echo "[INTERNAL] FAIL (exit=$rc)"
        return 1
    fi
}

mode="${1:-all}"
case "$mode" in
    success)
        run_success
        exit $?
        ;;
    internal)
        run_internal
        exit $?
        ;;
    sigint)
        run_signal INT
        exit $?
        ;;
    sigterm)
        run_signal TERM
        exit $?
        ;;
    all)
        ok=0
        run_success || ok=1
        run_internal || ok=1
        run_signal INT || ok=1
        run_signal TERM || ok=1
        exit $ok
        ;;
    *)
        echo "Usage: $0 [success|internal|sigint|sigterm|all]"
        exit 2
        ;;
esac