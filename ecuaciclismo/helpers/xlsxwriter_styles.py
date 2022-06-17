estilos = {}
estilos['titulo_reporte']                   = {'font_name': 'Century Gothic','font_size':'12','bottom':1,'top':1,'left':1,'right':1,'align':'center','bold':1}
estilos['subtitulo_izquierda']              = {'font_name': 'Century Gothic','font_size':'11','bottom':1,'top':1,'left':1,'right':1,'align':'left','bold':1}
estilos['subtitulo_centrado']               = {'font_name': 'Century Gothic','font_size':'11','bottom':1,'top':1,'left':1,'right':1,'align':'center','bold':1}
estilos['subtitulo_derecha']                = {'font_name': 'Century Gothic','font_size':'11','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1}
estilos['normal']                           = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1}
estilos['normal_centrado']                  = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'center'}
estilos['normal_derecha']                   = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right'}
estilos['normal_negrita']                   = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'bold':1}
estilos['normal_derecha_negrita']           = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1}
estilos['normal_valor']                     = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','num_format':'#,##0.00'}
estilos['normal_valor_negrita']             = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1,'num_format':'#,##0.00'}
estilos['normal_valor_dolar']               = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','num_format':'$#,##0.00'}
estilos['normal_valor_dolar_negrita']       = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1,'num_format':'$#,##0.00'}
estilos['normal_fecha_hora']                = {'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'num_format': 'd/mm/yyyy hh:mm:ss AM/PM'}

def cargarFormatos(workbook):
    diccionario_formatos = {}
    diccionario_formatos['titulo_reporte']                   = workbook.add_format({'font_name': 'Broadway','bold':1,'font_size':'20','align':'center'})#workbook.add_format({'font_name': 'Arial','font_size':'16','bottom':1,'top':1,'left':1,'right':1,'align':'center','bold':1})
    diccionario_formatos['subtitulo_izquierda']              = workbook.add_format({'font_name': 'Century Gothic','font_size':'11','bottom':1,'top':1,'left':1,'right':1,'align':'left','bold':1})
    diccionario_formatos['subtitulo_centrado']               = workbook.add_format({'font_name': 'Century Gothic','font_size':'11','bottom':2,'top':2,'left':2,'right':2,'align':'center','bold':1})
    diccionario_formatos['subtitulo_derecha']                = workbook.add_format({'font_name': 'Century Gothic','font_size':'11','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1})
    diccionario_formatos['normal']                           = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'left'})
    diccionario_formatos['normal_centrado']                  = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'center'})
    diccionario_formatos['normal_derecha']                   = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right'})
    diccionario_formatos['normal_negrita']                   = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'bold':1})
    diccionario_formatos['normal_derecha_negrita']           = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1})
    diccionario_formatos['normal_valor']                     = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','num_format':'#,##0.00'})
    diccionario_formatos['normal_valor_negrita']             = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1,'num_format':'#,##0.00'})
    diccionario_formatos['normal_valor_dolar']               = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','num_format':'$#,##0.00'})
    diccionario_formatos['normal_valor_dolar_negrita']       = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','bold':1,'num_format':'$#,##0.00'})
    diccionario_formatos['normal_fecha_hora']                = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'num_format': 'd/mm/yyyy hh:mm:ss AM/PM'})
    diccionario_formatos['normal_valor_3_decimales']         = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'right','num_format':'#,###0.000'})
    diccionario_formatos['normal_rojo']                      = workbook.add_format({'font_name': 'Century Gothic','font_size':'10','bottom':1,'top':1,'left':1,'right':1,'align':'left', 'font_color':'red'})
    return diccionario_formatos