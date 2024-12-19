import scanpy as sc
import anndata as ad

def split_plot_embedding(
    adata: ad.AnnData, 
    groupby: str, 
    color: list[str] | str, 
    use_rep: str = "X_umap",
    last_legend_only: bool =True, 
    **kwargs
):
    """
    Plots a split embedding, where each panel shows the 
    same colors (features) but for a different group 
    in the groupby column.

    kwargs are passed to relevant sc.pl function.
    
    Parameters
    ----------         
    adata: ad.AnnData
        The anndata object. 
        
    groupby: str 
        The name of the categorical column in `obs` to split by.
    
    color: str or list of str
        The var_names and/or obs columns to plot. One item in 
        `color` is plotted on each row. 
    
    use_rep: str (default: "X_umap"):
        The embedding in :code: `adata.obsm` to use

    last_legend_only: bool (default: True)
        If True, only the plots in the last column (right-side) 
        will have a legend. Useful to avoid crowding, however may be
        problematic when plotting categoricals where categories are
        missingin the subsetted data used for the final column, 
        as those missing categories will not appear in the legend.
        
    Returns
    -------
    fig: matplotlib.fig object
    
    """

    if (isinstance(color, str)):
        color = [color]
    elif not (isinstance(color, list)):
        print("[ERROR] color must be str or list of str")
        return None
    
    if not (use_rep in adata.obsm):
        print("[ERROR] " + str(use_rep) + " not in adata.obsm")
        return None

    # determine which plotting function to use
    # TODO: switch to sc.pl.embedding
    '''
    plot_func_dict = {
        "X_umap":    sc.pl.umap,
        "X_tsne":    sc.pl.tnse,
        "X_pca":     sc.pl.pca,
        "X_diffmap": sc.pl.diffmap
    }
    '''

    n_factor_levels = len(adata.obs[groupby].cat.categories)
    n_plots_per_factor = len(color)
    plot_size = 4
    
    fig, axs = plt.subplots(
        n_plots_per_factor, 
        n_factor_levels, 
        figsize=[plot_size * x for x in [n_factor_levels, n_plots_per_factor]]
    )

    for j,f in enumerate(adata.obs[groupby].cat.categories):
        a = adata[adata.obs[groupby]==f]
        for i,x in enumerate(color):
            if (len(color) == 1):
                axs_ij = axs[j]
            else:
                axs_ij = axs[i,j]
            
            title = x + " in " + f
            max_title_len = 50 # was 27
            if (len(title) > max_title_len):
                title = title[0:max_title_len] + "..."
            
            sc.pl.embedding(
                adata, 
                basis=use_rep,
                ax=axs_ij,
                show=False,
                na_color="#f0f0f0",
                **kwargs
            )
            sc.pl.embedding(
                a,
                basis=use_rep,
                color=x, 
                ax=axs_ij, 
                show=False,
                title=title, 
                **kwargs
            )
            axs_ij.title.set_fontsize(8)
            
            if (last_legend_only & (j<(n_factor_levels-1))):
                try:
                    axs_ij.get_legend().remove()
                except:
                    pass
        del a
    
    return fig