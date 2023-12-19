import pandas as pd
import numpy as np

import streamlit as st
from streamlit.logger import get_logger

# model_df = pd.read_excel('C:/Users/Doc/Desktop/hirsh/data.xlsx')

import pickle

import datetime

from datetime import date



# Loading models and data

with open('model.pickle', 'rb') as f:
  model = pickle.load(f)
  
data = pd.read_excel('data.xlsx')

lists = pd.read_excel('lists.xlsx')

  

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Трансторакальная ЭхоКГ",
        page_icon="favicon48.png"
    )
        
    
    st.image('lipetsk-med.jpg',
              caption=None, 
              width=25, use_column_width=1, clamp=True, channels="RGB", output_format="auto")
    
    st.subheader(""" Эхокардиография с интегрированной нейронной сетью """)
    
    
    # Now day
    
    today = date.today()

    
    
# PATIENTS DATA ===========================================================================================================================================================
        
    name = st.sidebar.text_input('Ф.И.О.', value=None, 
              max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, 
              args=None, kwargs=None, placeholder='Иванов Иван Иванович', 
              disabled=False, label_visibility="visible")
    
    dayofbirth = st.sidebar.date_input('Дата рождения', value=None, 
                              min_value=None, max_value=today, key=None, help=None, on_change=None, 
                              args=None, kwargs=None, format="DD.MM.YYYY", 
                              disabled=False, label_visibility="visible")
            
    grow = st.sidebar.number_input('Рост', min_value=None, max_value=None, value=170, 
                                   step=1, format=None, key=None, help=None, on_change=None, 
                                   args=None, kwargs=None, placeholder=174, disabled=False, label_visibility="visible")
    
    weigt = st.sidebar.number_input('Вес', min_value=None, max_value=None, value=70, 
                                   step=1, format=None, key=None, help=None, on_change=None, 
                                   args=None, kwargs=None, placeholder=76, disabled=False, label_visibility="visible")
         
    date_exam = st.sidebar.date_input('Дата исследования', value="today", 
                              min_value=None, max_value=None, key=None, help=None, on_change=None, 
                              args=None, kwargs=None, format="DD.MM.YYYY", 
                              disabled=False, label_visibility="visible")
    
    time_exam = st.sidebar.time_input('Время исследования', value="now", 
                                      key=None, help=None, on_change=None, 
                                      args=None, kwargs=None, disabled=False, label_visibility="visible", 
                                      step=600)
    
    machine = st.sidebar.selectbox('Аппарат УЗИ', lists['аппарат'])
    
        
    # Previos_preports
        
    # Day of birth calculate
    
    dob = str(dayofbirth)

    try:
        day = int(dob[8:])
        month = int(dob[5:7])
        year = int(dob[:4])    
        age = today.year - year - ((today.month, today.day) < (month, day))
    except:
        age = 0
        
    # Body area calculate
    
    try:
        body_area = round((((int(grow) * int(weigt))**0.5) / 60), 2)
    except:
        body_area = 0
    
    # Anamnesis data
    
    st.caption('Сопутствующие заболевания')
    
    copd_check = st.checkbox('ХОБЛ')
    
    if copd_check == True:
        copd_st = st.radio('Выберите стадию ХОБЛ', ['I', 'II', 'III', 'IV'], index=0, 
                             key=None, help=None, on_change=None, args=None, kwargs=None,
                             disabled=False, horizontal=True, captions=None, label_visibility="visible")
        if copd_st == 'I':
            copd = 1
        elif copd_st == 'II':
            copd = 2
        elif copd_st == 'III':
            copd = 3
        elif copd_st == 'IV':
            copd = 4
    else:
        copd = 0
        
    cad_check = st.checkbox('ИБС')
    
    if cad_check == True:
        cad_st = st.radio('Выберите вариант ИБС', ['ПИКС', 'ЧКВ/АКШ', 'ПИКС + ЧКВ/АКШ'], index=0, 
                             key=None, help=None, on_change=None, args=None, kwargs=None,
                             disabled=False, horizontal=True, captions=None, label_visibility="visible")
        if cad_st == 'ПИКС':
            cad = 1
        elif cad_st == 'ЧКВ/АКШ':
            cad = 2
        elif cad_st == 'ПИКС + ЧКВ/АКШ':
            cad = 3
    else:
        cad = 0
        
    af_check = st.checkbox('ФП')
    
    if af_check == True:
        af_st = st.radio('Выберите вариант ФП', ['Пароксизмальная', 'Персистирующая', 'Постоянная'], index=0, 
                             key=None, help=None, on_change=None, args=None, kwargs=None,
                             disabled=False, horizontal=True, captions=None, label_visibility="visible")
        if af_st == 'Пароксизмальная':
            af = 1
        elif af_st == 'Персистирующая':
            af = 2
        elif af_st == 'Постоянная':
            af = 3
    else:
        af = 0

        
