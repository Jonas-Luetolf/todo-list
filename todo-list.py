#imports from src
from src.argummentparser import ArgummentParser
from src.listhandler import ListHandler
from src.ui import UI
from src.settingshandler import SettingsHandler

#imports from std libary
from os.path import expanduser
from sys import argv

def parse_args()->tuple:
    arg_parser=ArgummentParser(["show","add-task","delete-task","change-state"])
    arg_parser.add_flag("list",1,"l")       
    arg_parser.add_flag("state",1,"s")      
    arg_parser.add_flag("folder",1,"f")     
    arg_parser.add_flag("task",1,"t")   
    return arg_parser.parse(argv[1:])

def main()->None:
    command,flags=parse_args()

    #load settings
    settings_handler=SettingsHandler(f"{expanduser('~')}/.todo-list/config.yaml")
    settings=settings_handler.get_settings()
    
    #make ui
    ui=UI(settings)

    #set folder path
    if "--folder" in flags:
        folder=flags["--folder"][0]
    else:
        folder=settings["list_folder"]
    
    #open list
    list_handler=ListHandler(flags["--list"][0],folder)

    match command:
        case "show":
            #set state
            if "--state" in flags:
                state=int(flags["--state"][0])        
            else:
                state=None

            ui.print_list(list_handler,state)

        case "add-task":
            new_task_data=ui.ask_task_informations()
            list_handler.add_task(new_task_data["name"],new_task_data["description"],new_task_data["state"])
        
        case "delete-task":
            list_handler.delete_task(flags["--task"][0])

        case "change-state":
            if "--state" in flags:
                state=int(flags["--state"][0])
            else:
                state=1
            list_handler.change_state(flags["--task"][0],state)
    
    #write list
    list_handler.write()   

if __name__=="__main__":
    main()