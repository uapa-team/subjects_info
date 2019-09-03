import mysql.connector
import os


def make_query(query):
  mydb = mysql.connector.connect(
    host      = os.environ.get('UAPA_HOST'),
    user      = os.environ.get('UAPA_USER'),
    passwd    = os.environ.get('UAPA_PASS'),
    database  = os.environ.get('UAPA_NAME') 
  )
  cursor = mydb.cursor()
  cursor.execute(query)
  result = cursor.fetchall()
  
  return result


def get_dni(username):
  query = 'select dni_persona from rel_estudiante_programa where correo_unal = "{}@unal.edu.co";'
  query = query.format(username)
  result = make_query(query)
  return result[0][0]

def get_subject_name(code):
  query = 'select nombre_materia from v_materias where cod_materia = "{}";'
  query = query.format(code)
  result = make_query(query)
  return result[0][0]