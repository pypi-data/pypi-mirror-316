from rpy2 import robjects

def read_gene_trees(args, prefix, customEventAttr):
    df_rec= read_csv(f'{prefix}reconciliation.tsv', sep= '\t',  dtype= {'OG':str})
    # Mask gene trees
    if args.OGs_mask:
        df_rec= df_rec[ df_rec.OG.isin(args.OGs_mask) ]
    # Newick to nxTree
    df_rec.tree= df_rec.tree.apply(read_nhx)
    # Set mu map in proper format
    df_rec.reconciliation_map= df_rec.reconciliation_map.apply(txtMu_2_dict)
    # Set mu with nx node identifier
    df_rec.reconciliation_map= df_rec.apply(lambda row: update_mu(row.tree,
                                                    Ts, row.reconciliation_map,
                                                    'node_id', 'node_id'),
                                            axis=1)
    # Add custom event attr
    F= lambda T: add_eventAttr(T, 'label', customEventAttr)
    df_rec.tree.apply(F)
    return df_rec


desc_def= """
"""

class R_out:
    def __init__(self):
        self.capture_r_output()

    def capture_r_output(self):
        """
        Will cause all the output that normally goes to the R console,
        to end up instead in a python list.
        """
        # Import module #
        import rpy2.rinterface_lib.callbacks
        # Record output #
        self.stdout = []
        self.stderr = []
        # Dummy functions #
        def add_to_stdout(line): self.stdout.append(line)
        def add_to_stderr(line): self.stderr.append(line)
        # Keep the old functions #
        self.stdout_orig = rpy2.rinterface_lib.callbacks.consolewrite_print
        self.stderr_orig = rpy2.rinterface_lib.callbacks.consolewrite_warnerror
        # Set the call backs #
        rpy2.rinterface_lib.callbacks.consolewrite_print     = add_to_stdout
        rpy2.rinterface_lib.callbacks.consolewrite_warnerror = add_to_stderr

