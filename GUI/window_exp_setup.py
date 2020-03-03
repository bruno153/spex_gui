import PySimpleGUI as sg
#from window_manual_control import manual_control

from pathlib import Path

sg.ChangeLookAndFeel('DarkBlue')
    

def exp_setup(work_path):    
    sg.SetOptions(text_justification='left')
    layout = [
        [sg.Text('Experiment', size=(20,1)), 
            sg.Radio('Excitation', 'RADIO1', default=True, 
                      enable_events=True, key='radio_ex'),
            sg.Radio('Emission', 'RADIO1',  enable_events=True, key='radio_em'), 
            sg.Radio('Kinectics', 'RADIO1', enable_events=True, key='radio_ki')],
        [sg.Text('Excitation', size=(20,1)), 
            sg.Input('400', size=(4,1), key='input_ex_st'), 
            sg.Text('nm', justification='left'),
            sg.Input('600', size=(4,1), key='input_ex_en'), 
            sg.Text('nm', justification='left')],
        [sg.Text('Emission', size=(20,1)), 
            sg.Input('300', size=(4,1), key='input_em_st'), 
            sg.Text('nm', justification='left'),
            sg.Input(size=(4,1), disabled=True, key='input_em_en'), 
            sg.Text('nm', justification='left')],
        [sg.Text('Increment', size=(20,1)), 
            sg.Input('1', size=(4,1), key='input_in_nm'), 
            sg.Text('nm', justification='left'), 
            sg.Input(size=(4,1), disabled=True, key='input_in_s'), 
            sg.Text('s', justification='left')],
        [sg.Text('Integration time', size=(20,1)), 
            sg.Slider(range=(1, 30), orientation='h', size=(20, 20), 
                      default_value=1, key='integration_time', 
                      enable_events=True, disable_number_display=True), 
            sg.Text('0.1 s', justification='left', key='text.slider')],
        [sg.Text('Total reaction time', size=(20,1)), 
            sg.Input(size=(4,1), disabled=True, key='input_ti'),
            sg.Text('s', justification='left')],
        # [sg.Text('Measure: ', size=(20,1)), sg.Text('0.0', size=(4,1), 
                                                                # key='measure')],
        [sg.Text('_'*60)],
        [sg.Button('Save setup...', key='save_setup'), 
            sg.Button('Open setup...', key='open_setup')], 
        [sg.Button('Select blank subtraction file...', key='blank_file'), 
            sg.Text('None', size=(40,1), key='blank_text')],
        [sg.Button('Select correction file...', key='correction_file'), 
            sg.Text('None', size=(40,1), key='correct_text')],
        [sg.Button('Submit', size=(20,1), button_color=('black','green')), 
            sg.Quit(size=(10,1), button_color=('black','red'))]
    ]

    window = sg.Window('SPEX control', layout)

    while True:
        event, values = window.read()

        if event=='radio_em':
            window.Element('input_ex_en').Update(disabled=True)
            window.Element('input_em_en').Update(disabled=False)
            window.Element('input_ti').Update(disabled=True)
            window.Element('input_in_s').Update(disabled=True)
            window.Element('input_in_nm').Update(disabled=False)

        if event=='radio_ex':
            window.Element('input_ex_en').Update(disabled=False)
            window.Element('input_em_en').Update(disabled=True)
            window.Element('input_ti').Update(disabled=True)
            window.Element('input_in_s').Update(disabled=True)
            window.Element('input_in_nm').Update(disabled=False)

        if event=='radio_ki':
            window.Element('input_ex_en').Update(disabled=True)
            window.Element('input_em_en').Update(disabled=True)
            window.Element('input_ti').Update(disabled=False)
            window.Element('input_in_s').Update(disabled=False)
            window.Element('input_in_nm').Update(disabled=True)

        if event=='integration_time':
            window.Element('text.slider').Update(str(values['integration_time']/10)+' s')
        
        # if event=='manual_control':
            # manual_control()
        
        if event=='save_setup':
            try:
                # save the experiment setup to the file
                save_path = sg.PopupGetFile('Save experiment setup as..', 
                                            initial_folder=str(work_path),
                                            save_as=True, 
                                            file_types= (('setup files', '.txt'),),)
                file = open(save_path, 'w')
                for key in values.keys():
                    if values[key] is '':
                        values[key]=-1
                    file.write(key + '=' + str(values[key]) + '\n')
                file.close()
            except:
                sg.PopupOK('Ou você não selecionou direito o caminho para salvar, ou algo deu errado.\n Sempre clique em browse para salvar.')
            
        if event=='open_setup':
            # open an experiment and fill the values
            open_path = sg.PopupGetFile('Open experiment setup.', 
                                        initial_folder=str(work_path),
                                        file_types= (('setup files', '.txt'),),)
            file = open((open_path), 'r')
            infos = file.readlines()
            for line in infos:
                line = line.rstrip('\n')
                line = line.split('=')
                if line[1]=='True':
                    line[1] = True
                elif line[1]=='False':
                    line[1]=False
                elif line[1]=='-1':
                    line[1]=''
                else:
                    line[1]=int(float(line[1]))
                window.Element(line[0]).Update(line[1])
                values[line[0]]=line[1]
                
            #-------------------UPDATING THE ELEMENTS VALUES----------
            if values['radio_em']:
                window.Element('input_ex_en').Update(disabled=True)
                window.Element('input_em_en').Update(disabled=False)
                window.Element('input_ti').Update(disabled=True)
                window.Element('input_in_s').Update(disabled=True)
                window.Element('input_in_nm').Update(disabled=False)
            if values['radio_ex']:
                window.Element('input_ex_en').Update(disabled=False)
                window.Element('input_em_en').Update(disabled=True)
                window.Element('input_ti').Update(disabled=True)
                window.Element('input_in_s').Update(disabled=True)
                window.Element('input_in_nm').Update(disabled=False)
            if values['radio_ki']:
                window.Element('input_ex_en').Update(disabled=True)
                window.Element('input_em_en').Update(disabled=True)
                window.Element('input_ti').Update(disabled=False)
                window.Element('input_in_s').Update(disabled=False)
                window.Element('input_in_nm').Update(disabled=True)        
            window.Element('text.slider').Update(str(values['integration_time']/10)+' s')
             #-----------------END OF UPDATES-----------------------------       
            
            file.close()
        
        if event=='blank_file':
            blank_file=''
            blank_file = sg.PopupGetFile('Select the blank subtraction file.')
            window.Element('blank_text').Update(blank_file)
            values['blank_file'] = blank_file
        
        if event=='correction_file':
            correction_file=''
            correction_file = sg.PopupGetFile('Select the photomultiplier correction file.')
            window.Element('correct_text').Update(correction_file)
            values['correction_file'] = correction_file
        
        if event in (None, 'Quit'):
            window.close()
            return None
        if event=='Submit':
            values['correction_file'] = window.Element('correct_text')
            values['blank_file'] = window.Element('blank_text')
            break
    
    for i in values:
        try:
            values[i] = int(values[i])
        except:
            pass

    values['integration_time'] = values['integration_time']/10
    window.close()
    return values
# exp_setup(Path.home()/'Documents'/'SPEX_users')