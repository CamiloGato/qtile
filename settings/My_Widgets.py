import subprocess
import math
from libqtile.widget import base
from libqtile.log_utils import logger

# Función que retorna la salida de un CMD, valida.
def run_command(cmd='clear'):
    command = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if command.returncode != 0:
        data = None
        error = command.stderr.decode("UTF-8")
        logger.error(f"Error en correr comando {cmd}:\n{error}")
    else:
        data = command.stdout.decode("UTF-8")
    
    return data


class BatteryIconWidget (base.ThreadPoolText):
    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        
        self.cmd_lvl = "acpi | cut -d ' ' -f4 | cut -c 1-2"
        self.cmd_state = "acpi | cut -d ' ' -f 3 | cut -d ',' -f 1"
        self.battery_level = 0
        self.battery_state = ''

    # Función escoge el icono dentro de los disponibles 
    def _battery_icon(self, *args, **kwargs):
        icon_theme = 0 # 0 - Unknown | 1 - Discharging | 2 - Charging

        battery_icon_dict = {
            #  100 - 10 - 20 - 30 - 40 - 50 - 60 - 70 - 80 - 90
            0:[' ','',' ',' ',' ','',' ','',' ',' '],
            1:[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            2:[' ','',' ',' ',' ','',' ','',' ',' '],
        }

        if(self.battery_state == 'Unknown\n'):
            icon_theme = 0
        if(self.battery_state == 'Discharging\n'):
            icon_theme = 1
        if(self.battery_state == 'Charging\n'):
            icon_theme = 2

        # Función para tener index por icono.
        def downLevel(level):
            if level == 100:
                return 0
            return math.floor(level/10)

        return str(battery_icon_dict.get(icon_theme)[downLevel(self.battery_level)])

    def poll(self):
        self.battery_level = int(run_command(self.cmd_lvl))
        self.battery_state = str(run_command(self.cmd_state))
        return self._battery_icon(self)