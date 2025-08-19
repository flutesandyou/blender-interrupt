import sys
import time
import signal
import os
import bpy

# хэндлер прерывания
def handle_interrupt(signum, frame):
    print(f"Получен сигнал прерывания (signum={signum})", flush=True)
    # код завершения по заданию
    sys.exit(130)

# регистрируем сигналы
signal.signal(signal.SIGINT, handle_interrupt)   # Ctrl-C / kill -INT
signal.signal(signal.SIGTERM, handle_interrupt)  # kill (по умолчанию)

print(f"Версия Blender: {bpy.app.version_string}", flush=True)
print(f"Активная сцена: {bpy.context.scene.name}", flush=True)
print(f"Количество объектов в сцене: {len(bpy.context.scene.objects)}", flush=True)

print("Старт длительной операции…", flush=True)

# имитация долгой работы: 20 шагов по 0.5 сек (10 сек)
for i in range(20):
    # здесь всякие рутины крутятся
    time.sleep(0.5)
    
    # внутреннее прерывание на 10-м шаге через пер окружения для теста
    if i == 9 and os.getenv('TEST_INTERNAL_INTERRUPT'):
        print("Инициировано прерывание изнутри скрипта", flush=True)
        sys.exit(130)
    
    # визуализация прогресса
    print(f"Шаг {i+1}/20", flush=True)

# если прошли весь луп то это успех с кодом 0
print("Работа завершена успешно.", flush=True)
sys.exit(0)