CMD_ON = 175
CMD_OFF = 174
CMD_CHARGE_PUMP_SET = 141
CMD_SET_ROW = 176

CMD_TOP_TO_BOTTOM = 200
CMD_LEFT_TO_RIGHT = 161
CMD_SET_ADDR_MODE = 32
ADDR_MODE_HORIZ = 0b00
CHARGE_PUMP_ON = 20

CMD_BUF = bytearray(1)

def command(*cmds):
    for cmd in cmds:
        CMD_BUF[0] = cmd
        i2c.write(60, CMD_BUF, prefix=128)

def display_init():
    i2c.init(1000000)
    command(CMD_OFF)
    sleep(10)
    command(CMD_ON)
    command(CMD_TOP_TO_BOTTOM, CMD_LEFT_TO_RIGHT)
    sleep(10)
    #command(CMD_SCROLL_STOP)
    command(CMD_SET_ADDR_MODE, ADDR_MODE_HORIZ)
    command(0x21, 0, 127)
    command(CMD_CHARGE_PUMP_SET, CHARGE_PUMP_ON)

# def showimg(img):
#     cur = 1
#     data = iter(img)
#     while True:
#         count = next(data)
#         val = next(data)
#         for x in range(cur, cur+count):
#             row, col = divmod(x, 128)
#             DISPLAY_BUF[col*8 + row] = val
#         cur += count
#         if cur == len(DISPLAY_BUF):
#             break
#     repaint()

# def set_update_window(start_col, end_col):
#     command(0x21, start_col, end_col)

# def set_inverse(inverse):
#     cmd = 0xA7 if inverse else 0xA6
#     command(cmd)

def pulse(time=500):
    per_step = time / 20
    for i in range(255, 1, -10):
        command(0x81)
        command(i)
        sleep(per_step)
    for i in range(1, 255, 10):
        command(0x81)
        command(i)
        sleep(per_step)

# def scroll_clear(self):
#     clear_cmd = bytearray(9)
#     clear_cmd[0] = 64
#     set_update_window(0, 0)
#     n_cleared = 0
#     h_scroll(False, 1)
#     while True:
#         i2c.write(60 , clear_cmd)
#         sleep(15)
#         n_frames = (running_time() - scroll_time_base) / ms_per_frame
#         if n_frames > 150:
#             break
#     set_update_window(0, 127)
#     command(CMD_SCROLL_STOP)
