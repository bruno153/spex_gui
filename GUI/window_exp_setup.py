import PySimpleGUI as sg
#from window_manual_control import manual_control
import pickle as p
from pathlib import Path

sg.ChangeLookAndFeel('DarkBlue')
    

def exp_setup(work_path):  
    blank_file = Path('None')
    correction_file = Path('None')
  
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
        [sg.Button('Select blank subtraction file...', key='blank_file_btn'), 
            sg.Text('None', size=(40,1), key='blank_file')],
        [sg.Button('Select correction file...', key='correction_file_btn'), 
            sg.Text('None', size=(40,1), key='correction_file')],
        [sg.Button('Submit', size=(20,1), button_color=('black','green')), 
            sg.Quit(size=(10,1), button_color=('black','red'))]
    ]

    window = sg.Window('SPEX control', layout)

    while True:
        event, values = window.read()
        values['blank_file'] = blank_file
        values['correction_file'] = correction_file
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
            values['blank_file'] = blank_file
            values['correction_file'] = correction_file
            try:
                # save the experiment setup to the file
                save_path = sg.PopupGetFile('Save experiment setup as..', 
                                            initial_folder=str(work_path),
                                            save_as=True, 
                                            file_types= (('setup files', '.setup'),),)
                if save_path is None:
                    continue
                p.dump(values, open(save_path, 'wb'))
            except:
                sg.PopupOK('Ou você não selecionou direito o caminho para salvar, ou algo deu errado.\n Sempre clique em browse para salvar.')
                raise
                
        if event=='open_setup':
            try:
                # open an experiment and fill the values
                open_path = sg.PopupGetFile('Open experiment setup.', 
                                            initial_folder=str(work_path),
                                            file_types= (('setup files', '.setup'),),)
                if open_path== None:
                    continue
                values = p.load(open(open_path,'rb'))                    
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
                for key in values:
                    window.Element(key).Update(values[key])
                window.Element('text.slider').Update(str(values['integration_time']/10)+' s')
                blank_file = values['blank_file']
                correction_file = values['correction_file']
                window.Element('blank_file').Update(values['blank_file'].name)
                window.Element('correction_file').Update(values['correction_file'].name)
                 #-----------------END OF UPDATES-----------------------------       
            except:
                sg.PopupOK('Erro de leitura, ou vc cancelou ou path inexistente ou bug inerente')
                raise
        if event=='blank_file_btn':
            blank_file = Path(sg.PopupGetFile('Select the blank subtraction file.',
                                                initial_folder=str(work_path)))
            window.Element('blank_file').Update(blank_file.name)
        
        if event=='correction_file_btn':
            correction_file = Path(sg.PopupGetFile('Select the photomultiplier correction file.',
                                                    initial_folder=str(work_path)))
            window.Element('correction_file').Update(correction_file.name)

        
        if event in (None, 'Quit'):
            window.close()
            return None
        if event=='Submit':
            values['blank_file'] = blank_file
            values['correction_file'] = correction_file
            print(values['correction_file'])
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