import pandas as pd
import os
import numpy as np
import networkx as nx
from itertools import chain
from tqdm import tqdm
tqdm.pandas()
from Bio.SeqIO.FastaIO import SimpleFastaParser
from joblib import Parallel, delayed

from .common_tools import norm_path
from .in_out import create_cBMG, tl_digraph_from_pandas
from .reduce_giant import reduce_graph
from .error import MissedData, ParameterError

####################
#                  #
# Some parameters  #
#                  #
####################

from .constants import _diamond_tl_headers, _default_f, _df_matches_cols

####################
#                  #
# Parse functions  #
#                  #
####################

normalization_modes= ['query',
                      'target',
                      'alignment',
                      'smallest',
                      'biggest',
                      'raw',
                      'Pdist',
                      'Pdist-JC',
                      'Pdist-LG',
                      'Pdist-Dayoff',
                     ]

from tqdm_joblib import tqdm_joblib

def _parse(path, f_value, singletons, fastaspath, mode= 'normal', N_max= 2000, n_jobs= 1, OGs_table= None):
    if mode not in normalization_modes:
        raise ParameterError(f'Mode for parsing only can be one of: {", ".join(normalization_modes)}')
    # Load best hits
    df_best= load_best_hits(path, mode, f_value, n_jobs, OGs_table= OGs_table)
    if OGs_table is None:
        # Identify orthogroups
        df_best, OGs_table= identify_orthogroups(df_best, N_max= N_max)
    if singletons:
        singletons= identify_singletons(OGs_table, fastaspath)
    return df_best, OGs_table, singletons

def load_orthogroups_df(path, OG_col= 'OG'):
    df= pd.read_csv(path, sep='\t')
    species= df.columns[3:]
    df[species]= df[species].map(lambda x: x if pd.isna(x) else set(x.split(',')))
    return df

def get_gene_2_orthogroup(df_OGs):
    # Dictionary orthogroup->genes
    species= df_OGs.columns[3:]
    OG_2_genes= df_OGs[species].apply(lambda X: set(chain.from_iterable(X.dropna())), axis= 1)
    # Dictionary gene -> orthogroup
    gene_2_OG= {j:i for i in OG_2_genes.index for j in OG_2_genes.loc[i]}
    N= sum((1 for i in OG_2_genes.index for j in OG_2_genes.loc[i]))
    if len(gene_2_OG) != N:
        raise ValueError('There are repeated genes')
    return gene_2_OG

def load_best_hits(path, mode, f_value, n_jobs, OGs_table= None):
    species_pairs= identify_file_pairs(path)
    # Select best hits for each pair of species
    if OGs_table is None:
        gene_2_OG= None
    else:
        gene_2_OG= get_gene_2_orthogroup(OGs_table)

    F= lambda X: pair_best_hits(X, path, mode, f_value, gene_2_OG=gene_2_OG)
    if n_jobs == 1:
        df_best= map(F, species_pairs.items())
    else:
        with tqdm_joblib(tqdm(desc="Selecting best hits", total=len(species_pairs))) as progress_bar:
            df_best= Parallel(n_jobs=n_jobs)(delayed(F)(X) for X in species_pairs.items())
    # Combine results for every pair of species
    df_best= pd.concat(df_best)
    # Check that files are not empy

    collected_species= set(map(frozenset, df_best[['Query_species','Target_species']].values))
    expected_species= set(map(frozenset, species_pairs))
    missing_species= expected_species - collected_species

    if len(missing_species)>0:
        txt= ','.join(map(lambda X: '-vs-'.join(X), missing_species))
        txt= f'There are no hits for: {txt}'
        raise MissedData(txt)

    if df_best.shape[0]==0:
        raise MissedData('There are not alignment hits in the input directory.')

    return df_best

def load_all_hits_raw(path):
    species_pairs= identify_file_pairs(path)
    # Load raw hits for each pair of species
    F= lambda X: pair_all_hits_raw(X, path)
    df_hits= map(F, species_pairs.items())
    return pd.concat(df_hits)


