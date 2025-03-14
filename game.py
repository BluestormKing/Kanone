import FreeSimpleGUI as sg
import math
import random

col_player_1_r = sg.Column(layout=[
    [sg.Multiline(default_text="history:\n",
                  autoscroll=True,
                  key="history",
                  disabled=True,
                  size=(50, 10))]
])

col_player_1_l = sg.Column(layout=[
    [sg.Text("Blauer Spieler:", text_color="#0000ff")],
    [sg.Text("Winkel"),
     sg.Slider(range=(1, 90),
               orientation="h",
               size=(25, 20),
               key="angle1", change_submits=True)],
    [sg.Text("Geschwindigkeit"),
     sg.Slider(range=(1, 250),
               orientation="h",
               size=(25, 20),
               key="speed")],
    [sg.Button("Feuer"), sg.Button("clear")],
])

col_player_2_r = sg.Column(layout=[
    [sg.Text("Roter Spieler", text_color="#ff5555")],
    [sg.Text("Winkel"),
     sg.Slider(range=(1, 90),
               orientation="h",
               size=(25, 20),
               key="angle2", change_submits=True)],
    [sg.Text("Geschwindigkeit"),
     sg.Slider(range=(1, 250),
               orientation="h",
               size=(25, 20),
               key="speed2")],
    [sg.Button("Feuer2"), sg.Button("clear2")],
])

col_player_2_l = sg.Column(layout=[
    [sg.Multiline(default_text="history:\n",
                  autoscroll=True,
                  key="history2",
                  disabled=True,
                  size=(50, 10))]
])


col_wins=sg.Column(layout=[
    [sg.Text("Siege Blau:", text_color="#0000ff"), sg.Push(),sg.Text("Siege Rot:", text_color="#ff5555")],
    [sg.Text("0", key="blue", font=("Arial", 48), text_color="#0000ff"),
     sg.Text(":", font=("Arial", 48), text_color="#ff00ff"),
     sg.Text("0", key="red", font=("Arial", 48), text_color="#ff0000")],
])

MAXX = 2500

layout = [
    [col_player_1_l,
     col_player_1_r,
     sg.Push(),
     col_wins,
     #col_wins_blue,
     #col_wins_red,
     sg.Push(),
     col_player_2_l,
     col_player_2_r,
     ],

    [sg.Graph((2500, 1000), (0, 0), (MAXX, 400), key="canvas", background_color="#FFFFFF")],
    [sg.Button("exit")],
]

window = sg.Window("Kanonenspiel", layout)
window.finalize()
figures = []
schuss_figures = {}
schuss = 0
figures2 = []
schuss_figures2 = {}
schuss2 = 0
kanone1_x = random.uniform(0.1 * MAXX, 0.3 * MAXX)
kanone2_x = random.uniform(0.7 * MAXX, 0.9 * MAXX)
kanone1 = window["canvas"].draw_circle((kanone1_x, 0),
                                       40,
                                       "#0000ff",
                                       )
kanone2 = window["canvas"].draw_circle((kanone2_x, 0),
                                       40,
                                       "#ff0000",
                                       )
