from dgl.data import DGLDataset
from dgl import save_graphs, load_graphs
from dgl.data.utils import save_info, load_info
import os
import numpy as np
import torch
import uuid
from typing import Dict, Union


"""DGL dataset wrapper for the O-CIQA graph question-answering dataset.
This class stores aligned triples of `(graph, question, answer)` and integrates
with `dgl.data.DGLDataset` lifecycle methods (`process`, `save`, `load`,
`has_cache`). It supports:
- single-item access by integer index, returning one `(graph, question, answer)` tuple
- slicing/index arrays, returning a new `OCIQA` subset dataset
- optional cache persistence of graphs and QA metadata
- utility mapping between node `id` values and human-readable O-RAN feature labels
Args:
    url: Optional dataset URL passed to `DGLDataset`.
    raw_dir: Directory containing raw data.
    save_dir: Directory used for processed/cache files.
    force_reload: Whether to ignore cache and reprocess.
    verbose: Whether to enable verbose DGL dataset logs.
    graphs: Optional initial list of DGL graphs.
    questions: Optional initial list of question strings/objects.
    answers: Optional initial list of answer strings/objects.
    subset: If True, disables cache save/load checks for temporary sliced datasets.
    
    
Example usage:

from dgl.dataloading import GraphDataLoader
from tqdm import tqdm

dataset = OCIQA(
        save_dir="./data/o-ciqa/V1.0.7/all_sets",
)

train_dataloader = GraphDataLoader(
        dataset,
        batch_size=1,
        shuffle=True,
)

for graph, question, answer in tqdm(train_dataloader, total=len(train_dataloader)):
    print(graph)
    print(question)
    print(answer)
"""
class OCIQA(DGLDataset):
    def __init__(self,
                 url=None,
                 raw_dir=None,
                 save_dir=None,
                 force_reload=False,
                 verbose=False,
                 graphs=None,
                 questions=None,
                 answers=None,
                 subset=False
                 
                 ):
        self._graphs = graphs if graphs is not None else []
        self._questions = questions if questions is not None else []
        self._answers = answers if answers is not None else []
        self._name = 'o-ciqa'
        self._subset = subset
        self.all_node_labels = ['F-node', 'a1_latency_mean_dl_ms', 'a1_latency_mean_ul_ms',
       'a1_latency_p90_dl_ms', 'a1_latency_p90_ul_ms',
       'a1_packet_loss_dl_percentage', 'a1_packet_loss_ul_percentage',
       'a1_retransmissions_dl_count', 'a1_retransmissions_ul_count',
       'a1_throughput_dl_kbps', 'a1_throughput_ul_kbps',
       'e2_du_latency_mean_dl_ms', 'e2_du_latency_mean_ul_ms',
       'e2_du_latency_p90_dl_ms', 'e2_du_latency_p90_ul_ms',
       'e2_du_packet_loss_dl_percentage', 'e2_du_packet_loss_ul_percentage',
       'e2_du_retransmissions_dl_count', 'e2_du_retransmissions_ul_count',
       'e2_du_throughput_dl_kbps', 'e2_du_throughput_ul_kbps',
       'f1_c_latency_mean_dl_ms', 'f1_c_latency_mean_ul_ms',
       'f1_c_latency_p90_dl_ms', 'f1_c_latency_p90_ul_ms',
       'f1_c_packet_loss_dl_percentage', 'f1_c_packet_loss_ul_percentage',
       'f1_c_retransmissions_dl_count', 'f1_c_retransmissions_ul_count',
       'f1_c_throughput_dl_kbps', 'f1_c_throughput_ul_kbps',
       'f1_u_latency_mean_dl_ms', 'f1_u_latency_mean_ul_ms',
       'f1_u_latency_p90_dl_ms', 'f1_u_latency_p90_ul_ms',
       'f1_u_packet_loss_dl_percentage', 'f1_u_packet_loss_ul_percentage',
       'f1_u_retransmissions_dl_count', 'f1_u_retransmissions_ul_count',
       'f1_u_throughput_dl_kbps', 'f1_u_throughput_ul_kbps']
        super(OCIQA, self).__init__(name=self._name,
                                         url=url,
                                         raw_dir=raw_dir,
                                         save_dir=save_dir,
                                         force_reload=force_reload,
                                         verbose=verbose,
                                         
                                         )
        
        

    def process(self):
        if len(self._graphs) == 0:
            raise ValueError("No graphs provided for processing.")
        self.graphs : np.ndarray = np.array(self._graphs)
        self.questions : np.ndarray = np.array(self._questions)
        self.answers : np.ndarray = np.array(self._answers)
        

    def __getitem__(self, idx):
        
        if isinstance(idx, torch.Tensor):
            idx = idx.cpu().numpy()
            
        if isinstance(idx, (int, np.int64)) or idx.size==1:

            if isinstance(idx, np.ndarray) and idx.size == 1:
                idx = idx.item()
            
            return self.graphs[idx], self.questions[idx], self.answers[idx]
        
        # Case 2: Slicing with a list, numpy array, or slice object
        elif isinstance(idx, (list, np.ndarray, slice)):
            # The slicing logic for subset creation (as discussed in the previous turn)
            # You must ensure this block returns a new GraphQADataset object
            new_graphs = self.graphs[idx].tolist() 
            new_questions = self.questions[idx].tolist()
            new_answers = self.answers[idx].tolist()
            
            myuuid = uuid.uuid4()
            return OCIQA(
                graphs=new_graphs,
                questions=new_questions,
                answers=new_answers,
                save_dir=f'/tmp/graph_qa_subset/{str(myuuid)}',  # Temporary save dir for subset
                subset=False 
            )
        else:
            # Fallback for unhandled types
            raise TypeError(f"Dataset index must be an integer, slice, list, or array, not {type(idx)}")

    def __len__(self):
        # Ensure __len__ works whether self.graphs is a numpy array or a list
        if hasattr(self, 'graphs'):
            return len(self.graphs)
        return len(self._graphs) # For initialization state

    
    def save(self):
        if self._subset:
            return
        # save processed data to directory `self.save_path`
        # save graphs and labels
        graph_path = os.path.join(self.save_path, 'dgl_graphs.bin')
        save_graphs(graph_path, self.graphs.tolist())
        # save other information in python dict
        qa_path = os.path.join(self.save_path, 'questions_answers.pkl')
        save_info(qa_path, {'questions': self.questions.tolist(), 'answers': self.answers.tolist()})
        

    def load(self):
        if self._subset:
            return
        # load processed data from directory `self.save_path`
        graph_path = os.path.join(self.save_path, 'dgl_graphs.bin')
        graphs, _ = load_graphs(graph_path)
        self.graphs = np.array(graphs)
        qa_path = os.path.join(self.save_path, 'questions_answers.pkl')
        info = load_info(qa_path)
        self.questions = np.array(info['questions'])
        self.answers = np.array(info['answers'])
        
        
        
        
    def has_cache(self):
        if self._subset:
            return True
        # check whether there are processed data in `self.save_path`
        graph_path = os.path.join(self.save_path, 'dgl_graphs.bin')
        qa_path = os.path.join(self.save_path, 'questions_answers.pkl')
        return os.path.exists(graph_path) and os.path.exists(qa_path)
    
    def get_node_label_list(self, graph):
        node_labels = []
        for i in range(graph.num_nodes()):
            node_id = int(graph.ndata['id'][i])
            node_labels.append(self.all_node_labels[node_id])
        return node_labels
    
    @property
    def idx_features(self) -> Dict[str, Dict[str, Union[int, np.ndarray]]]:
        
        num_nodes = len(self.all_node_labels)
        idx_map = {}

        for i, name in enumerate(self.all_node_labels):
            # Create the one-hot vector (the actual feature used by the GNN)
            one_hot_vector = np.zeros(num_nodes, dtype=np.float32)
            one_hot_vector[i] = 1.0

            idx_map[name] = {
                "index": i,
                "one_hot_vector": one_hot_vector
            }

        return idx_map, num_nodes