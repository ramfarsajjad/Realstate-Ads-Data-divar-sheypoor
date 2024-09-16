import os
import threading
import subprocess

def main():

    dir_main =  os.path.dirname(os.path.abspath(__name__))

    sc_program = os.path.join(dir_main, 'scraper', 'rab_sc.py')

    div_program_pars1 = os.path.join(dir_main, 'parser/lev1_parser/div_lev1_parser', 'div_rab_pars1.py')
    div_program_pars2 = os.path.join(dir_main, 'parser/lev2_parser/div_lev2_parser', 'div_rab_pars2.py')
    div_programـpars3 = os.path.join(dir_main, 'parser/lev3_parser/div_lev3_parser', 'div_rab_pars3.py')

    syp_program_pars1 = os.path.join(dir_main, 'parser/lev1_parser/syp_lev1_parser', 'syp_rab_pars1.py')
    syp_program_pars2 = os.path.join(dir_main, 'parser/lev2_parser/syp_lev2_parser', 'syp_rab_pars2.py')
    syp_program_pars3 = os.path.join(dir_main, 'parser/lev3_parser/syp_lev3_parser', 'syp_rab_pars3.py')

    save2db_program = os.path.join(dir_main, 'saver', 'rab_db.py')

    selector1 = 'div'
    selector2 = 'syp'

    sc_process = subprocess.Popen(['python3', sc_program])

    if selector1 == 'div':
        div_process1 = subprocess.Popen(['python3', div_program_pars1])
        div_process2 = subprocess.Popen(['python3', div_program_pars2])
        div_process3 = subprocess.Popen(['python3', div_programـpars3])

    if selector2 == 'syp':
        syp_process1 = subprocess.Popen(['python3', syp_program_pars1])
        syp_process2 = subprocess.Popen(['python3', syp_program_pars2])
        syp_process3 = subprocess.Popen(['python3', syp_program_pars3])

    save2db_process = subprocess.Popen(['python3', save2db_program])
    



if __name__ == '__main__':
    main()



