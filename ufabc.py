# -*- coding: utf-8 -*-


import json
from get_materias_planejadas import returMaterias
import re

class materias_feitas():

    def __init__(self, path_file_ficha):
        self.json_file = json.load(open(path_file_ficha, encoding='utf8'))


    def return_all(self, situacao=None):
        
        materias = []
        for materia in self.json_file:
            if situacao:
                if materia['situacao'] == situacao:
                    materias.append(materia)
            else:
                materias.append(materia)

        return materias

    def get_all_done(self):
        done = self.return_all('Aprovado')
        result = []
        for materias in done:
            result.append({'ano':materias['ano'] , 'codigo':materias['codigo'], 'disciplina':materias['disciplina']})
        return json.dumps(result, ensure_ascii=False)
    
    def compare_with_grade(self, path_grade):
        result = []
        with open(path_grade, encoding='utf-8') as file_grade:
            grade = [] 
            for line in file_grade:
                line = line.split(';')
                if len(line)> 2:
                    grade.append({'codigo':line[0],'disciplina':line[1], 'categoria':line[3]})

        materias_feitas = json.loads(self.get_all_done())
        covalidacoes = open('covalidacoes', 'r', encoding='utf8').read()
        for materia in grade:
            #print(materia)
            aux_result = {'disciplina':materia['disciplina'], 'codigo':materia['codigo'], 'situacao':'', 'categoria':materia['categoria'].strip()}
            if not any(((x['codigo'] == materia['codigo'] or materia['codigo'] in covalidacoes) or x['disciplina']==materia['disciplina']) for x in materias_feitas):
                aux_result['situacao'] = 'Not OK'
                result.append(aux_result)
            else:
                aux_result['situacao'] = 'OK'
                result.append(aux_result)
        
        return sorted(result,key=lambda k: k['categoria'])
    
    def get_obrigatorias(self, path_grade):
        result = {}
        with open(path_grade, encoding='utf-8') as file_grade:
            grade = [] 
            for line in file_grade:
                line = line.split(';')
                if len(line)> 2 and line[3]=='Obrigatória':
                    result[line[0]]=line[1]
        return result        




materias_ufabc = materias_feitas('ficha.json')

ok_sit = [x for x in materias_ufabc.compare_with_grade('2017_bcc') if (x['categoria']=='Obrigatória' and x['situacao']=='OK')]
not_ok_sit = [x for x in materias_ufabc.compare_with_grade('2017_bcc') if (x['categoria']=='Obrigatória' and x['situacao']=='Not OK')]

print("Ok\n\n")
list(map(print, ok_sit))

print("\n\n\n\nNot Ok\n\n")
list(map(print, not_ok_sit))
print(len(not_ok_sit))

materias_ofertadas = returMaterias('matricula_disciplinas_2019.2_turmas_planejadas.pdf').get_materias()
for materia in not_ok_sit:
    #print(materia['codigo'])
    matches = [x for x in materias_ofertadas.keys() if materia['codigo'] in x]
    for match in matches:
        if match is not None and 'diurno' not in materias_ofertadas[match]:# and 'sexta' not in materias_ofertadas[match]:
            value = materias_ofertadas[match]
            horario = re.search('(?:\)\s)(.+)(?:CMCC)', value).group(1).strip()
            materia = re.split('(?<=\))\s', value)[0]
            professor = re.split('\d\s/',value.split('CMCC')[1].strip())[0].replace(' BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO','')
            formatted_str = "Discp.: {0}\nHorário: {1}\nProf.:{2}\n\n".format(materia, horario, professor)
            print(formatted_str)
    
print('Outras'.center(20,'#'))
cod_discp_feitas = {}
for x in json.loads(materias_ufabc.get_all_done()):
    cod_discp_feitas[x['codigo']]=x['disciplina']

for key, value in materias_ofertadas.items():
    if 'CIÊNCIA DA COMPUTAÇÃO' in value and 'diurno' not in value:
        print(value.split('(')[0].strip())