ext_alignment_hits= '.alignment_hits'
def identify_file_pairs(path):
    alignment_files= filter(lambda file: file.endswith(ext_alignment_hits), os.listdir(path))
    species_pairs= dict()
    for file in alignment_files:
        species_AB= simple_species_parser(file)
        species_BA= species_AB[::-1]
        if species_BA in species_pairs:
            species_pairs[species_BA]+= [file]
        else:
            species_pairs[species_AB]= [file]
    missing_files= [x for x,y in species_pairs.items() if len(y)<2]
    if len(missing_files)>0:
        TEXT= f'There are missing bidirectional-alignment hit files for the pairs of species:\n{ missing_files }'
        raise MissedData(TEXT)
    return species_pairs

def pair_best_hits(X, path, mode, f_value, gene_2_OG=None):
    species_list,file_list= X
    # Load alignment hits
    F1= [path+x for x in file_list]
    df_hits= parse_prt_hits(F1, species_list)
    # Normalize and simmetrize score
    df_hits= normalize_table(df_hits, mode)
    if not (gene_2_OG is None):
        df_hits= filter_hits_within_orthogroup(df_hits, gene_2_OG)
    # Select best hits
    return select_best_hits(df_hits, f_value)

def filter_hits_within_orthogroup(df_hits, gene_2_OG):
    F0= lambda row: (row.Query_accession in gene_2_OG) and (row.Target_accession in gene_2_OG)
    F1= lambda row: gene_2_OG[row.Query_accession]==gene_2_OG[row.Target_accession]
    F2= lambda row: F0(row) and F1(row)

    print('-----------------------------------')
    print(gene_2_OG)
    print(df_hits.apply(F0, axis= 1).sum())
    print(df_hits.apply(F1, axis= 1).sum())
    print(df_hits.apply(F2, axis= 1).sum())
    print('-----------------------------------')

    df_hits= df_hits[ df_hits.apply(F2, axis= 1) ].copy()
    columns= list(df_hits.columns)
    df_hits['OG']= df_hits.Query_accession.map(gene_2_OG)
    return df_hits[ ['OG']+columns ]

def pair_all_hits_raw(X, path):
    species_list,file_list= X
    # Load alignment hits
    F1= [path+x for x in file_list]
    return parse_prt_hits(F1, species_list)

def simple_species_parser(file):
    x0= file.find('.vs.')
    x1= x0+4
    x2= file.find(ext_alignment_hits)
    S0= file[:x0]
    S1= file[x1:x2]
    S1= '.'.join(S1.split('.')[:-1])
    return (S0,S1)

def select_best_hits(df_hits, f_value, a= 'Query_accession', b= 'Target_accession'):
    """
    Input:
    - path: A directory containing reciprocal blast-like analisis between pairs of species.
            The files contained there should be named as follows: <species_a>.fa.vs<species_b.fa>.blast
    - f_value: used for the dinamic threshold.
    """
    # Identify best hit scores w.r.t. query_gene and target_species
    w_x_B= max_hit_scores(df_hits)
    # Apply dynamic threshold for best hit selection
    #print('Selecting best hits by dynamic threshold...')
    is_best_hit= lambda row: row.Normalized_bit_score >= f_value * w_x_B[ row.Query_accession, row.Target_species ]
    mask= df_hits.apply(is_best_hit, axis= 1)

    #print('\n\n\n\n\n')
    #print(df_hits)
    #print(mask)
    #print('\n\n\n\n\n')

    df_best_hits= df_hits.loc[mask]
    return df_best_hits

