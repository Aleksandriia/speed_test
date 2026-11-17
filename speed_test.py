import time
import requests
import sys

def measure_download_speed(url, num_requests=10):
    total_bytes = 0
    total_time = 0.0

    print(f"Начинаем тестирование скорости для: {url}")
    print(f"Количество запросов: {num_requests}\n")

    for i in range(1, num_requests + 1):
        try:
            # Засекаем время перед запросом
            start_time = time.time()
            
            # Выполняем GET-запрос. stream=True позволяет не грузить всё в память сразу,
            # а получать данные по частям, что честнее для замера скорости.
            with requests.get(url, stream=True) as response:
                response.raise_for_status() # Проверка на ошибки (404, 500 и т.д.)
                
                # Читаем данные порциями, чтобы дождаться полного ответа и посчитать объем
                content_size = 0
                for chunk in response.iter_content(chunk_size=8192):
                    content_size += len(chunk)
            
            # Засекаем время после получения полного ответа
            end_time = time.time()
            
            request_time = end_time - start_time
            total_time += request_time
            total_bytes += content_size
            
            # Переводим байты в Килобайты для вывода
            kb_size = content_size / 1024
            
            print(f"Запрос {i}/{num_requests}: {kb_size:.2f} КБ за {request_time:.4f} сек.")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {i}: {e}")
            sys.exit(1)

    # Вычисления средних значений
    if num_requests > 0:
        average_time = total_time / num_requests
        
        # Скорость = Объем (в байтах) / Время (в секундах)
        # Переведем в Килобиты в секунду (Кбит/с), так как это стандарт для интернета
        # 1 байт = 8 бит. Или можно считать в КБ/с. Выберем Кбит/с.
        speed_bps = (total_bytes * 8) / total_time
        speed_kbps = speed_bps / 1024
        
        total_mb = total_bytes / (1024 * 1024)

        print("\n" + "="*40)
        print("РЕЗУЛЬТАТЫ ТЕСТА:")
        print(f"Общий объем скачанных данных: {total_mb:.2f} МБ ({total_bytes} байт)")
        print(f"Среднее время запроса: {average_time:.4f} сек.")
        print(f"Средняя скорость скачивания: {speed_kbps:.2f} Кбит/с (или {speed_kbps/8:.2f} КБ/с)")
        print("="*40)

if __name__ == "__main__":
    # Пример тяжелой картинки (можно заменить на любую другую ссылку)
    # Ссылка на случайное изображение высокого разрешения
    test_url = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=2000"
    
    # Если хочешь передавать URL аргументом, раскомментируй код ниже:
    # if len(sys.argv) > 1:
    #     test_url = sys.argv[1]
    
    measure_download_speed(test_url, num_requests=10)