if __name__ == "__main__":
    from .plot_functions import get_tree_layoult, add_numbers, init_numbers, plot_dendogram, og_class_statistics, get_leaves_pos
    from .common_tools import norm_path, txtMu_2_dict, update_mu, add_eventAttr
    from .nhx_tools import read_nhx
    from .nxTree import is_leaf

    import argparse
    from importlib.metadata import version
    from pandas import read_csv
    import matplotlib.pyplot as plt
    from upsetplot import plot, UpSet

    from pandas import DataFrame, Series
    from collections import Counter
    from itertools import chain
    import seaborn as sns
    import matplotlib.patches as mpatches
    from math import ceil

    from tqdm import tqdm
    tqdm.pandas()

    V_tl= version('revolutionhtl')
    txt= f'REvolutionH-tl: Reconstruction of Evolutionaty Histories TooL (V{V_tl})'

    parser = argparse.ArgumentParser(prog= 'revolutionhtl',
                                     description=f'{txt}{desc_def}',
                                     usage='python -m revolutionhtl <arguments>',
                                     formatter_class=argparse.MetavarTypeHelpFormatter,
                                    )

    #############
    # Arguments #
    #############

    parser.add_argument('files_path',
                        help= '[str] Path of files outpued by REvolutionH-tl.',
                        type= norm_path,
                        nargs='?',
                        default= './',
                       )

    parser.add_argument('--files_prefix',
                        help= '[str] Prefix of files outpued by REvolutionH-tl.',
                        type= str,
                        nargs='?',
                        default= 'tl_project.',
                       )

    parser.add_argument('--species_order',
                        help= '[str] List of species in the desired order to plot.',
                        type= str,
                        nargs= '*',
                        default= None,
                       )

    parser.add_argument('--OGs_mask',
                        help= '[str] List of orthogroups IDs to mask gene trees at the file "gene_trees"',
                        type= str,
                        nargs= '*',
                        default= None,
                       )

    parser.add_argument('--output_path',
                        help= '[str | default: ./] Directory to save figures.',
                        type= norm_path,
                        default= './',
                       )

    parser.add_argument('--size',
                        help= '[float | default: 10] size of the side of the output figures',
                        type= float,
                        default= 10,
                       )

    parser.add_argument('--percentage_upsetplot',
                        help= '[int | default: 100] percentage of rows shown in upsetplot.',
                        type= int,
                        default= 100,
                       )

    args= parser.parse_args()

    from .hello import hello5
    print(f'{hello5}V{V_tl}\n')

    f_name= lambda name: f"{prefix}{name}.pdf"

    ####################
    # Define constants #
    ####################
    customEventAttr= 'customEventAttr'
    prefix= f'{args.files_path}{args.files_prefix}'
    s_tree_path_py= f'{prefix}labeled_species_tree.nhx'
    # Output parameters
    numbers_path= f'{prefix}gene_counts_reconciliation.tsv'

    #############
    # Load data #
    #############
    print("Loading data...")
    # Species tree
    #-------------
    with open(s_tree_path_py) as F:
        Ts= read_nhx(''.join( F.read().strip().split('\n') ))
    # Gene trees table
    #-----------------
    df_rec= read_gene_trees(args, prefix, customEventAttr)
    # Orthogroups
    #------------
    df_ogs= read_csv(f'{prefix}orthogroups.tsv', sep='\t').set_index('OG')
    # Species order and sorted leaves
    #--------------------------------
    if not args.species_order:
        _,_,_,aux= get_leaves_pos(Ts)
        args.species_order= [Ts.nodes[x]['label'] for x in aux]
    # Create a list of leaves sorted as specified by args.species_order
    label2node= {Ts.nodes[x]['label']:x for x in Ts if is_leaf(Ts,x)}
    sorted_leaves= [label2node[x] for x in args.species_order]
    # Sort columns of orthogroups dataframe
    df_ogs= df_ogs[ args.species_order ]
    # Count genes at each cell of orthogroups dataframe.
    from pandas import isna
    F= lambda X: 0 if isna(X) else len(X.split(','))
    df_ogs= df_ogs.map(F)

    # Singletones
    #------------
    df_sing= read_csv(f'{prefix}singletons.tsv', sep='\t')
    df_sing['species']= df_sing.file.str.split('.').str[0]
    singletones= df_sing.groupby('species').apply(lambda df: df.shape[0])
    # Orthologs
    #----------
    df_orth= read_csv(f'{prefix}orthologs.tsv', sep='\t')

    ################
    # Process data #
    ################
    print("Processing data...")

    # Species tree
    #-------------
    s_numbers= init_numbers(Ts)
    F= lambda row: add_numbers(row.tree, Ts, row.reconciliation_map, s_numbers)
    df_rec.progress_apply(F, axis= 1)

    df_numbers= [[Ts.nodes[vNode]['node_id'],
                  Dcounts['Dr'],
                  Dcounts['D'],
                  Dcounts['Sr'],
                  Dcounts['S'],
                  Dcounts['X'],
                 ]
                 for vNode,Dcounts in s_numbers.items() if vNode!=Ts.root]
    df_numbers= DataFrame(df_numbers, columns= ['node_id','duplication_roots','gene_gain_by_duplication','speciation_roots','genes_at_speciation','gene_loss'])
    df_numbers.to_csv(numbers_path,sep='\t',index=False)

    # UpSetPlot
    #----------
    class_statistics= og_class_statistics(df_ogs, args.species_order)

    nrows= class_statistics.shape[0]
    showRows= ceil( nrows*(args.percentage_upsetplot/100) )

    # Barplots
    #---------
    dropzero= lambda series: series[series!=0]

    # For each species classify orthogroups as single copy and multiple copy
    species_is_present= df_ogs>0
    OG_is_single_copy= df_ogs.apply(lambda row: (dropzero(row)==1).all(), axis=1)
    class_single_copy= DataFrame({'Single copy' : species_is_present.apply( lambda X: X & OG_is_single_copy ).sum(),
                                     'Multi copy' : species_is_present.apply( lambda X: X & ~OG_is_single_copy ).sum(),
                                    })
    class_single_copy.index.name= 'species'

    # For each species classify orthogroups by the number of species present
    count_species= lambda X: dropzero(X).shape[0]
    mask_sp= lambda species: df_ogs.loc[species_is_present[species]]
    class_n_species= DataFrame({species:Counter(mask_sp(species).apply(count_species, axis=1))
                                for species in df_ogs.columns})
    class_n_species.index.name= 'n_species'
    class_n_species.columns.name= None
    class_n_species= class_n_species.T
    class_n_species.index.name= 'species'
    class_n_species['Singletones']= singletones

    # For each species classify genes by the number of orthologs
    def get_n_orthologs_per_gene(df):
        df= DataFrame(chain(df[['species_a','a']].values,  df[['species_b','b']].values),
                      columns= ['species','gene'])
        df['one']= 1
        df= df.groupby('species')[['gene', 'one']].apply( lambda df: df.groupby('gene').one.sum().values ).to_dict()
        df= DataFrame([[species,x] for species,X in df.items() for x in X],
                      columns= ['species','n'])
        return df.set_index('species').n
    class_n_orthologs= get_n_orthologs_per_gene(df_orth)

    # For each species classify orthogroups as 1-1, 1-n, n-1, n-m
    species_is_single_copy= df_ogs==1
    species_is_1_n= lambda species: (species_is_single_copy[species] & ~(species_is_single_copy.drop(species, axis=1).all(axis=1)) ).sum()
    species_is_n_1= lambda species: (~species_is_single_copy[species] & species_is_single_copy.drop(species, axis=1).all(axis=1) ).sum()
    species_is_n_m= lambda species: (~species_is_single_copy[species] & ~(species_is_single_copy.drop(species, axis=1).all(axis=1)) ).sum()

    class_nm_orthogroups= DataFrame({'1-1' : species_is_present.apply( lambda X: X & OG_is_single_copy ).sum(),
                                     '1-n' : {species:species_is_1_n(species) for species in df_ogs.columns},
                                     'n-1' : {species:species_is_n_1(species) for species in df_ogs.columns},
                                     'n-m' : {species:species_is_n_m(species) for species in df_ogs.columns},
                                    })
    class_nm_orthogroups.index.name= 'species'



    ################
    # Plot figures #
    ################

    # Species tree
    #-------------
    fig, ax= plt.subplots(1,1, figsize= (3*args.size,args.size))
    plot_dendogram(Ts, s_numbers, ax, sorted_leaves= sorted_leaves)
    ax.axis('off')

    filename_tree = f_name("species_tree")
    fig.savefig(filename_tree, format="pdf", bbox_inches="tight")
    print(f'Written to {filename_tree}')

    width, height = fig.get_size_inches()
    uniform_figsize = (width, height)

    # UpSet plot
    #-----------
    upset= UpSet(class_statistics, sum_over='No. OGs',
                 sort_categories_by='input',
                 sort_by= '-cardinality',
                 intersection_plot_elements= 0,
                 orientation= 'vertical',
                 max_subset_rank= showRows,
                )

    upset.plot()

    fig= plt.gcf()
    fig.set_size_inches(3*args.size,args.size)
    for ax in fig.axes:
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    filename_upset = f_name("upset_plot")
    fig.savefig(filename_upset, format="pdf", bbox_inches="tight")
    print(f'Written to {filename_upset}')

    # Barplots
    #---------
    fig, axs= plt.subplots(4,1,sharex=True, figsize= (uniform_figsize))
    class_single_copy.plot.bar(stacked=True, ax= axs[0], rot=0, legend='reverse')
    class_n_species.plot.bar(stacked=True, ax= axs[1], rot=0, legend='reverse')
    axs[2].violinplot([class_n_orthologs[species].values for species in df_ogs.columns], positions= list(range(len(df_ogs.columns))))
    class_nm_orthogroups.plot.bar(stacked=True, ax= axs[3], rot=0, legend='reverse')

    for ax in axs:
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    axs[0].set_ylabel('Orthogroups')
    axs[1].set_ylabel('Genes')
    axs[2].set_ylabel('Genes')
    axs[3].set_ylabel('Orthogroups')
    axs[0].set_title('Single vs multy copy')
    axs[1].set_title('Species per orthogroup')
    axs[2].set_title('Orthologs per gene')
    axs[3].set_title('Orthologs and coorthologs')

    filename_barplots = f_name("barplots")
    fig.savefig(filename_barplots, format="pdf", bbox_inches="tight")
    print(f'Written to {filename_barplots}')

####

    from PyPDF2 import PdfReader, PdfWriter

    pdf_writer = PdfWriter()

    pdf_files = [filename_tree, filename_barplots, filename_upset]


    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_writer.add_page(page)

    outName= f_name('combined_plot')
    with open(outName, 'wb') as f:
        pdf_writer.write(f)
    print(f'Written to {outName}')

####

    ##################
    # Plot R summary #
    ##################
    from .r_plot_summary import modules

    # Run R modules
    rout= R_out()
    robjects.r( modules.Module_1 )
    robjects.r(f'species_tree_file <- "{s_tree_path_py}"')
    robjects.r(f'numbers_file <- "{numbers_path}"')
    robjects.r( modules.Module_2 )
    robjects.r( modules.Module_3 )
    robjects.r( modules.Module_4 )
    robjects.r( modules.Module_5 )
    robjects.r( f'o_format <- "pdf"' )
    robjects.r( f'prefix <- "{prefix}"' )
    robjects.r( modules.Module_6 )

    #######
    # End #
    #######
