from time import sleep
from keyboard import add_hotkey, wait
from pyautogui import locateAllOnScreen, locateCenterOnScreen, mouseDown, moveTo, Point, pixel
from multiprocessing import Process, Manager

battle_end = f"./samples/battle_end.png"
point = "./samples/point.png"
purp_point = "./samples/purp_point.png" #255+-5 76+-30 255+-10
blue_point = "./samples/blue_point.png"
last_proc: Process


def clicking(loc) -> None:
    print(f"        Нашёл: {loc}")
    moveTo(loc)
    mouseDown()
    sleep(2)
    return loc

def filtering(point_location):
    lasc_loc = None
    for loc in point_location:
        if not check_battle_end():
            break
        if lasc_loc:
            if loc.top - lasc_loc.top < 5:
                print(f"####Пропуск {loc}")
                continue
        clicking(loc)
        Amount -= 1
        lasc_loc = loc
                

def check_battle_end() ->(Point | None):
    searching_start = locateCenterOnScreen(battle_end, confidence=0.6, grayscale=True)
    return searching_start if searching_start else None




def searching(SEARCHING_ACTIVE: Manager):
    while SEARCHING_ACTIVE.value:
        sleep(0.5)
        print("Ожидаю окончания сражения")
        searching_start = check_battle_end()
        if searching_start:
            point_locations = locateAllOnScreen(point, confidence=0.85, grayscale=True)
            if not point_locations:
                print(f"\nЦенностей не найдено\n")
                break
            else:
                filtering()
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
    last_proc.terminate()


if __name__ == "__main__":
    main()
