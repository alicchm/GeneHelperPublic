from Bio.Seq import Seq, MutableSeq
import re

class Model():
    def __init__(self):
        self.input_sequence = None
        self.exons = None
        self.translate_range = None
        self.mutations = None

    def to_seq(self, seq):
        #zamienia typ danych z tekstu na Seq (specjalny typ danych biblioteki BioPython)
        return Seq(seq)

    def check_if_correct_format(self, x): 
        #sprawdza czy sekwencja składa się z dozwolonych znaków
        allowed_characters = ['A','T','G','C']
        for i in x.upper():
            if i not in allowed_characters:
                return False
        return True
    
    def is_len_divisible_by_3(self, x): #sprawdza podzielność podanej sekwencji na substringi o dł 3 (kodony)
        if len(x)%3 == 0:
            return True
        else: 
            return False
    
    def complementary(self):
        if self.check_if_correct_format(self.input_sequence)==True:
            self.input_sequence = self.to_seq(self.input_sequence)
            return [self.input_sequence.complement(), self.input_sequence.reverse_complement()]
        else:
            return [None, None]

    def transcribe_seq(self): 
        #tworzenie transkryptu (mRNA) na podstawie nici kodującej
        if self.check_if_correct_format(self.input_sequence)==True:
            self.input_sequence = self.to_seq(self.input_sequence)
            return self.input_sequence.transcribe() 
        else:
            return None
        
    def input_multiple_comma(self, x): #dzieli wprowadzone dane na części - po przecinkach
        input_list = re.split(',', x)
        
        #usuwanie potencjalnych białych znaków na brzegach sekwencji i pustych ciągów znaków
        input_list = [i.strip() for i in input_list if i.strip()] 
        
        return input_list
    
    def input_multiple_semicol(self, x): #dzieli wprowadzone dane na części - po średnikach
        input_list = re.split(';', x)
        
        #usuwanie potencjalnych białych znaków na brzegach sekwencji i pustych ciągów znaków
        input_list = [i.strip() for i in input_list if i.strip()] 
        
        return input_list
    
    def input_multiple_nl(self, x): #dzieli wprowadzone dane na części - po znaku nowej linii
        input_list = re.split('\n', x)
        
        #usuwanie potencjalnych białych znaków na brzegach sekwencji i pustych ciągów znaków
        input_list = [i.strip() for i in input_list if i.strip()] 
        
        return input_list
        
    def exon_list_create(self, x): #zmiana wpisanych przedziałów ('1-7, 9-12, 15-22') na listę z wartościami liczbowymi 
        exon_range_list = self.input_multiple_comma(x) #podział po średnikach i nowych liniach

        exon_range_list = [i.split("-") for i in exon_range_list] #podział na przedziałów na konkretne liczby po myślnikach

        for i in range(len(exon_range_list)): #próba zamiany na liczby całkowite
            for j in range(len(exon_range_list[i])):
                try:
                    exon_range_list[i][j] = int(exon_range_list[i][j])
                except:
                    return None
                
        return exon_range_list
        
    def splicing(self, other_input = None): #wycinanie intronów z sekwencji genomowej, zostawiając tylko eksony tworzące sekwencję kodującą
        if other_input != None:
            self.input_sequence = other_input
        if self.check_if_correct_format(self.input_sequence)==True:
            self.input_sequence = self.to_seq(self.input_sequence)
            exon_list = self.exon_list_create(self.exons) #tworzenie listy eksonów w odpowiednim formacie
            if exon_list == None: #jeśli niepoprawny format rzuca None
                return None

            cds = Seq('')

            for i in exon_list: #wybieranie tylko eksonów (włącznie z końcowym znakiem)
                cds += self.input_sequence[i[0]-1:i[1]] #'-1's accomodate for python indexing (0)

            return cds
        else:
            return None

    def check_first_stop(self):
        if self.translate_range == 'Do kodonu STOP':
            return True
        else:
            return False    

    def translate_seq(self, tab_no, other_input = None):
        if other_input != None:
            self.input_sequence = other_input
        if self.check_if_correct_format(self.input_sequence)==True and self.is_len_divisible_by_3(self.input_sequence)==True:
            
            #transkrypcja nici kodującej na mRNA
            mRNA = self.transcribe_seq() 

            if tab_no == 5:
                to_first_stop = self.check_first_stop()
            else:
                to_first_stop = False

            if to_first_stop == True: #translacja przebiega do napotkania pierwszego kodonu STOP
                protein = mRNA.translate(to_stop=True, table=1)
            else: #translacja przebiega do końca sekwencji
                protein = mRNA.translate(to_stop=False,table=1)
            return protein
        else:
            return None

    def separate_input(self, x): #dzieli wprowadzone dane na części - po znaku nowej linii, a następnie po średniku (przygotowanie danych pod jednoczesną analizę mutacji dla kliku sekwencji)
        by_new_line = self.input_multiple_nl(x) #podział po nowej linii
        res = [] 
        
        for i in by_new_line:
            res.append(self.input_multiple_semicol(i)) #podział po średniku
        #wynikiem jest lista list - główna lista rozdziela poszczególne analizowane sekwencje, lista zagnieżdżona rozdziela elementy składowe (sekwencja, miejsca mutacji i zakresy eksonów)
        return res  
    
    def mutation_list_create(self): #tworzenie listy mutacji na podstawie wielu danych wejściowych
        mutation_list = self.input_multiple_comma(self.mutations)

        formated_mutation_list = []

        for i in mutation_list:
            left = i[:1] #nukleotyd przed mutacją
            right = i[-1:] #nukleotyd po mutacji
            number = i[1:len(i)-1] #numer nukleotydu (numerowane od 1)

            if self.check_if_correct_format(left) == False:
                return None
            if self.check_if_correct_format(right) == False:
                return None
            try:
                number = int(number)
            except:
                return None 
            formated_mutation_list.append([left,number,right])    

        return formated_mutation_list
    
    def mutate_seq(self, x, mutation_list): #mutacja sekwencji genomowej na podstawie podanych miejsc mutacji
        if self.check_if_correct_format(x) == True:
            mutated_seq = MutableSeq(x) #zmiana typu na modyfikowalny
            for i in mutation_list:
                if mutated_seq[i[1]-1] == i[0]: #sprawdzenie czy podany typ/miejsce mutacji zgadza się z oryginalną sekwencją genomową
                    mutated_seq[i[1]-1] = i[2]
                else:
                    return None 
            return mutated_seq
        else:
            return None
            
    def mutation_places_in_coding(self, x, mutation_list): #znajduje miejsca (indeksy od 1) w sekwencji kodującej
        if self.check_if_correct_format(x) == True:
            cds = self.splicing(x) #przygotowanie sekwencji kodującej
            if cds is not None:
                if self.is_len_divisible_by_3(cds) == True:
                    mutated_seq = self.mutate_seq(x, mutation_list) #mutacja

                    if mutated_seq == None:
                        return [None, None, None]

                    mutated_cds = self.splicing(mutated_seq) #przygotowanie zmutowanej sekwencji kodującej

                    #porównanie sekwencji kodujących przed i po mutacji
                    cds_mutation_list = [[cds[i],i+1,mutated_cds[i]] for i in range(len(mutated_cds)) if mutated_cds[i].upper() != cds[i].upper()]

                    return [cds_mutation_list, cds, mutated_cds]
                else:
                    return [None, None, None]
            else:
                    return [None, None, None]
        else:
            return [None, None, None]
        
    def mutation_places_in_protein(self, coding, mutated_coding, mutation_places_in_coding): #znajduje miejsca i typ mutacji w łańcuchu białkowym
        protein_coding = self.translate_seq(6, coding) #translacja sekwencji przed mutacją
        protein_mutated_coding = self.translate_seq(6, mutated_coding) #translacja sekwencji po mutacji

        place_list = []
        for i in mutation_places_in_coding:
            place_list.append([protein_coding[(i[1]-1)//3], ((i[1]-1)//3)+1, protein_mutated_coding[(i[1]-1)//3]]) #miejsce/typ mutacji w łańcuchu białkowym (indeksy od 1)

        return [protein_coding, protein_mutated_coding, place_list]
    
    def analyze_mutations(self):
        #miejsca mutacji w postaci listy list - sekwencja genomowa
        mutation_places_list = self.mutation_list_create()
        
        if mutation_places_list is not None:
            #miejsca mutacji w postaci listy list - sekwencja kodująca
            [cds_mutation_list, cds, mutated_cds] = self.mutation_places_in_coding(self.input_sequence, mutation_places_list) 

            if cds_mutation_list != None and cds != None and mutated_cds != None:
                [protein_coding, protein_mutated_coding, place_list] = self.mutation_places_in_protein(cds, mutated_cds, cds_mutation_list)
            else:
                return None
        else:
            return None

        return [cds, mutated_cds, cds_mutation_list, protein_coding, protein_mutated_coding, place_list]

    def visualize_sequence_differences(self, x, y, difference_list): #podstawowa wizualizacja różnicy podanych sekwencji
        difference_list_flat0 = [i[1]-1 for i in difference_list] #wybranie tylko miejsc (indeksów od 0) mutacji z listy 

        n_columns = 50 #maksymalna liczba znaków pojawiająca się w jednym wierszu
        max_len = max(len(x), len(y)) #maksymalna liczba znaków w porównywanych sekwencjach

        if max_len%n_columns != 0: #sprawdzenie czy maksymalna liczba znaków jest podzielna przez maksymalną liczbę znaków wyświetlaną w pojedynczym wierszu
            max_len = ((max_len//n_columns)+1)*n_columns #maksymalna liczba znaków równa jest najbliższej, większej wielokrotności maksymalnej liczby znaków pojawiającej się w jednym wierszu

        #dodanie białych znaków do sekwencji, żeby miały długość równą max_len - zapobieganie błędom typu 'index out of range' przy późniejszej wizualizacji
        x += " "*(max_len-len(x))
        y += " "*(max_len-len(y))
        
        seq_row_count = max_len // n_columns #liczba wierszy na wizualizacji
        
        output = ''

        for i in range(seq_row_count): #dla każdego wiersza na wizualizacji
            for j in range(n_columns): #wyświetlane jest n_columns-znaków z sekwencji pierwszej (x)
                if (i*n_columns+j) in difference_list_flat0 and x[i*n_columns+j] == y[i*n_columns+j]: #jeśli mutacja nie zmieniła sensu sekwencji
                    output += "<font color = #238823>"
                    output += str(x[i*n_columns+j])
                    output += "</font>"
                elif x[i*n_columns+j] != y[i*n_columns+j] and y[i*n_columns+j] == '*': #jeśli mutacja zmieniła sens sekwencji (powstanie kodonu STOP)
                    output += "<font color = #2568B0>"
                    output += str(x[i*n_columns+j])
                    output += "</font>"
                elif x[i*n_columns+j] != y[i*n_columns+j] and y[i*n_columns+j] != '*': #jeśli mutacja zmieniła sens sekwencji (zmiana symbolu nukleotydu/aminokwasu)
                    output += "<font color = #d2222d>"
                    output += str(x[i*n_columns+j])
                    output += "</font>"
                else: #brak zmian w sekwencji
                    output += str(x[i*n_columns+j]) 
            output += "<br>"
            for j in range(n_columns): #wyświetlane jest n_columns-znaków z sekwencji drugiej )y
                if (i*n_columns+j) in difference_list_flat0 and x[i*n_columns+j] == y[i*n_columns+j]: #jeśli mutacja nie zmieniła sensu sekwencji
                    output += "<font color = #238823>"
                    output += str(y[i*n_columns+j])
                    output += "</font>"
                elif x[i*n_columns+j] != y[i*n_columns+j] and y[i*n_columns+j] == '*': #jeśli mutacja zmieniła sens sekwencji (powstanie kodonu STOP)
                    output += "<font color = #2568B0>"
                    output += str(y[i*n_columns+j])
                    output += "</font>"
                elif x[i*n_columns+j] != y[i*n_columns+j] and y[i*n_columns+j] != '*': #jeśli mutacja zmieniła sens sekwencji (zmiana symbolu nukleotydu/aminokwasu)
                    output += "<font color = #d2222d>"
                    output += str(y[i*n_columns+j])
                    output += "</font>"
                else: #brak zmian w sekwencji
                    output += str(y[i*n_columns+j]) 
            output += "<br>"
            for j in range(n_columns): #zaznaczenie różnic w sekwencjach znakiem '^'
                sign = "&nbsp;"
                if x[i*n_columns+j] != y[i*n_columns+j] or (i*n_columns+j) in difference_list_flat0:
                    sign = "^"
                output += sign
            output += "<br><br>"
        
        return output