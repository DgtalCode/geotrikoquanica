from pioneer_sdk.asynchronous import Pioneer
import cv2
import numpy as np

# создаем объект квадрокоптера, через который будет происходить управление
# в параметрах отключается вывод отладочной информации
pioneer = Pioneer(logger=False, heartbeat_logger=False)

shots = []

pioneer.arm()

while True:
    img = pioneer.get_raw_video_frame()
    img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow('image', img)
    cv2.waitKey(1)

    if pioneer.step_get() == 1:
        pioneer.takeoff()
        if pioneer.in_air():
            pioneer.step_inc()

    elif pioneer.step_get() == 2:
        pioneer.sleep(1, callback=pioneer.step_inc)

    elif pioneer.step_get() == 3:
        pioneer.go_to_local_point(x=1.1, y=1.1, z=2, callback=pioneer.step_inc)

    elif pioneer.step_get() == 4:
        pioneer.sleep(1, callback=[
            pioneer.step_inc,
            lambda: shots.append( ((1.1, 1.1, 2), img) )
        ])

    elif pioneer.step_get() == 5:
        pioneer.go_to_local_point(x=2.2, y=1.1, z=2, callback=pioneer.step_inc)

    elif pioneer.step_get() == 6:
        pioneer.sleep(1, callback=[
            pioneer.step_inc,
            lambda: shots.append( ((2.2, 1.1, 2), img) )
        ])

    elif pioneer.step_get() == 7:
        pioneer.go_to_local_point(x=3.3, y=1.1, z=2, callback=pioneer.step_inc)

    elif pioneer.step_get() == 8:
        pioneer.sleep(1, callback=[
            pioneer.step_inc,
            lambda: shots.append( ((3.3, 1.1, 2), img) )
        ])

    elif pioneer.step_get() == 9:
        pioneer.go_to_local_point(x=0.8, y=0.8, z=1, callback=pioneer.step_inc)

    elif pioneer.step_get() == 10:
        pioneer.land()
        if pioneer.landed():
            break

cv2.vconcat(shots)
