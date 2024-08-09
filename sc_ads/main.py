# import scraper 
# from parser.lev1_parser import div_lev1_parser 
# from parser.lev1_parser import syp_lev1_parser 
# from parser.lev2_parser import div_lev2_parser 
# from parser.lev2_parser import syp_lev2_parser 
# from saver import div_saver 
# from saver import syp_saver 
import os
import threading
import subprocess

def main():

    dir_main =  os.path.dirname(os.path.abspath(__name__))

    selector = 'div'

    div_program1 = os.path.join(dir_main, r'scraper', 'div_sc.py')
    div_program2 = os.path.join(dir_main, r'parser/lev1_parser/div_lev1_parser', 'div_parser_lev1.py')
    div_program3 = os.path.join(dir_main, r'parser/lev2_parser/div_lev2_parser', 'div_parser_lev2.py')
    div_program4 = os.path.join(dir_main, r'saver/div_saver', 'div_saver.py')

    syp_program1 = os.path.join(dir_main, r'scraper', 'syp_sc.py')
    syp_program2 = os.path.join(dir_main, r'parser/lev1_parser/syp_lev1_parser', 'syp_parser_lev1.py')
    syp_program3 = os.path.join(dir_main, r'parser/lev2_parser/syp_lev2_parser', 'syp_parser_lev2.py')
    syp_program4 = os.path.join(dir_main, r'saver/syp_saver', 'syp_saver.py')


    if selector == 'div':
        div_process1 = subprocess.Popen(['python', div_program1])
        div_process2 = subprocess.Popen(['python', div_program2])
        div_process3 = subprocess.Popen(['python', div_program3])
        div_process4 = subprocess.Popen(['python', div_program4])

    elif selector == 'syp':
        syp_process1 = subprocess.Popen(['python', syp_program1])
        syp_process2 = subprocess.Popen(['python', syp_program2])
        syp_process3 = subprocess.Popen(['python', syp_program3])
        syp_process4 = subprocess.Popen(['python', syp_program4])





# ----------------------------------------------------------------------------
    # div_thread1 = threading.Thread(target= scraper.div_sc)
    # div_thread2 = threading.Thread(target= div_lev1_parser.div_parser_lev1)
    # div_thread3 = threading.Thread(target= div_lev2_parser.div_parser_lev2)
    # div_thread4 = threading.Thread(target= div_saver.div_saver)

    # syp_thread1 = threading.Thread(target= scraper.syp_sc)
    # syp_thread2 = threading.Thread(target= syp_lev1_parser.syp_parser_lev1)
    # syp_thread3 = threading.Thread(target= syp_lev2_parser.syp_parser_lev2)
    # syp_thread4 = threading.Thread(target= syp_saver.syp_saver)
    
    # if selector == 'div':
    #     div_thread1.start()
    #     div_thread2.start()
    #     div_thread3.start()
    #     div_thread4.start()

    # elif selector == 'syp':
    #     syp_thread1.start()
    #     syp_thread2.start()
    #     syp_thread3.start()
    #     syp_thread4.start()


if __name__ == '__main__':
    main()