def identify_orthogroups(df_best_hits,
                         Query_accession= 'Query_accession',
                         Target_accession= 'Target_accession',
                         Query_species= 'Query_species',
                         Target_species= 'Target_species',
                         N_max= 2000):
    # Create graph
    G= nx.DiGraph()
    G.add_edges_from( df_best_hits[[Query_accession,Target_accession]].values )
    # Identify connected components
    CCs= pd.Series(list(nx.weakly_connected_components(G)))
    # Reduce giant connected components
    mask_giant= CCs.apply(lambda X: len(X)>N_max)
    reduced_CCs= CCs[ mask_giant ].apply(lambda X: reduce_graph(nx.induced_subgraph(G, X), N_max= N_max))
    # Obtain singletons list
    singletons= reduced_CCs.str[1]
    singletons= set(chain.from_iterable(singletons.values))
    # Obtain graph partitions
    reduced_CCs= reduced_CCs.str[0]
    reduced_CCs= pd.Series(list(chain.from_iterable(reduced_CCs.values)), dtype='object')
    # Make final CCs list
    CCs= pd.concat((CCs[ ~mask_giant ], reduced_CCs), ignore_index= True)
    # Sort connected components by size and gene names
    CCs= pd.DataFrame(dict(CCs= CCs,
                           N= CCs.str.len(),
                           name= CCs.apply(lambda X: ''.join(sorted(''.join(X)))),
                          ))
    CCs= CCs.sort_values(by= ['N', 'name']).CCs
    # Asign a number for each connected component
    idx_2_og= dict(enumerate(CCs.values))
    D= {x: i for i,X in idx_2_og.items() for x in X}
    # Quit singletons w.r.t partition
    F= lambda x: x not in singletons
    df_best_hits= df_best_hits[ df_best_hits[Query_accession].apply(F) & df_best_hits[Target_accession].apply(F) ]
    # Keep only intra-hits w.r.t partition
    df_best_hits= df_best_hits[ df_best_hits.apply(lambda X: D[X[Query_accession]]==D[X[Target_accession]], axis= 1) ]

    # Asign a connected component to each row of dataframe
    cols= list(df_best_hits.columns)
    df_best_hits['OG']= df_best_hits[Query_accession].map(D)
    # Sort rows by OG
    df_best_hits= df_best_hits[['OG']+cols].sort_values('OG')

    # Create OGs table
    OGs_table= create_og_table(df_best_hits, idx_2_og,
                               Query_accession,
                               Target_accession,
                               Query_species,
                               Target_species)

    return df_best_hits, OGs_table

def identify_singletons(df, fastaspath):
    """
    df: dataframe for orthogroups
    fastaspath: list of fasta files
    """
    # Identify genes in orthogroups
    species_columns= list(df.columns)[3:]
    #F= lambda X: X.split(',')
    genes_og= df[species_columns].apply(lambda row: chain.from_iterable(row.dropna()) , axis= 1)
    #genes_og= df[species_columns].apply(lambda row: chain.from_iterable(F(X) for X in row.dropna()) , axis= 1)
    genes_og= set(chain.from_iterable(genes_og.values))

    # Identify genes in fasta files
    genes_fa= set()
    DD= dict()
    for file in fastaspath:
        with open(file) as F:
            fgenes= [title.split()[0] for title, _ in SimpleFastaParser(F)]
        genes_fa.update(fgenes)
        DD.update({x:file.split('/')[-1] for x in fgenes})
    singletons= genes_fa - genes_og
    singletons= [[x, DD[x]] for x in singletons]
    singletons= pd.DataFrame(singletons, columns= ['gene', 'file'])
    return singletons.sort_values('file')

def get_species_columns(genes, species, gene2species, idx):
    ret= {}
    for gene in genes:
        spec= gene2species[gene]
        ret[spec]= ret.get(spec, []) + [gene]

    nGenes= len(genes)
    nSpecies= len(ret)

    return [idx, nGenes, nSpecies] + [set(ret.get(spec, []))
                                      for spec in species]
    #return [idx, nGenes, nSpecies] + [','.join(ret.get(spec, []))
    #                                  for spec in species]

def create_og_table(df_BHs, idx_2_og,
                    Query_accession,
                    Target_accession,
                    Query_species,
                    Target_species):
    # Create genesdict
    gene2species= pd.DataFrame(
        list(df_BHs[[Query_accession,
                     Query_species]].values) + list(df_BHs[[Target_accession,
                                                            Target_species]].values
                                                   ),
        columns= ['gene', 'species']
    ).drop_duplicates().set_index('gene').species

    # Create species set
    species_list= sorted(set(gene2species))

    # Create map OG->species->gene
    OGs_table= pd.DataFrame([get_species_columns(genes, species_list, gene2species, idx)
                             for idx, genes in idx_2_og.items()],
                            columns= ['OG', 'n_genes', 'n_sepecies'] + species_list
                           )
    return OGs_table

