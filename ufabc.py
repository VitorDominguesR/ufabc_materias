# -*- coding: utf-8 -*-


import json

class materias_feitas():

    def __init__(self, path_file_ficha):
        self.json_file = json.load(open(path_file_ficha))


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
        with open(path_grade) as file_grade:
            grade = [] 
            for line in file_grade:
                line = line.split(';')
                if len(line)> 2:
                    grade.append({'codigo':line[0],'disciplina':line[1], 'categoria':line[3]})

        materias_feitas = json.loads(self.get_all_done())
        covalidacoes = open('covalidacoes', 'r').read()
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
        




materias_ufabc = materias_feitas('ficha.json')

obgri = [x for x in materias_ufabc.compare_with_grade('2017') if (x['categoria']=='Obrigatória' and x['situacao']=='OK')]
not_obg = [x for x in materias_ufabc.compare_with_grade('2017') if (x['categoria']=='Obrigatória' and x['situacao']=='Not OK')]

print("Ok\n\n")
list(map(print, obgri))

print("\n\n\n\nNot Ok\n\n")
list(map(print, not_obg))
print(len(not_obg))