rohr1=window["canvas"].draw_line((kanone1_x,0),(kanone1_x,40), color="#0000ff", width=50)
rohr2=window["canvas"].draw_line((kanone2_x,0),(kanone2_x,40), color="#ff0000", width=50)
game_over = False
blue_wins=0
red_wins=0
while True:
    event, values = window.read()
    if event == "angle1":
        print(values["angle1"])
        #rohr1=window["canvas"].draw_line((kanone1_x,0),(kanone1_x,40), color="#0000ff", width=5)
        window["canvas"].delete_figure(rohr1)
        dx=math.cos(math.radians(values["angle1"]+10))*80
        dy=math.sin(math.radians(values["angle1"]+10))*40
        rohr1 = window["canvas"].draw_line((kanone1_x, 0), (kanone1_x+dx, dy), color="#0000ff", width=50)
    if event == "angle2":
        print(values["angle2"])
        #rohr1=window["canvas"].draw_line((kanone1_x,0),(kanone1_x,40), color="#0000ff", width=5)
        window["canvas"].delete_figure(rohr2)
        dx=math.cos(math.radians(values["angle2"]+10))*80
        dy=math.sin(math.radians(values["angle2"]+10))*40
        rohr2 = window["canvas"].draw_line((kanone2_x, 0), (kanone2_x-dx, dy), color="#ff0000", width=50)
    if event in ("exit", sg.WIN_CLOSED):
        break
    if event == "clear":
        for fig in figures:
            window["canvas"].delete_figure(fig)
        figures = []

    if event == "clear2":
        for fig in figures2:
            window["canvas"].delete_figure(fig)
        figures2 = []

    if event == "Feuer2":
        schuss2 += 1
        schuss_figures2[schuss2] = []
        # alte schüsse immer mehr löschen
        for alter_schuss_nummer in range(1, schuss2):
            to_delete = []
            for fig_nr in schuss_figures2[alter_schuss_nummer]:
                if random.random() < 0.6:
                    to_delete.append(fig_nr)
            for fnr in to_delete:
                window["canvas"].delete_figure(fnr)
                schuss_figures2[alter_schuss_nummer].remove(fnr)
                try:
                    figures2.remove(fnr)
                except ValueError:
                    pass
        # print(f"Schuss mit Winkel {values['angle']} und Geschwindigkeit {values['speed']}")
        y0 = 1  # anfangs h
        x0 = MAXX - kanone2_x  # start x
        # vx=20    #x speed
        # vy=20    #y speed
        vx = math.cos(math.radians(values["angle2"])) * values['speed2']
        vy = math.sin(math.radians(values["angle2"])) * values['speed2']
        x = x0  # x pos Kugel
        y = y0  # y pos Kugel
        t = 0  # time
        g = -9.81
        while y > 0:
            x = x0 + vx * t
            y = y0 + vy * t + 0.5 + g * t * t
            # fig ist eine nummer
            fig = window["canvas"].draw_point((MAXX - x, y), size=2, color='#FF0000')
            figures2.append(fig)
            schuss_figures2[schuss2].append(fig)
            t += 0.01
        # multiline feld updaten
        txt = values["history2"]
        txt += f"\n# {schuss2} winkel: {values['angle2']} speed: {values['speed2']} ergebnis: {x:.2f} {x - MAXX + kanone1_x:.1f} {'zu kurz' if x - MAXX + kanone1_x < 0 else 'zu weit'}"
        window["history2"].update(txt)
        if abs(x - MAXX + kanone1_x) < 22:
            sg.popup_ok("Roter Spieler hat Gewonnen!")
            game_over = True
            red_wins+= 1
            window["red"].update(f"{red_wins}")

    if event == "Feuer":
        schuss += 1
        schuss_figures[schuss] = []
        # alte schüsse immer mehr löschen
        for alter_schuss_nummer in range(1, schuss):
            to_delete = []
            for fig_nr in schuss_figures[alter_schuss_nummer]:
                if random.random() < 0.6:
                    to_delete.append(fig_nr)
            for fnr in to_delete:
                window["canvas"].delete_figure(fnr)
                schuss_figures[alter_schuss_nummer].remove(fnr)
                try:
                    figures.remove(fnr)
                except ValueError:
                    pass
        # print(f"Schuss mit Winkel {values['angle']} und Geschwindigkeit {values['speed']}")
        y0 = 1  # anfangs h
        x0 = kanone1_x  # start x
        # vx=20    #x speed
        # vy=20    #y speed
        vx = math.cos(math.radians(values["angle1"])) * values['speed']
        vy = math.sin(math.radians(values["angle1"])) * values['speed']
        x = x0  # x pos Kugel
        y = y0  # y pos Kugel
        t = 0  # time
        g = -9.81
        while y > 0:
            x = x0 + vx * t
            y = y0 + vy * t + 0.5 + g * t * t
            # fig ist eine nummer
            fig = window["canvas"].draw_point((x, y), size=2, color='#0000FF')
            figures.append(fig)
            schuss_figures[schuss].append(fig)
            t += 0.01
        # multiline feld updaten
        txt = values["history"]
        txt += f"\n# {schuss} winkel: {values['angle1']} speed: {values['speed']} ergebnis: {x:.2f} {x - kanone2_x:.1f} {'zu kurz' if x - kanone2_x < 0 else 'zu weit'} "
        window["history"].update(txt)
        # treffer?
        if abs(x - kanone2_x) < 22:
            sg.popup_ok("Blauer Spieler hat Gewonnen!")
            game_over = True
            blue_wins+=1
            window["blue"].update(f"{blue_wins}")

    if game_over:
        window["history"].update("history:")
        window["history2"].update("history:")
        window["canvas"].erase()
        figures = []
        schuss_figures = {}
        schuss = 0
        figures2 = []
        schuss_figures2 = {}
        schuss2 = 0
        kanone1_x = random.uniform(0.1 * MAXX, 0.3 * MAXX)
        kanone2_x = random.uniform(0.7 * MAXX, 0.9 * MAXX)
        kanone1 = window["canvas"].draw_circle((kanone1_x, 0),
                                               40,
                                               "#0000ff",
                                               )
        kanone2 = window["canvas"].draw_circle((kanone2_x, 0),
                                               40,
                                               "#ff0000",
                                               )
        game_over = False

window.close()

# self.pos.x = self.startpos.x + self.startspeed.x * self.t
# self.pos.z = self.startpos.z + self.startspeed.z * self.t
# self.pos.y = self.startpos.y + self.startspeed.y * self.t + 0.5 * gravity.y * self.t * self.t