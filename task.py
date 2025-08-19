import sys
import time
import signal
import os
import bpy

class BlenderInterruptibleTask:
    # класс для создания прерываемых задач в Blender
    def __init__(self):
        self.interrupted = False
        self.interrupt_reason = None
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        # обработчики сигналов прерывания
        signal.signal(signal.SIGINT, self.handle_interrupt)
        signal.signal(signal.SIGTERM, self.handle_interrupt)
    
    def handle_interrupt(self, signum, frame):
        # обработчик внешних сигналов прерывания
        print(f"Получен сигнал прерывания (signum={signum})", flush=True)
        self.interrupted = True
        self.interrupt_reason = f"external_signal_{signum}"
        sys.exit(130)
    
    def request_internal_interrupt(self, reason="internal"):
        # инициирует внутреннее прерывание
        print("Инициировано прерывание изнутри скрипта", flush=True)
        self.interrupted = True
        self.interrupt_reason = reason
        sys.exit(130)
    
    def interrupt_condition(self, step):
        # условие для внутреннего прерывания
        # внутреннее прерывание для тестирования
        if step == 9 and os.getenv('TEST_INTERNAL_INTERRUPT'):
            self.request_internal_interrupt("test_internal")
    def run_task(self):
        # основная логика задачи
        raise NotImplementedError("Метод run_task должен быть переопределен")
    
    def execute(self):
        # запуск выполнения задачи с обработкой прерываний
        try:
            self.run_task()
            print("Работа завершена успешно.", flush=True)
            sys.exit(0)
        except KeyboardInterrupt:
            # дополнительная защита от Ctrl+C
            print("Получено прерывание с клавиатуры", flush=True)
            sys.exit(130)

class DemoLongRunningTask(BlenderInterruptibleTask):
    # демо задача для проверки работы системы прерывания
    
    def run_task(self):
        # имитация длительной работы с возможностью прерывания
        print("Старт длительной операции…", flush=True)
        
        self.print_blender_context()
        
        # имитация долгой работы - 20 шагов по 0.5 сек (~10 сек)
        for i in range(20):
            self.interrupt_condition(i)
            time.sleep(0.5)
            print(f"Шаг {i+1}/20", flush=True)

    def print_blender_context(self):
        # вывод информации о контексте Blender для демонстрации
        print(f"Версия Blender: {bpy.app.version_string}", flush=True)
        print(f"Активная сцена: {bpy.context.scene.name}", flush=True)
        print(f"Количество объектов в сцене: {len(bpy.context.scene.objects)}", flush=True)
    
if __name__ == "__main__":
    # запуск демо задачи
    demo_task = DemoLongRunningTask()
    demo_task.execute()