def normalize_table(df_hits, normalization_method):
    # Normalize score
    normalized_score= normalize_scores(df_hits, normalization_method)
    F= lambda X: normalized_score[frozenset(X)]
    df_hits['Normalized_bit_score']= df_hits[['Query_accession', 'Target_accession']].apply(F, axis= 1)
    return df_hits

def normalize_scores(df, method):
    if method == 'query':
        normalized_score= df.Bit_score/df.Query_length
    elif method == 'target':
        normalized_score= df.Bit_score/df.Target_length
    elif method == 'alignment':
        normalized_score= df.Bit_score/df.Alignment_length
    elif method == 'smallest':
        normalized_score= df.Bit_score/df[['Query_length', 'Target_length']].min(axis=1)
    elif method == 'biggest':
        normalized_score= df.Bit_score/df[['Query_length', 'Target_length']].max(axis=1)
    elif method == 'raw':
        normalized_score= df.Bit_score
    elif method == 'Pdist':
        normalized_score= df.Sequence_identity.apply(lambda x:1-(x)/100)
    elif method == 'Pdist-JC':
        normalized_score= df.Sequence_identity.apply(calculate_jukes_cantor_correction)
    elif method == 'Pdist-LG':
        normalized_score= df.Sequence_identity.apply(lambda x:calculate_gamma_correction(x,1.0))
    elif method == 'Pdist-Dayoff':
        normalized_score= df.Sequence_identity.apply(lambda x:calculate_gamma_correction(x,2.25))
    else:
        raise ParameterError(f'Unrecognized method for normalization "{method}"')
    return symmetrize_scores(df, normalized_score, 'Query_accession', 'Target_accession')

def symmetrize_scores(df_hits, scores, a, b):
    # Map directed hit -> score
    DD= {(Q,T):S for Q,T,S in zip(df_hits[a], df_hits[b], scores)}
    # Set of undirected hits
    hits= {frozenset(X) for X in DD}
    # Map undirected hit -> score
    D1= {X : average_hit_scores(X,DD) for X in hits}
    return pd.Series(D1)

def average_hit_scores(X,DD):
    Q,T= X
    N=0
    S= 0
    edges= [(Q,T), (T,Q)]
    for edge in edges:
        if edge in DD:
            S+= DD[edge]
            N+= 1
    return S/N

def calculate_jukes_cantor_correction(seq_id):
    p_distance = 1-seq_id/100
    if p_distance == 0:
        return 0.0
    else:
        corrected_distance = - 19/20* log(1 - (20/19) * p_distance)
        return corrected_distance

def calculate_gamma_correction(seq_id, gamma_value):
    p_distance = 1-seq_id/100
    if p_distance == 0:
        return 0.0
    else:
        corrected_distance = gamma_value * ((1 - p_distance)**(-1/gamma_value)-1)
        return corrected_distance

pd_params= dict(names= _diamond_tl_headers, sep= '\t')
def parse_prt_hits(file_list, species_list, pd_params= pd_params):
    """
    Returns a DataFrame of hits obtained from proteinortho files
    """
    df_0= _read_bh_table(file_list[0], species_list, pd_params)
    df_1= _read_bh_table(file_list[1], species_list[::-1], pd_params)
    df= pd.concat((df_0, df_1))
    return df

def _read_bh_table(file, species, pd_params):
    df= pd.read_csv(file, **pd_params)
    columns= list(df.columns)
    df['Query_species']= species[0]
    df['Target_species']= species[1]
    return df[ ['Query_species', 'Target_species']+columns ]

def max_hit_scores(df_hits,
                   Query_accession= 'Query_accession',
                   Target_species= 'Target_species',
                   Score= 'Normalized_bit_score',
                  ):
    return df_hits.groupby([Query_accession, Target_species])[Score].max()
