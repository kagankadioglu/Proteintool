from tkinter.filedialog import *


class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.initUI()
        self.data_manager = DataCenter()  #this is data center object to manage data processes.
        self.uploaded_file_counter = 0
        #this file counter counts the file that uploaded so it can begin its work to create object
        #after all files uploaded. So there will be no error according to upload order.

    def initUI(self):
        self.pack(fill=BOTH)
        self.similarity_var = StringVar()
        self.similarity_var.set("euclidean")        #variable initially setted to euclidean
        self.configure(background='gray')
        self.top_frame = Frame(self)
        self.top_frame.pack(side=TOP,fill=BOTH)
        self.header = Label(self.top_frame,text="Protein Function Prediction Tool",background="orange",font=('Arial','23','bold'),
                            foreground="white")
        self.header.pack(side=TOP,fill=BOTH,ipady=10)
        self.buttons_frame = Frame(self.top_frame)
        self.buttons_frame.pack(side=TOP,fill=BOTH)
        self.upload_annotation_button = Button(self.buttons_frame,text="UPLOAD\nANNOTATIONS",height=2,command=self.read_gaf)
        self.upload_ecv_button = Button(self.buttons_frame,text="UPLOAD EVIDENCE\nCODE VALUES",height=2,command=self.read_ecv)
        self.upload_go_button = Button(self.buttons_frame,text="UPLOAD GO FILE",height=2,command=self.read_obo)
        self.upload_annotation_button.pack(side=LEFT,padx=(300,0),pady=10)
        self.upload_ecv_button.pack(side=LEFT,padx=40,pady=10)
        self.upload_go_button.pack(side=LEFT,pady=10)
        self.body_frame = Frame(self)
        self.body_frame.pack(side=TOP,fill=BOTH)
        self.proteins_frame = Frame(self.body_frame)
        self.similarity_metric_frame = Frame(self.body_frame)
        self.similar_protein_frame = Frame(self.body_frame)
        self.predicted_function_frame = Frame(self.body_frame)
        self.proteins_frame.pack(side=LEFT,fill=BOTH,padx=(20,0),pady=10)
        self.protein_label = Label(self.proteins_frame,text="Proteins",font=('Arial','12',''))
        self.protein_listbox = Listbox(self.proteins_frame,width=35,height=18)
        self.protein_scroll = Scrollbar(self.proteins_frame)
        self.protein_listbox.configure(yscrollcommand=self.protein_scroll.set)
        self.protein_scroll.config(command=self.protein_listbox.yview)
        self.protein_label.pack(side=TOP,fill=BOTH,pady=5)
        self.protein_listbox.pack(side=LEFT,fill=BOTH)
        self.protein_scroll.pack(side=LEFT,fill=Y)
        self.similarity_label = Label(self.similarity_metric_frame,text="Similarity Metric",font=('Arial','12',''))
        self.similarity_label.pack(side=TOP,fill=BOTH,pady=5)
        self.similarity_metric_frame.pack(side=LEFT,fill=BOTH,padx=40,pady=10)
        self.bordered_frame = Frame(self.similarity_metric_frame,highlightthickness=2,highlightbackground="black")
        self.pearson_check = Checkbutton(self.bordered_frame,text="Pearson",variable=self.similarity_var,onvalue="pearson",offvalue="euclidean")
        self.euclidean_check = Checkbutton(self.bordered_frame,text="Euclidean",variable=self.similarity_var,onvalue="euclidean",offvalue="pearson")
        #offvalue makes switch effect and program always have a one of the variables onvalue.
        self.bordered_frame.pack(side=TOP,fill=BOTH,ipady=120)
        self.pearson_check.pack(side=TOP,fill=BOTH,pady=(10,0))
        self.euclidean_check.pack(side=TOP,fill=BOTH)
        self.similar_protein_frame.pack(side=LEFT,fill=BOTH,padx=(0,40),pady=10)
        self.similar_protein_label = Label(self.similar_protein_frame,text="Similar Protein",font=('Arial','12',''))
        self.similar_protein_listbox = Listbox(self.similar_protein_frame,width=35)
        self.similar_protein_scroll = Scrollbar(self.similar_protein_frame)
        self.similar_protein_listbox.configure(yscrollcommand=self.similar_protein_scroll.set)
        self.similar_protein_scroll.config(command=self.similar_protein_listbox.yview)
        self.similar_protein_label.pack(side=TOP, fill=BOTH,pady=5)
        self.similar_protein_listbox.pack(side=LEFT, fill=BOTH, padx=(10, 0))
        self.similar_protein_scroll.pack(side=LEFT, fill=Y)
        self.predicted_function_frame.pack(side=LEFT,fill=BOTH,padx=(0,20),pady=10)
        self.predicted_function_label = Label(self.predicted_function_frame,text="Predicted Function",font=('Arial','12',''))
        self.predicted_function_listbox = Listbox(self.predicted_function_frame,width=50)
        self.predicted_function_scroll = Scrollbar(self.predicted_function_frame)
        self.predicted_function_listbox.configure(yscrollcommand=self.predicted_function_scroll.set)
        self.predicted_function_scroll.config(command=self.predicted_function_listbox.yview)
        self.predicted_function_label.pack(side=TOP,fill=BOTH,pady=5)
        self.predicted_function_listbox.pack(side=LEFT,fill=BOTH)
        self.predicted_function_scroll.pack(side=LEFT,fill=Y)
        #bind event for listbox to left click
        self.protein_listbox.bind("<Button-1>",self.make_recommendation)

    #these functions are trigger functions to use datacenter's methods.
    #end all functions check if user uploaded all the files. if counter is three objects will created by datacenter.
    def read_ecv(self):
        txt_file = tkFileDialog.askopenfilename(title="Select file",filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        self.data_manager.ecv_manager(txt_file)
        self.uploaded_file_counter += 1
        if self.uploaded_file_counter == 3:
            self.data_manager.create_structure()
            self.create_recommendation_dict()

    def read_obo(self):
        obo_file = tkFileDialog.askopenfilename(title="Select file",filetypes=(("obo files", "*.obo"), ("all files", "*.*")))
        self.data_manager.obo_manager(obo_file)
        self.uploaded_file_counter +=1
        if self.uploaded_file_counter == 3:
            self.data_manager.create_structure()
            self.create_recommendation_dict()

    def read_gaf(self):
        self.protein_listbox.delete(0,END)
        gaf_file = tkFileDialog.askopenfilename(title="Select file",filetypes=(("gaf files", "*.gaf"), ("all files", "*.*")))
        self.data_manager.gaf_manager(gaf_file)
        self.uploaded_file_counter += 1
        for name in self.data_manager.temp_protein_struct.values():
            name = name[0]
            self.protein_listbox.insert(END,name)

        if self.uploaded_file_counter == 3:
            self.data_manager.create_structure()
            self.create_recommendation_dict()

    #creates recommendation format of dictionary with datas to use recommendations methods.
    def create_recommendation_dict(self):
        self.recommendation_dictionary = dict()
        for value in self.data_manager.protein_dict.values():
            protein_id = value.id
            protein_name = value.name
            inner_dict = dict()
            #{'GO:0007179': <__main__.Annotation instance at 0x000000000B797488>, 'GO:0005025': <__main__.Annotation instance at 0x000000000B797448>}
            for value2 in value.annotation_dict.values():
                go_obj = value2.functionality
                ecv_obj = value2.evidence_code
                inner_dict[go_obj.id] = ecv_obj.value
            self.recommendation_dictionary[protein_id] = inner_dict

    def make_recommendation(self,event):
        self.similar_protein_listbox.delete(0,END)
        self.predicted_function_listbox.delete(0,END)
        self.protein_listbox.update()
        name= self.protein_listbox.get(ACTIVE) #gets active item
        protein_id = self.data_manager.protein_dict[name].id
        if self.similarity_var.get() == "pearson":
            similar_protein_list = rc.topMatches(self.recommendation_dictionary,protein_id,similarity=rc.sim_pearson)
            for protein in similar_protein_list:
                protein_sim_score = protein[0]
                sim_protein_id = protein[1]
                for value in self.data_manager.protein_dict.values():
                    if value.id == sim_protein_id:
                        sim_protein_name = value.name
                line = str(protein_sim_score) + " - " + sim_protein_id + " - " + sim_protein_name
                self.similar_protein_listbox.insert(END,line)
            predicted_function_list = rc.getRecommendations(self.recommendation_dictionary,protein_id,similarity=rc.sim_pearson)
            for function in predicted_function_list:
                function_sim_score = function[0]
                sim_function_id = function[1]
                for value in self.data_manager.go_dict.values():
                    if value.id == sim_function_id:
                        sim_function_name = value.name
                line = str(function_sim_score) + " - " + sim_function_id + " - " + sim_function_name
                self.predicted_function_listbox.insert(END,line)
        else:
            similar_protein_list = rc.topMatches(self.recommendation_dictionary,protein_id,similarity=rc.sim_distance)
            for protein in similar_protein_list:
                sim_score = protein[0]
                sim_protein_id = protein[1]
                for value in self.data_manager.protein_dict.values():
                    if value.id == sim_protein_id:
                        sim_protein_name = value.name
                line = str(sim_score) + " - " + sim_protein_id + " - " + sim_protein_name
                self.similar_protein_listbox.insert(END,line)
            predicted_function_list = rc.getRecommendations(self.recommendation_dictionary,protein_id,similarity=rc.sim_distance)
            for function in predicted_function_list:
                function_sim_score = function[0]
                sim_function_id = function[1]
                for value in self.data_manager.go_dict.values():
                    if value.id == sim_function_id:
                        sim_function_name = value.name
                line = str(function_sim_score) + " - " + sim_function_id + " - " + sim_function_name
                self.predicted_function_listbox.insert(END,line)

class DataCenter:
    def __init__(self):
        self.protein_dict = dict()
        self.evidence_code_dict = dict()
        self.go_dict = dict()
        self.temp_protein_struct = dict()

    def obo_manager(self,obopath):
        counter = 0 #a counter that will be 0 after reading two lines.
        with open(obopath,"r") as obofile:
            for line in obofile:
                line = line.strip()
                if line.startswith("id:"):
                    id = line.split("id: ")[1]
                    counter += 1  #id red and counter incremented.
                else:
                    name = line.split("name: ")[1]
                    counter +=1  #name red and counter incremented
                if counter ==2: #if counter is 2 ProteinFunctionality object will be created into go_dict
                    if id.startswith("ends_"):break
                    self.go_dict[id] = ProteinFunctionality(id=id,name=name)
                    counter=0  #again counter setted to zero for next two lines.

    #simple txt reading
    def ecv_manager(self,txtpath):
        with open(txtpath,"r") as txtfile:
            for line in txtfile:
                line = line.strip()
                acronym = line.split()[0]
                value = line.split()[1]
                value = float(value)
                self.evidence_code_dict[acronym] = EvidenceCode(acronym=acronym,value=value)

    def gaf_manager(self,gafpath):
        with open(gafpath,"r") as gaffile:
            for line in gaffile:
                if line.startswith("!") == False: #if line does not starts with ! read it.
                    line = line.strip()  #get rid of extra spaces
                    protein_id = line.split()[1]
                    protein_name = line.split()[2]
                    functionality_id = line.split()[3]
                    evidence_acronym = line.split()[5]
                    #it creates temporary protein dictionary to create protein objects after uploading necessary go.obo and ecv.txt files.
                    if protein_id not in self.temp_protein_struct.keys():
                        self.temp_protein_struct[protein_id] = [protein_name,(functionality_id,evidence_acronym)]
                    else:
                        previous_element = self.temp_protein_struct[protein_id]
                        new_tuple = (functionality_id,evidence_acronym)
                        new_tuple = tuple(new_tuple)
                        previous_element.append(new_tuple)
                        self.temp_protein_struct[protein_id] = previous_element

    def create_structure(self):
        for key,value in self.temp_protein_struct.items():
            annotation_dict = {}
            protein_name = value[0]
            annotation_list = value[1::]
            for pair in annotation_list:
                go_id = pair[0]
                ecv_acr = pair[1]
                try:
                    annotation = Annotation(functionality=self.go_dict[go_id],evidence_code=self.evidence_code_dict[ecv_acr])
                    annotation_dict[go_id] = annotation
                except:
                    pass
                    #raise(Exception,"Protein name in line in .gaf file does not fit same parsing method with others!.")
            self.protein_dict[protein_name] = Protein(id=key, name=protein_name,annotation_dict=annotation_dict)


class ProteinFunctionality: #GO class
    def __init__(self,id,name):
        self.id = id
        self.name = name


class EvidenceCode: # evidence class
    def __init__(self,acronym,value):
        self.acronym = acronym
        self.value = value


class Annotation: #annotation class
    def __init__(self,functionality,evidence_code):
        self.functionality = functionality
        self.evidence_code =evidence_code


class Protein:
    def __init__(self,id,name,annotation_dict):
        self.id = id
        self.name = name
        self.annotation_dict = annotation_dict


def main():
    root.title("Protein Function Prediction Tool")
    app = Application(root)
    root.mainloop()

if __name__ == '__main__':
    root = Tk()
    main()
