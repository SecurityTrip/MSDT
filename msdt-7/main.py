import asyncio
import aiohttp
import time
import json
import aiofiles

# Список URL для проверки
urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
]

# Асинхронная функция для выполнения HTTP-запроса
async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            result = await response.json()
            print(f"Получены данные с {url}")
            return result
    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")
        return None

# Асинхронная функция для сохранения данных в файл
async def save_to_file(data, filename):
    try:
        async with aiofiles.open(filename, mode="w") as file:
            await file.write(json.dumps(data, indent=4, ensure_ascii=False))
            print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в файл {filename}: {e}")

# Основная функция
async def main():
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Запускаем все запросы параллельно
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # Фильтруем успешные результаты
        valid_results = [res for res in results if res is not None]
        
        # Сохраняем результаты в файл
        await save_to_file(valid_results, "results.json")
    
    elapsed_time = time.time() - start_time
    print(f"Обработка завершена за {elapsed_time:.2f} секунд.")

# Запуск основного события
if __name__ == "__main__":
    asyncio.run(main())
