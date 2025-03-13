def render_error(errtitle,message):
    from flask import render_template

    return render_template('error.html', title=errtitle, error=message)

def write_file(funct_Str, funct_str2=''):
    """ 
    debug function that creates text file
    and returns file to be written to for
    debugging functions and procedures.
    """
    
    from datetime import datetime
    import os
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cTime = current_time.replace(':','')
    
    save_Path = 'debug_Log'
    if not funct_str2=='':
        file_name = 'debug_'+ funct_str2 + '_' + funct_Str + "_" + str(cTime) + ".txt"
    else:
        file_name = 'debug_'+ funct_Str + "_" + str(cTime) + ".txt"
    

    file = os.path.join(save_Path,file_name)
    
    debugFile = open(file,"w")
    debugFile.write("Created - " + str(now) + "\n")
    
    return debugFile