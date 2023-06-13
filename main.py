from time import sleep
from keyboard import add_hotkey, wait
from pyautogui import locateAllOnScreen, locateCenterOnScreen, mouseDown, moveTo
from multiprocessing import Process, Manager

lang = "ru"
searching_sample = f"./samples/searching_{lang}.png"
sample = "./samples/4.png"
last_proc: Process


def clicking(image_location) -> None:
    print(f"        Нашёл: {image_location}")
    moveTo(image_location)
    mouseDown()
    sleep(2)
    return image_location


def searching(SEARCHING_ACTIVE: Manager):
    conf = 0.9
    Amount = 5
    while SEARCHING_ACTIVE.value:
        print("Ожидаю окончания сражения")
        searching_start = locateCenterOnScreen(searching_sample, confidence=0.6, grayscale=True)
        sleep(0.5)
        if searching_start:
            print("    Добываем!!!")
            image_location = locateAllOnScreen(sample, confidence=conf, grayscale=True)
            if not image_location:
                print(f"\nНе нашёл кнопок\n")
                break
            else:
                lasc_loc = None
                for loc in image_location:
                    if not Amount:
                        break
                    if lasc_loc:
                        if loc.top - lasc_loc.top < 5:
                            print(f"####Пропуск {loc}")
                            continue
                    clicking(loc)
                    Amount -= 1
                    lasc_loc = loc
                print("    Добыча завершена\n")
                sleep(5)
    print('Для запуска/остановки поиска нажмите "F2"\nДля завершения нажмине "F3"')


def start_stop(SEARCHING_ACTIVE: Manager):
    global last_proc
    search_proc = Process(target=searching, args=(SEARCHING_ACTIVE,))
    if SEARCHING_ACTIVE.value:
        print("Остновка поиска")
        print('Для запуска/остановки поиска нажмите "F2"\nДля завершения нажмине "F3"')
        SEARCHING_ACTIVE.value = False
        last_proc.terminate()
    else:
        print("Запуск поиска")
        SEARCHING_ACTIVE.value = True
        search_proc.start()
        last_proc = search_proc


def cancel():
    exit(0)


def main():
    manager = Manager()
    SEARCHING_ACTIVE = manager.Value("SEARCHING_ACTIVE", False)
    print('Для запуска/остановки поиска нажмите "F2"\nДля завершения нажмине "F3"')
    add_hotkey("f2", start_stop, args=(SEARCHING_ACTIVE,))
    wait("f3")


if __name__ == "__main__":
    main()