# DATA OF EXAM ===========================================================================================================================================================
    
    try:
        st.caption(name + ', ' + str(age) + ' лет, ' + 'ППТ = ' + str(body_area) + ' м2') 
    except:
        st.caption('Данные о пациенте и исследовании')
    
    exam = st.text_area('Особенности исследования (нажмите ctrl + enter для подтверждения изменений)', value='Визуализация затруднена ввиду анатомических особенностей пациента', 
                        height=25, max_chars=None, key=None, help=None, on_change=None, 
                        args=None, kwargs=None, placeholder='Всё, что не вошло в стандартный протокол', disabled=False, label_visibility="visible")
    
    rythm = st.selectbox('Ритм сердца', lists['ритм'])
        
    st.write('')
    st.write('')
    st.write('*Аорта*')
    
    ao_wall = st.text_input('Стенка аорты', value='уплотнена', 
              max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, 
              args=None, kwargs=None, placeholder=None, 
              disabled=False, label_visibility="visible")
    
    ao_vals = st.number_input('Аорта на уровне с. Вальсальвы, см (норма до 4.0см)', min_value=None, max_value=None, value=3.4, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=3.6, disabled=False, label_visibility="visible")
        
    
    ao = st.number_input('Аорта, восходящий отдел, см (норма до 3.8 см)', min_value=None, max_value=None, value=3.6, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=3.4, disabled=False, label_visibility="visible")
    
    
    st.write('')
    st.write('')
    st.write('*Левое предсердие*')
            
    la = st.number_input('Левое предсердие в PLAX, см (норма до 4.0 см)', min_value=None, max_value=None, value=3.6, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=3.6, disabled=False, label_visibility="visible")
    
    la_a4c_hor = st.number_input('Левое предсердие в A4C - поперечный размер, см (норма до 4.5 см)', min_value=None, max_value=None, value=la + 0.2, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=3.6, disabled=False, label_visibility="visible")
    
    la_a4c_ver = st.number_input('Левое предсердие в A4C - продольный размер, см (норма до 5.3 см)', min_value=None, max_value=None, value=la + 0.5, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=4.6, disabled=False, label_visibility="visible")
    
    la_volume = st.number_input('Объем левого предсерия по Симпсону, мл (норма до 52 мл)', min_value=None, max_value=None, value=la * 10 + 10, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=4.6, disabled=False, label_visibility="visible")
    
    try:
        la_volume_index = round((la_volume / body_area), 1)
        la_index = st.caption('Индекс объема левого предсердия ' + str(la_volume_index) + '  мл/м2 (норма до 28.0 мл/м2)') 
    except:
        la_volume_index = None
             
    st.write('')
    st.write('')
    st.write('*Левый желудочек*')   

    lv = st.number_input('Конечный диастолический размер левого желдудочка, см (норма до 5.6 см)', min_value=None, max_value=None, value=4.8, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    lv_sv = st.number_input('Конечный систолический размер левого желдудочка, см (норма до 2.8 см)', min_value=None, max_value=None, value=2.9, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
                
    lv_dvol = round(7 * (lv**3) / (2.4 + lv), 0)
    
    lv_svol = round(7 * (lv_sv**3) / (2.4 + lv_sv), 0)
    
    bv_teih = round((lv_dvol - lv_svol), 0)
    
    ef = bv_teih / lv_dvol
    
    try:
        ef_teih = round((ef * 100), 0)
        bv_t = st.caption('ударный объем ' + str(bv_teih) + ' мл')
        ef_t = st.caption('фракция выброса по Тейхольцу ' + str(ef_teih) + ' % (норма – более 55%)')
    except:
        ef_t = None
        
     
    dvol = st.number_input('Конечный диастолический объем левого желдудочка, мл (норма до 104.0 мл)', min_value=None, max_value=None, value=lv_dvol, 
                                       step=1.0, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    
    svol = st.number_input('Конечный систолический объем левого желдудочка, мл (норма до 49.0 мл)', min_value=None, max_value=None, value=lv_svol, 
                                       step=1.0, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")

    bv_simpson = round((dvol - svol), 0)
       
    ef_sim = bv_simpson / dvol
    
    try:
        lv_dv_body_area = round(lv_dvol / body_area, 0)
        lv_dv_area = st.caption('КДО/ППТ ' + str(lv_dv_body_area) + ' мл/м2 (норма менее 75.0 мл/м2)')
    except:
        lv_dv_body_area = None
    
    try:
        ef_sim = round((ef_sim * 100), 0)
        bv_s = st.caption('ударный объем ' + str(bv_simpson) + ' мл')
        ef_s = st.caption('фракция выброса по Симпсону ' + str(round(ef_sim)) + ' % (норма – более 50.0 %)')
    except:
        ef_t = None
        
    lvaw = st.number_input('Толщина межжелудочковой перегородки в PLAX, см (норма до 1.1 см)', min_value=None, max_value=None, value=1.0, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=0.9, disabled=False, label_visibility="visible")
        
    lvpw = st.number_input('Толщина задней стенки левого желудочка в PLAX, см (норма до 1.1 см)', min_value=None, max_value=None, value=1.0, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=0.9, disabled=False, label_visibility="visible")
    
    myocard_mass = 0.8 * (1.04 * (lvaw + lv + lvpw)**3 - lv**3) + 0.6 
    
    mass_index = myocard_mass / body_area
    
    try:
        mass_miocard = st.caption('Масса миокарда левого желудочка ' + str(round(myocard_mass, 0)) + ' г (норма -   женщины менее 162.0 г, мужчины менее 224.0 г). ')
    except:
        mass_miocard = None
    
    try:
        mass_miocard_index = st.caption('ИММЛЖ ' + str(round(mass_index, 1)) + ' г/м2 (норма -   женщины менее 95.0 г/м2, мужчины менее 115.0 г/м2). ')
    except:
        mass_miocard_index = None

    st.write('')
    st.write('')
    st.write('*Правое пресердие*')
                
    ra_hor = st.number_input('Правое предсердие в A4C - поперечный размер, см (норма до 3.8 см)', min_value=None, max_value=None, value=3.2, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=3.6, disabled=False, label_visibility="visible")
    
    ra_ver = st.number_input('Правое предсердие в A4C - продольный размер, см (норма до 4.6 см)', min_value=None, max_value=None, value=3.8, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=3.6, disabled=False, label_visibility="visible")
        
    st.write('')
    st.write('')
    st.write('*Правый желудочек*')    
        
    rv = st.number_input('Правый желудочек в PLAX, см (норма до 2.9 см)', min_value=None, max_value=None, value=2.4, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=2.6, disabled=False, label_visibility="visible")
    
    rv_check = st.checkbox('Дополнительные размеры правого желудочка')
    
    if rv_check:
        rv1 = st.number_input('Базальны размер правого желудочка в A4C, см (норма до 2.8 см)', min_value=None, max_value=None, value=2.0, 
                                          step=0.1, format=None, key=None, help=None, on_change=None, 
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        rv2 = st.number_input('Срединный размер правого желудочка в A4C, см (норма до 2.8 см)', min_value=None, max_value=None, value=2.2, 
                                          step=0.1, format=None, key=None, help=None, on_change=None, 
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        rv3 = st.number_input('Продольный размер правого желудочка в A4C, см (норма до 7.9 см)', min_value=None, max_value=None, value=6.2, 
                                          step=0.1, format=None, key=None, help=None, on_change=None, 
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        rv_et = st.number_input('Выносящий тракт правого желудочка в PSAX, см (норма до 3.3 см)', min_value=None, max_value=None, value=2.9, 
                                          step=0.1, format=None, key=None, help=None, on_change=None, 
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    else:
        rv1 = 0
        rv2 = 0
        rv3 = 0
        rv_et = 0
        
    rv_wall = st.number_input('Тощина стенки правого желудочка в PLAX, см (норма до 0.4 см)', min_value=None, max_value=None, value=0.4, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=2.6, disabled=False, label_visibility="visible")
    
    
    st.write('')
    st.write('')
    st.write('*Легочная артерия*')  
        
    pa = st.number_input('Диаметр легочной артерии в PSAX, см (норма до 2.9 см)', min_value=None, max_value=None, value=1.8, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=1.8, disabled=False, label_visibility="visible")
        
    st.write('')
    st.write('')
    st.write('*Нижняя полая вена*')    

    cv = st.number_input('Диаметр нижней полой вены, см (норма менее 2.5 см)', min_value=0.2, max_value=None, value=1.2, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=1.0, disabled=False, label_visibility="visible")
    
    cv_colab = st.selectbox('Коллабирует на вдохе ', lists['нпв'])

    st.write('')
    st.write('')
    st.write('*Систолическая и диастолическая функция желудочков*')  
    
    if rythm == 'фибрилляция предсердий':
        defalt_value_segments = lists['сегменты'][1]
    else:
        defalt_value_segments = lists['сегменты'][0]
    
    segments =  st.multiselect('Зоны нарушения локальной сократимости стенок левого желудочка', 
                               lists['сегменты'], default=defalt_value_segments, key=None, help=None, on_change=None, args=None, kwargs=None, max_selections=None, placeholder='Выберите несколько вариантов', disabled=False, label_visibility="visible")
    
    sg = ''
    
    for seg in segments:
        sg += seg
    
    segments_str = st.text_area('Зоны нарушения локальной сократимости стенок левого желудочка \n(нажмите ctrl + enter для подтверждения изменений)', value=sg, 
                        height=None, max_chars=None, key=None, help=None, on_change=None, 
                        args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    
    ef_select = st.radio('Систолическая функция левого желудочка', ['Тейхольц', 'Симпсон'], index=1, 
                         key=None, help=None, on_change=None, args=None, kwargs=None,
                         disabled=False, horizontal=True, captions=None, label_visibility="visible")
    
    if ef_select == 'Тейхольц':
        st.caption('Ударный объем ' + str(bv_teih) + ' мл')
        st.caption('Фракция выброса левого желудочка по Тейхольцу ' + str(ef_teih) + ' % (норма – более 55.0%)')
        ef_report = 'Ударный объем ' + str(bv_teih) + ' мл. Фракция выброса левого желудочка по Тейхольцу ' + str(ef_teih) + ' % (норма – более 55.0 %). '
        teih = round(ef_teih, 0)
        sim = 0
    else:
        st.caption('Ударный объем ' + str(bv_simpson) + ' мл')
        st.caption('Фракция выброса левого желудочка по Симпсону ' + str(round(ef_sim, 0)) + ' % (норма – более 50.0 %)')
        ef_report = 'Ударный объем ' + str(bv_simpson) + ' мл. Фракция выброса левого желудочка по Симпсону ' + str(ef_sim) + ' % (норма – более 50.0 %). '
        sim = round(ef_sim, 0)
        teih = 0

    rv_ef_check = st.checkbox('Систолическая функция правого желудочка')
    
    if rv_ef_check:
        rv_ef = st.number_input('Систолическая экскурсия кольца трикуспидального клапана (TAPSE), норма более 17.0 мм ', min_value=None, max_value=None, value=19.0, 
                                          step=1.0, format=None, key=None, help=None, on_change=None,                                           
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    else:
        rv_ef = 0

    if rythm == 'синусовый':
        e_peak = st.number_input('Трансмитральный поток - пик Е, см/с', min_value=None, max_value=None, value=46.0, 
                                           step=2.0, format=None, key=None, help=None, on_change=None, 
                                           args=None, kwargs=None, placeholder=3.6, disabled=False, label_visibility="visible")
        
        a_peak = st.number_input('Трансмитральный поток - пик А, см/с', min_value=None, max_value=None, value=77.0, 
                                           step=2.0, format=None, key=None, help=None, on_change=None, 
                                           args=None, kwargs=None, placeholder=3.6, disabled=False, label_visibility="visible")
        
        ea = e_peak / a_peak
        
        ea_report = st.caption('Отношение: пик Е / пик А = ' + str(round(ea, 2)))
        
        if ea > 2.0:
            df = st.caption('Нарушение диастолической функции левого желудочка по рестриктивному типу')
            diastola = 'Нарушение диастолической функции левого желудочка по рестриктивному типу'
        elif ea < 0.8:
            df = st.caption('Нарушение диастолической функции левого желудочка по 1 типу (нарушение релаксации)')
            diastola = 'Нарушение диастолической функции левого желудочка по 1 типу (нарушение релаксации)'
        elif ea > 0.8 and ea <2.0 and la_volume_index > 28.0:
            df = st.caption('Нарушение диастолической функции левого желудочка по типу псевдонормализации')
            diastola = 'Нарушение диастолической функции левого желудочка по типу псевдонормализации'
        else:
            df = st.caption('Диастолическая функция левого желудочка не нарушена')
            diastola = 'Диастолическая функция левого желудочка не нарушена'
    else:
        e_peak = 0
        a_peak = 0
        ea = 0
        
    st.write('')
    st.write('')
    st.write('*Клапанный аппарат*')
    
    av = st.text_area('Аорталный клапан (нажмите ctrl + enter для подтверждения изменений)', value='трехстворчатый, створки уплотнены, движение створок не ограничено ', 
                        height=25, max_chars=None, key=None, help=None, on_change=None, 
                        args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    av_open = st.number_input('Раскрытие аортального клапана в PLAX, см', min_value=None, max_value=None, value=1.9, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    av_pg = st.number_input('Pg макс. на аортальном клапане в A4C, мм.рт.ст. ', min_value=None, max_value=None, value=4.3, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    av_check = st.checkbox('Аортальный клапан - дополнительно')
    
    if av_check:
        av_pg_mean = st.number_input('Pg ср. на аортальном клапане в А4С, мм.рт.ст.', min_value=None, max_value=None, value=19.0, 
                                          step=0.1, format=None, key=None, help=None, on_change=None,                                           
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        av_vti = st.number_input('Интеграл скорости кровотока на аортальном клапане в А4С, см', min_value=None, max_value=None, value=3.0, 
                                          step=0.1, format=None, key=None, help=None, on_change=None,                                           
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        av_lvot = st.number_input('Диаметр выносящего тракта левого желудочка в А4С, см', min_value=None, max_value=None, value=1.0, 
                                          step=0.1, format=None, key=None, help=None, on_change=None,                                           
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        lvot_vti = st.number_input('Итеграл скорости кровотока в выносящем тракте левого желудочка в А4С, см', min_value=None, max_value=None, value=2.0, 
                                          step=0.1, format=None, key=None, help=None, on_change=None,                                           
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        s_av = av_lvot**2 * 0.7854 * lvot_vti / av_vti 
        
        s_av_report = st.caption('Площадь аортального клапана ' + str(round(s_av, 2)) + ' см2')
                
    else:
        av_pg_mean = 0
        av_vti = 0
        av_lvot = 0
        lvot_vti = 0
        s_av = 100

    ar = st.number_input('Аортальная регургитация, степень (1-2ст = 1.5ст)', min_value=0.0, max_value=3.0, value=0.0, 
                                       step=0.5, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=0.0, disabled=False, label_visibility="visible")
           
    st.write('')
    st.write('')
    st.write('')
    
    mv = st.text_area('Митральный клапан (нажмите ctrl + enter для подтверждения изменений)', value='створки уплотнены, движение створок разнонаправленное, в противофазе, не ограничено', 
                        height=25, max_chars=None, key=None, help=None, on_change=None, 
                        args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    mv_check = st.checkbox('Митральный клапан - дополнительно')
    
    
    if mv_check:
        mv_pg_max = st.number_input('Pg макс. на митрально клапане в А4С, мм.рт.ст.', min_value=None, max_value=None, value=7.0, 
                                          step=0.1, format=None, key=None, help=None, on_change=None,                                           
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        s_mv = st.number_input('Площадь митрального клапана планиметрически в PSAX, см2', min_value=None, max_value=None, value=4.0, 
                                          step=0.1, format=None, key=None, help=None, on_change=None,                                           
                                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    else:
        mv_pg_max = 0
        s_mv = 100
    
    mr = st.number_input('Митральная регургитация, степень (1-2ст = 1.5ст)', min_value=0.0, max_value=3.5, value=1.0, 
                                       step=0.5, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=1.0, disabled=False, label_visibility="visible")
    
    st.write('')
    st.write('')
    st.write('')
        
    tv = st.text_area('Трикуспидальный клапан (нажмите ctrl + enter для подтверждения изменений)', value='створки не изменены, движение не ограничено', 
                        height=25, max_chars=None, key=None, help=None, on_change=None, 
                        args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
    tr = st.number_input('Трикуспидальная регургитация, степень (1-2ст = 1.5ст)', min_value=0.0, max_value=3.5, value=1.0, 
                                       step=0.5, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")

    st.write('')
    st.write('')
    st.write('')
    
    
    lval = st.text_area('Клапан легочной артерии (нажмите ctrl + enter для подтверждения изменений)', value='створки не изменены, движение не ограничено', 
                        height=25, max_chars=None, key=None, help=None, on_change=None, 
                        args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    lval_pg = st.number_input('Pg max', min_value=None, max_value=None, value=4.1, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
    lr = st.number_input('Регургитация на клапане легочной артерии, степень (1-2ст = 1.5ст)', min_value=0.0, max_value=4.0, value=0.5, 
                                       step=0.5, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
    la_pressure_check = st.checkbox('Определение давления в легочной артерии затруднено')
    
    if la_pressure_check:    
        la_pressure = st.caption('определение давления в легочной артерии затруднено ввиду низкого качества эхосигнала трикуспиальной регургитации')
    else:        
        la_pressure = st.number_input('Расчетное давление в легочной артерии, мм.рт.ст.', min_value=0.0, max_value=None, value=18.0, 
                                       step=1.0, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
       
    st.write('')
    st.write('')
    st.write('')
    
    pericard_check = st.checkbox('Жидкость в полости перикарда')
    
    if pericard_check:
        pericard_pw = st.number_input('За задней стенкой левого желудочка - эхонегативное пространство до, см', min_value=0.0, max_value=None, value=0.6, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        pericard_rv = st.number_input('За правым желудочком - эхонегативное пространство до, см', min_value=0.0, max_value=None, value=0.4, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        pericard_ra = st.number_input('За правым предсердием - эхонегативное пространство до, см', min_value=0.0, max_value=None, value=0.5, 
                                       step=0.1, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    else:        
        pericard = st.caption('Свободная жидкость в полости перикарда не выявлена')
        pericard_pw = 0
        pericard_rv = 0
        pericard_ra = 0
        
    pleura_check = st.checkbox('Жидкость в плевральных полостях')
    
    if pleura_check:
        right_pleura = st.number_input('В правой плевральной полости - эхонегативное пространство до, см', min_value=0.0, max_value=None, value=0.5, 
                                       step=0.5, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
        
        left_pleura = st.number_input('В левой плевральной полости - эхонегативное пространство до, см', min_value=0.0, max_value=None, value=0.5, 
                                       step=0.5, format=None, key=None, help=None, on_change=None, 
                                       args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    else:
        right_pleura = 0
        left_pleura = 0

    also = st.text_area('Дополнительные сведения (нажмите ctrl + enter для подтверждения изменений)', value='', 
                        height=None, max_chars=None, key=None, help=None, on_change=None, 
                        args=None, kwargs=None, placeholder='Всё, что не вошло в стандартный протокол', disabled=False, label_visibility="visible")



# NETWORK PREDICTION =======================================================================================================================================================

    st.write('')
    st.write(':fire: :fire: :fire:')
        
    # Preprocessing variables
    
    try:
        ao1 = (ao - 1.8) / (5.4 - 1.8)
        la1 = (la - 2.4) / (7.8 - 2.4)
        lv1 = (lv - 2.4) / (8.1 - 2.4)
        rv1 = (rv - 1.5) / (4.8 - 1.5)
        ra1 = (ra_hor - 2.3) / (6.0 - 2.3)
        pa1 = (pa - 1.0) / (3.6 - 1.0)
        lvaw1 = (lvaw - 0.7) / (2.6 - 0.7)
        lvpw1 = (lvpw - 0.7) / (2.2 - 0.7)
        ef1 = (ef - 18.0) / (75.0 - 18.0)
        ar1 = (ar - 0) / (2.5 - 0)
        mr1 = (mr - 0) / (3.5 - 0)
        tr1 = (tr - 0) / (3.5 - 0)
        cv1 = (cv - 0) / (3.5 - 0)
    
    
    # Prediction
    
        pred = pd.DataFrame([ao1, la1, lv1, rv1, ra1, pa1, lvaw1, lvpw1, ef1, ar1, mr1, tr1, cv1])
        x = pred.T
    
        probs = model.predict_proba(x)
    
        report = probs[:,1][:]
        
    except:
        pass
    
    
    try:
        if float(report[0]) >= 0.85:
            pred = 'высокая вероятность фибрилляции предсердий'
        elif float(report[0]) >= 0.50:
            pred = 'умеренная вероятность фибрилляции предсердий'
        else:
            pred = 'низкая вероятность фибрилляции предсердий'
    except:
        pred = 'Недостаточно данных для прогноза'
        st.markdown('Недостаточно данных для прогноза')

    nw = 'Эхокардиография соответствует структуре и функции сердца при фибрилляции предсердий на ' + str(round(float(report[0])*100, 2)) + ' % (' + pred + ').'
    
    network_to_report_check = st.checkbox('Включить прогноз нейросети в отчет')
    
    if network_to_report_check:
        nw_report = nw
    else:
        nw_report = ''
        
    st.write(nw)
        
    st.write('')
    st.write('')
    st.write('')
    
    

    
    # AUTOREPORT =======================================================================================================================================================   
    
    st.subheader('Заключение')
    
    
    # Vascs and valvs - autoreport
    
    if ao_wall == 'не изменена':
        vascs = ['']
    else:
        vascs = ['Уплотнение стенок аорты, створок аортального и митрального клапанов. ']
    
        
    # Cambers - autorepotr
    
    if ao_vals > 4.0 and ao > 3.9:
        defolt_ao = lists['аорта'][4]
    elif ao_vals > 4.0:
        defolt_ao = lists['аорта'][2]
    elif ao > 3.9:
        defolt_ao = lists['аорта'][3]
    else:
        defolt_ao = ''
    
    if (la > 4.0 or la_a4c_hor > 4.5 or la_a4c_ver > 5.3) and lv > 5.6 and (ra_hor > 3.8 or ra_ver > 4.6) and rv > 2.9:
        defolt_chambers = lists['камеры'][4]
    elif (la > 4.0 or la_a4c_hor > 4.5 or la_a4c_ver > 5.3) and lv > 5.6 and (ra_hor > 3.8 or ra_ver > 4.6):
        defolt_chambers = lists['камеры'][5]
    elif (la > 4.0 or la_a4c_hor > 4.5 or la_a4c_ver > 5.3) and (ra_hor > 3.8 or ra_ver > 4.6) and rv > 2.9:
        defolt_chambers = lists['камеры'][6]
    elif (la > 4.0 or la_a4c_hor > 4.5 or la_a4c_ver > 5.3) and lv > 5.6 and rv > 2.9:
        defolt_chambers = lists['камеры'][7]
    elif lv > 5.8 and (ra_hor > 3.8 or ra_ver > 4.6) and rv > 2.9:
        defolt_chambers = lists['камеры'][8]
    elif (la > 4.0 or la_a4c_hor > 4.5 or la_a4c_ver > 5.3) and lv > 5.8:
        defolt_chambers = lists['камеры'][9]
    elif (ra_hor > 3.8 or ra_ver > 4.6) and rv > 2.9:
        defolt_chambers = lists['камеры'][10]
    elif (la > 4.0 or la_a4c_hor > 4.5 or la_a4c_ver > 5.3) and (ra_hor > 3.8 or ra_ver > 4.6):
        defolt_chambers = lists['камеры'][11]
    elif (la > 4.0 or la_a4c_hor > 4.5 or la_a4c_ver > 5.3):
        defolt_chambers = lists['камеры'][12]
    elif lv > 5.8:
        defolt_chambers = lists['камеры'][13]
    elif (ra_hor > 3.8 or ra_ver > 4.6):
        defolt_chambers = lists['камеры'][14]
    elif rv > 2.9:
        defolt_chambers = lists['камеры'][15]
    else:
        defolt_chambers = lists['камеры'][0]


    if la_volume_index > 28.0:
        defolt_la_volume = lists['камеры'][1]
    else:
        defolt_la_volume = ''
    
    if pa > 2.9:
        defolt_pa = lists['камеры'][2]
    else:
        defolt_pa = ''
        
    if cv > 2.5:
        defolt_cv = lists['камеры'][3]
    else:
        defolt_cv = ''
        
    
    cambers = [defolt_ao, defolt_chambers, defolt_la_volume, defolt_pa, defolt_cv]
    
    
    # Walls - autoreport

    if lvaw > 2.0:
        defolt_a_wall = lists['стенки'][5]
    elif lvaw > 1.5:
        defolt_a_wall = lists['стенки'][3]
    elif lvaw > 1.1:
        defolt_a_wall = lists['стенки'][1]
    else:
        defolt_a_wall = ''
        
    if lvpw > 2.0:
        defolt_p_wall = lists['стенки'][6]
    elif lvpw > 1.5:
        defolt_p_wall = lists['стенки'][4]
    elif lvpw > 1.1:
        defolt_p_wall = lists['стенки'][2]
    else:
        defolt_p_wall = ''
        
    if rv_wall > 0.4:
        defolt_rv_wall = lists['стенки'][7]
    else:
        defolt_rv_wall = ''

    if defolt_a_wall == '' and defolt_p_wall == '' and defolt_rv_wall == '':
        defolt_walls = lists['стенки'][0]
    else:
        defolt_walls = ''
        
    if round(mass_index, 1) > 115.0:
        defolt_mass = lists['стенки'][8]
    else:
        defolt_mass = ''

    walls = [defolt_walls, defolt_a_wall, defolt_p_wall, defolt_rv_wall, defolt_mass]
    
        
    # Kinetic - autoreport
    
    kinetik = ['Зоны нарушения локальной сократимости миокарда: ', segments_str, '. ']
        
    
    # EF - autoreport
    
    if teih >= 55.0 or sim >= 50.0:
        defalt_ef = lists['систола'][0]
    elif teih >= 40.0 or sim >= 40.0:
        defalt_ef = lists['систола'][1]
    elif teih >= 30.0 or sim >= 30.0:
        defalt_ef = lists['систола'][2]
    elif teih < 30.0 or sim < 30.0:
        defalt_ef = lists['систола'][3]

    systolyc_function = list(defalt_ef)

    
    # Diastolic - autoreport
    
    if rythm == 'синусовый':
    
        dyastolic_function = [diastola, '. ']
   
    else:
        dyastolic_function = ['Диастолическая функция не определена ввиду отсутствия устойчивого синусового ритма. ']
        
        
    # Valvs_functon - autoreport
     
    if av_pg_mean >= 40.0:
        defolt_as = lists['стенозы'][2]
    elif av_pg_mean >= 30.0:
        defolt_as = lists['стенозы'][1]
    elif av_pg_mean >= 20.0:
        defolt_as = lists['стенозы'][0]
    else:
        defolt_as = ''   
        
    if mv_check == True:   
        if s_mv <= 1.6:
            defolt_ms = lists['стенозы'][5]
        elif s_mv <= 2.2:
            defolt_ms = lists['стенозы'][4]
        elif s_mv <= 3.0:
            defolt_ms = lists['стенозы'][3]
        else:
            defolt_ms = ''
    else:
        defolt_ms = ''
    
    if ar == 0.0:
        defolt_av = ''
    elif ar == 0.5:
        defolt_av = lists['клапаны'][1]
    elif ar == 1.0:
        defolt_av = lists['клапаны'][2]
    elif ar == 1.5:
        defolt_av = lists['клапаны'][3]
    elif ar == 2.0:
        defolt_av = lists['клапаны'][4]
    elif ar == 2.5:
        defolt_av = lists['клапаны'][5]
    elif ar == 3.0:
        defolt_av = lists['клапаны'][6]
    
    if mr < 1.5:
        defolt_mv = ''
    elif mr == 1.5:
        defolt_mv = lists['клапаны'][7]
    elif mr == 2.0:
        defolt_mv = lists['клапаны'][8]
    elif mr == 2.5:
        defolt_mv = lists['клапаны'][9]
    elif mr == 3.0:
        defolt_mv = lists['клапаны'][10]
    elif mr == 3.5:
        defolt_mv = lists['клапаны'][11]
        
    if tr < 1.5:
        defolt_tv = ''
    elif tr == 1.5:
        defolt_tv = lists['клапаны'][12]
    elif tr == 2.0:
        defolt_tv = lists['клапаны'][13]
    elif tr == 2.5:
        defolt_tv = lists['клапаны'][14]
    elif tr == 3.0:
        defolt_tv = lists['клапаны'][15]
    elif tr == 3.5:
        defolt_tv = lists['клапаны'][16]
    
    if lr < 1.5:
        defolt_lv = ''
    elif lr == 1.5:
        defolt_lv = lists['клапаны'][17]
    elif lr == 2.0:
        defolt_lv = lists['клапаны'][18]
    elif lr == 2.5:
        defolt_lv = lists['клапаны'][19]
    elif lr == 3.0:
        defolt_lv = lists['клапаны'][20]
    elif lr == 3.5:
        defolt_lv = lists['клапаны'][21]
        
    if defolt_as == '' and defolt_ms == '' and defolt_av == '' and defolt_mv == '' and defolt_mv == '' and defolt_lv == '':
        defolt_norm = lists['клапаны'][0]
    else:
        defolt_norm = ''
    
    valvs = [defolt_as, defolt_ms, defolt_av, defolt_mv, defolt_tv, defolt_lv, defolt_norm]    
    
    
    # Pulmonary_pressure autoreport
    
    if la_pressure_check == False:
        if la_pressure >= 70:
            defolt_la_pressure = lists['прочее'][2]
        elif la_pressure >= 50:
            defolt_la_pressure = lists['прочее'][1]
        elif la_pressure >=30:
            defolt_la_pressure = lists['прочее'][0]
        else:
            defolt_la_pressure = ''
    else:
        defolt_la_pressure = 'Определение давления в легочной артерии затруднено. '
        
        
    # Hydropericard autoreport
    
    if pericard_check == True:
        if pericard_pw > 2.0 or pericard_rv > 2.0 or pericard_ra > 2.0:
            defolt_pericard = lists['прочее'][8]
        elif pericard_pw > 1.0 or pericard_rv > 1.0 or pericard_ra > 1.0:
            defolt_pericard = lists['прочее'][7]
        elif pericard_pw > 5.0 or pericard_rv > 0.0 or pericard_ra > 0.0:
            defolt_pericard = lists['прочее'][6]
        else:
            defolt_pericard = ''
    else:
        defolt_pericard = ''
        
        
    # Hydrothorax autoreport
    
    if pleura_check == True:
        if left_pleura > 0.5 and right_pleura > 0.5:
            defolt_pleura = lists['прочее'][3]
        elif left_pleura > 0.5 and right_pleura == 0.5:
            defolt_pleura = lists['прочее'][4]
        elif left_pleura == 0.5 and right_pleura > 0.5:
            defolt_pleura = lists['прочее'][5]
        else:
            defolt_pleura = ''
    else:
        defolt_pleura = ''
    
    others = [defolt_la_pressure, defolt_pericard, defolt_pleura]
    
    
    report_data = vascs + cambers + walls + kinetik + systolyc_function + dyastolic_function + valvs + others + [also]
    
    rp = ''
    
    for rep in report_data:
        rp += rep
   
    report = rp
    
    # report_str = st.text_area('Заключение (нажмите ctrl + enter для подтверждения изменений)', value=report, 
    #                     height=300, max_chars=None, key=None, help=None, on_change=None, 
    #                     args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
    
        

# TEXT REPORT ================================================================================================================================================================================


    # Main data    

    if name == None:
        name_report = ''
    else:
        name_report = name
        
    if ao_wall == None:
        ao_wall_report = ''
    else:
        ao_wall_report = 'Стенка аорты ' + str(ao_wall) + '. ' 
        
    if ao_vals == None:
        ao_vals_report = ''
    else:
        ao_vals_report = 'Аорта на уровне с. Вальсальвы ' + str(round(ao_vals, 1)) + ' см (норма до 4.0 см). ' 

    if ao == None:
        ao_report = ''
    else:
        ao_report = 'Восходящий отдел аорты ' + str(round(ao, 1)) + ' см (норма до 3.8 см). ' 
        
        
    if la == None:
        la_report = ''
    else:
        la_report = 'Левое предсердие в PLAX ' + str(round(la, 1)) + ' см (норма до 4.0 см). '
        
    if la_a4c_ver == None or la_a4c_hor == None:
        la_a4c_report = ''
    else:
        la_a4c_report = 'Левое предсердие апикально ' + str(round(la_a4c_hor, 1)) + ' x ' + str(round(la_a4c_ver, 1)) + ' см (норма до 4.5 х 5.3 см). '
        
    if la_volume == None:
        la_volume_report = ''
    else:
        la_volume_report = 'Объем левого предсердия по Симпсону ' + str(round(la_volume, 1)) + ' мл (норма до 52.0 мл). '
        
    if la_volume_index == None:
        la_index_report = ''
    else:
        la_index_report = 'Индекс объема левого предсердия ' + str(round(la_volume_index, 1)) + ' мл/м2 (норма до 28.0 мл/м2). '
        
    if lv == None:
        lv_report = ''
    else:
        lv_report = 'Конечный диастолический размер левого желудочка ' + str(round(lv, 1)) + ' см (норма до 5.8 см). '
        
    if lv_sv == None:
        lv_sv_report = ''
    else:
        lv_sv_report = 'Конечный систолический размер левого желудочка ' + str(round(lv_sv, 1)) + ' см (норма до 2.8 см). '
        
    if dvol == None:
        dvol_report = ''
    else:
        dvol_report = 'Конечный диастолический объем левого желудочка ' + str(round(dvol, 0)) + ' мл (норма до 104.0 мл). '
        
    if svol == None:
        svol_report = ''
    else:
        svol_report = 'Конечный систолический объем левого желудочка ' + str(round(svol, 0)) + ' мл (норма до 49.0 мл). '
        
    if lv_dv_body_area == None:
        lv_dv_body_area_report = ''
    else:
        lv_dv_body_area_report = 'Отношение конечного диастолического объема левого желудочка к площади поверхности тела ' + str(round(lv_dv_body_area, 2)) + ' мл/м2 (норма менее 75.0 мл/м2). '
        
    if lvaw == None:
        lvaw_report = ''
    else:
        lvaw_report = 'Толщина межжелудочковой перегородки ' + str(round(lvaw, 1)) + ' см (норма до 1.1 см). '   

    if lvpw == None:
        lvpw_report = ''
    else:
        lvpw_report = 'Толщина задней стенки левого желудочка ' + str(round(lvpw, 1)) + ' см (норма до 1.1 см). '  
        
    if myocard_mass == None:
        myocard_mass_report = ''
    else:
        myocard_mass_report = 'Масса миокарда левого желудочка ' + str(round(myocard_mass, 1)) + ' г (норма -   женщины менее 162.0 г, мужчины менее 224.0 г). '  

    if mass_miocard_index == None:
        mass_miocard_index_report = ''
    else:
        mass_miocard_index_report = 'Индекс массы миокарда левого желудочка ' + str(round(mass_index, 1)) + ' г/м2 (норма -   женщины менее 95.0 г/м2, мужчины менее 115.0 г/м2). '  

    if ra_hor == None or ra_ver == None:
        ra_report = ''
    else:
        ra_report = 'Правое предсердие апикально ' + str(round(ra_hor, 1)) + ' x ' + str(round(ra_ver, 1)) + ' см (норма до 3.8 х 4.6 см). '
        
    if rv == None:
        rv_report = ''
    else:
        rv_report = 'Размер правого желудочка в PLAX ' + str(round(rv, 1)) + ' см (норма до 2.9 см). '
        
    if rv_wall == None:
        rv_wall_report = ''
    else:
        rv_wall_report = 'Толщина стенки правого желудочка в PLAX ' + str(round(rv_wall, 1)) + ' см (норма до 0.4 см). '
        
    try:
        check_rv_report = 'Базальный размер правого желудочка ' + str(round(rv1, 1)) + ' см (норма до 2.8 см). Срединный размер правого желудочка ' + str(round(rv2, 1)) + ' см (норма до 2.8 см). Продольный размер правого желудочка ' + str(round(rv3, 1)) + ' см (норма до 7,9 см). Диаметр выносящего тракта правого желудочка ' + str(round(rv_et, 1)) + ' см (норма до 3.3 см). '
    except:
        check_rv_report = ''
        
    if pa == None:
        pa_report = ''
    else:
        pa_report = 'Диаметр легочной артерии в PSAX ' + str(round(pa, 1)) + ' см (норма до 2.9 см). '
        
    if cv == None:
        cv_report = ''
    else:
        cv_report = 'Диаметр нижней полой вены ' + str(round(cv, 1)) + ' см (норма до 2.5 см). '
        
    if cv_colab == None:
        cv_colab_report = ''
    else:
        cv_colab_report = ' Коллабирование нижней полой вены на вдохе: ' + cv_colab + ' (норма - более 50%). '
        
    if segments_str == None:
        segments_str_report = ''
    else:
        segments_str_report = 'Зоны нарушения локальной сократимости: ' + str(segments_str) + '. '
    
    try:
        rv_ef_report = 'Систолическая экскурсия кольца трикуспидального клапана (TAPSE) ' + str(round(rv_ef, 1)) + ' мм (норма - более 17.0 мм). '
    except:
        rv_ef_report = ''
    
    try:
        ea_report = 'Трансмитральный поток: пик Е = ' + str(round(e_peak, 0)) + ' см/с, пик А = ' + str(round(a_peak, 0)) + ' см/с, отношение Е/А = ' + str(round(ea, 2))
    except:
        ea_report = 'Диастолическая функция левого желудочка не определеяется ввиду отсутствия устойчивого синусового ритма. '
        
    try:
        av_report = 'Аортальный клапан: ' + av + '. Раскрытие аортального клапана в PLAX ' + str(round(av_open, 1)) + ' см. ' + 'Pg макс. ' + str(round(av_pg, 1)) + ' мм.рт.ст.. '
    except:
        av_report = ''
        
    try:
        av_stenose_report = 'Pg ср. ' + str(round(av_pg_mean, 1)) + ' мм.рт.ст.. Площадь аортального клапана (расчетная) ' +  str(round(s_av, 2)) + ' см2. '
    except:
       av_stenose_report = '' 
        
    if ar == None:
        ar_report = ''
    else:
        ar_report = 'Аортальная регургитация ' + str(ar) + ' ст.. ' 
        
    try:
        mv_report = 'Митральный клапан: ' + mv + '. '
    except:
        mv_report = ''
    
    try:
        mv_stenose_report = 'Pg макс. на митральном клапане в A4C ' + str(round(mv_pg_max, 1)) + ' мм.рт.ст.. '
    except:
        mv_stenose_report = ''
    
    try:
        s_mv_report = 'Площадь митрального клапана планиметрически в PSAX ' + str(round(s_mv, 1)) + ' см2. '
    except:
        s_mv_report = ''

    if mr == None:
         mr_report = ''
    else:
         mr_report = 'Митральная регургитация ' + str(mr) + ' ст.. ' 
         
    if tv == None:
         tv_report = ''
    else:
         tv_report = tv + '. '
         
    if tr == None:
         tr_report = ''
    else:
         tr_report = 'Трикуспидальная регургитация ' + str(tr) + ' ст.. '
        
    if lval == None:
         lval_report = ''
    else:
         lval_report = 'Клапан легочной артерии: ' + lval + '. '
         
    if lval_pg == None:
         lval_pg_report = ''
    else:
         lval_pg_report = 'Pg макс. на клапане легочной артерии ' + str(round(lval_pg, 1)) + ' мм.рт.ст.. '
         
    if lr == None:
         lr_report = ''
    else:
         lr_report = 'Регургитация на клапане легочной артерии ' + str(round(lr, 1)) + ' ст.. '
    
    if la_pressure_check == False:
        la_pressure_report = 'Расчетное давление в легочной артерии ' + str(round(la_pressure, 0)) + ' мм.рт.ст.. '
    else:
        la_pressure_report = 'Определение давления в легочной артерии затруднено ввиду низкого качества сигнала трикуспидальной регургитации. '
    
    if pericard_check == True:
        pericard_report = 'В полости перикарда определяется эхонегативное пространство - за задней стенкой левого желудочка до ' + str(round(pericard_pw, 1)) + ' см, за правым желудочком - до ' + str(round(pericard_rv, 1)) + ' см, за правым предсердием - до ' + str(round(pericard_ra, 1)) + ' см в диастолу. '
    else:
        pericard_report = 'Признаков свободной жидкости в полости перикарда не выявлено. '

    if pleura_check == True:
        pleura_report = 'В правой плевральной полости - эхонегативное пространство до ' + str(round(right_pleura, 1)) + ' см. В левой плевральной полости - эхонегативное пространство до ' + str(round(left_pleura, 1)) + ' см. '
    else:
        pleura_report = ''

    if also == None:
         other = ''
    else:
         other = also        
    
    # Paragrafs of report
    
    h1 = 'Ф.И.О.: ' + name_report
    h2 = '\nДата рождения: ' + str(dayofbirth) + ' (' + str(age) + ' лет)'
    h3 = '\nРост: ' + str(grow) + ' см. Вес: ' + str(weigt) + ' кг. ППТ: ' + str(body_area) + ' м2.'
    h4 = '\nДата и время исследования: ' + str(date_exam) + ' ' + str(time_exam)
    h5 = '\nАппарат УЗИ: ' + str(machine)
    h6 = '\nОсобенности: ' + exam
    h7 = '\nРитм сердца: ' + rythm
    
    header = h1 + h2 + h3 + h4 + h5 + h6 + h7
    
    st1 = '\n' + ao_vals_report + ao_report + ao_wall_report
    st2 = la_report + la_a4c_report + la_volume_report + la_index_report
    st3 = lv_report + lv_sv_report + dvol_report + svol_report + lv_dv_body_area_report + lvaw_report + lvpw_report + myocard_mass_report + mass_miocard_index_report
    st4 = ra_report
    st5 = rv_report + check_rv_report + rv_wall_report
    st6 = pa_report
    st7 = cv_report + cv_colab_report
    
    structure_data = st1 + st2 + st3 + st4 + st5 + st6 + st7 + '\n'
    
    fd1 = str(segments_str_report)
    fd2 = ef_report
    fd3 = rv_ef_report
    fd4 = ea_report
    
    function_data = fd1 + fd2 + fd3 + fd4 + '\n'
    
    vd1 = av_report + av_stenose_report + ar_report
    vd2 = mv_report + mv_stenose_report + s_mv_report + mr_report
    vd3 = tv_report + tr_report
    vd4 = lval_report + lval_pg_report + lr_report + la_pressure_report
    
    valv_data = vd1 + vd2 + vd3 + vd4
    
    pericard = pericard_report + pleura_report
    
    conclusion = 'ЗАКЛЮЧЕНИЕ\n' + report + '\n\nВрач функциональной диагностики:                                Любавин Александр Владимирович'
        
    report_data = header + '\n\nТРАНСТОРАКАЛЬНАЯ ЭХОКАРДИОГРАФИЯ' + '\n' + structure_data + function_data + valv_data + pericard + other + nw_report + '\n\n' + conclusion
    
     
    # Report to text    

    report_str = st.text_area('Протокол исследования', value=report_data, 
                          height=1400, max_chars=None, key=None, help=None, on_change=None, 
                          args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")




# SAVING DATA ===============================================================================================================================================================

    # Variables_to_saving:
        
    save_id = str(name) + ' ' + str(dayofbirth) + ' иссследование от ' + str(date_exam)
    save_name = str(name)
    save_dayofbirth = str(dayofbirth)
    save_date_exam = str(date_exam)
    save_machine = str(machine)
    save_grow = grow
    save_weigt = weigt
    
    save_copd = copd
    save_cad = cad
    save_af = af
    
    save_exam = str(exam)
    save_rythm = str(rythm)
    
    save_ao_wall = str(ao_wall)
    save_ao_vals = ao_vals
    save_ao = ao
    
    save_la = la
    save_la_a4c_hor = la_a4c_hor
    save_la_a4c_ver = la_a4c_ver
    save_la_volume = la_volume
    save_la_volume_index = la_volume_index
    
    save_lv = lv
    save_lv_sv = lv_sv
    save_lv_dvol = lv_dvol
    save_lv_svol = lv_svol
    
    save_bv_teih = bv_teih
    save_ef_teih = ef_teih
    save_bv_simpson = bv_simpson
    save_ef_sim = ef_sim
    
    save_lvaw = lvaw
    save_lvpw = lvpw
    save_myocard_mass = myocard_mass
    save_mass_index = mass_index
    
    save_ra_hor = ra_hor
    save_ra_ver = ra_ver
    
    save_rv = rv
    save_rv1 = rv1
    save_rv2 = rv2
    save_rv3 = rv3
    save_rv_ef = rv_ef
    save_rv_wall = rv_wall
    
    save_pa = pa
    save_cv = cv
    save_cv_colab = cv_colab
    
    save_segments_str = str(segments_str)
    
    save_e_peak = e_peak
    save_a_peak = a_peak
    save_ea = ea
    
    save_av = str(av)
    save_av_open = av_open
    save_av_pg = av_pg
    save_av_pg_mean = av_pg_mean
    save_av_vti = av_vti
    save_av_lvot = av_lvot
    save_lvot_vti = lvot_vti
    save_s_av = s_av
    save_ar = ar
    
    save_mv = str(mv)
    save_mv_pg_max = mv_pg_max
    save_s_mv = s_mv
    save_mr = mr
    
    save_tv = str(tv)
    save_tr = tr
    
    save_lval = str(lval)
    save_lval_pg = lval_pg
    save_lr = lr
    
    save_la_pressure = la_pressure

    save_pericard = pericard
    save_pericard_pw = pericard_pw
    save_pericard_rv = pericard_rv
    save_pericard_ra = pericard_ra
    
    save_right_pleura = right_pleura
    save_left_pleura = left_pleura
    
    save_also = str(also)
    
    save_predict = float(probs[:,1][:])
    
    save_report_str = str(report_str)
    
# Save data
    
    data.loc[len(data.index )] = [save_id, save_name, save_dayofbirth, save_date_exam, save_machine, save_grow, save_weigt,
                                  save_copd, save_cad, save_af,
                                  save_exam, save_rythm,
                                  save_ao_wall, save_ao_vals, save_ao,
                                  save_la, save_la_a4c_hor, save_la_a4c_ver, save_la_volume, save_la_volume_index,
                                  save_lv, save_lv_sv, save_lv_dvol, save_lv_svol,
                                  save_bv_teih, save_ef_teih, save_bv_simpson, save_ef_sim,
                                  save_lvaw, save_lvpw, save_myocard_mass, save_mass_index,
                                  save_ra_hor, save_ra_ver,
                                  save_rv, save_rv1, save_rv2, save_rv3, save_rv_ef, save_rv_wall,
                                  save_pa, save_cv, save_cv_colab,
                                  save_segments_str,
                                  save_e_peak, save_a_peak, save_ea,
                                  save_av, save_av_open, save_av_pg, save_av_pg_mean, save_av_vti, save_av_lvot, save_lvot_vti, save_s_av, save_ar,
                                  save_mv, save_mv_pg_max, save_s_mv, save_mr,
                                  save_tv, save_tr,
                                  save_lval, save_lval_pg, save_lr,
                                  save_la_pressure,
                                  save_pericard, save_pericard_pw, save_pericard_rv, save_pericard_ra,
                                  save_right_pleura, save_left_pleura,
                                  save_also,
                                  save_predict,
                                  save_report_str]

#    st.write(data)
    
    def save_report():
        data.to_excel('data.xlsx', index=False)
        f = open('C:/Users/Doc/Desktop/tte_max_presision/reports/' + save_id + '.txt', 'w')
        f.write(report)
        f.close()
            
    save_btn = st.button('Сохранить протокол', key=None, help=None, 
                         on_click=save_report(), args=None, kwargs=None, type="secondary", 
                         disabled=False, use_container_width=False)
       
    st.subheader(" ")    
    st.subheader(" ")    
    st.subheader(" ")    
    st.subheader(" ")
    st.subheader(" ")
    st.subheader(" ")    
    
    st.markdown(""" Реализация идеи: научный сотрудник НМИЦ ТПМ А. В. Любавин +7-915-857-88-65 """)
    
if __name__ == "__main__":
    run()
