class Controller:
    def __init__(self, view, model):
        self.model = model
        self.view = view
    
    def set_input_sequence(self, input_sequence):
        self.model.input_sequence = input_sequence
        
    def set_exons(self, exons):
        self.model.exons = exons

    def set_mutations(self, mutations):
        self.model.mutations = mutations

    def set_translate_range(self, translate_range):
        self.model.translate_range = translate_range

    def run_complementary(self):
        self.model.output = self.model.complementary()
        return self.model.output

    def run_transcribe_seq(self):
        self.model.output = self.model.transcribe_seq()
        return self.model.output
    
    def run_splicing(self):
        self.model.output = self.model.splicing()
        return self.model.output
    
    def run_translate_seq(self, tab_no):
        self.model.output = self.model.translate_seq(tab_no)
        return self.model.output
    
    def run_input_multiple_semicol(self, content):
        return self.model.input_multiple_semicol(content)
    
    def run_separate_input(self, content):
        return self.model.separate_input(content)

    def run_analyze_mutations(self):
        return self.model.analyze_mutations()
    
    def run_visualize_sequence_differences(self, x, y, difference_list):
        return self.model.visualize_sequence_differences(x, y, difference_list)