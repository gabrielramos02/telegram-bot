def barra_progreso(
    porciento: float,
):
    t, no, si = ("█", "⬜", "⬛")
    cuadros_si = porciento // 10
    cuadros_si = int(cuadros_si)
    cuadros_no = 10 - cuadros_si
    # print(cuadros_si,cuadros_no)
    barra = si * cuadros_si + no * cuadros_no
    return barra
