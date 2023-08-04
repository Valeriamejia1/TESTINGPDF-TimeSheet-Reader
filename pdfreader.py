from View.windowshandlers import windowshandler as wh

def main():
    main_menu = wh('TimeSheet PDF Reader','400x200+50+50')
    main_menu.open_file_dialog('*.pdf','PDF Files')

if __name__ == '__main__':
    main()


    #TEST