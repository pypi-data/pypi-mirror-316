from gprofiler import GProfiler

def do_gprofiler_analysis(
    markers: list[str], 
    organism: str = "hsapiens",
    max_term_size: int = 2000,
    ordered: bool =True,
    sources: list[str] = ["GO:BP", "GO:MF", "REAC", "KEGG", "TF"]
):
    """
    Given an ordered list of genes,
    performs an over-representation analysis (ORA) 
    using the gProfiler API.

    References:

    * https://biit.cs.ut.ee/gprofiler/gost
    * https://doi.org/10.1093/nar/gkad347
    
    Parameters
    ----------
    
    markers: list of str
        List of marker genes, sorted by user
        based on FDR or other significance 
        metric.
    
    organism: str (default: "hsapiens")
        The organism ID to use for the query.
        See https://biit.cs.ut.ee/gprofiler/page/organism-list
        for a list of organism IDs supported
        by gProfiler. 
        Commonly one of: ["hsapiens", "mmusculus"]
    
    max_term_size: int (default: 2000)
        Filter results table to only include those
        results with term sizes less than this 
        maximum. Set to None to disable.
    
    ordered: bool (default: True)
        If the list of genes is ordered by
        descending significance, set to True, 
        otherwise set to False. A slightly different 
        ORA is performed on ordered gene lists. 
    
    sources: list of str (default: ["GO:BP", "GO:MF",
                                    "REAC", "KEGG", 
                                    "TF"])
        The list of source databases to consider for 
        gProfiler ORA. Some may only be available for
        certain organisms; see organism list page in
        the gProfiler documentation for more
        information.
    
    Returns
    -------
    ret: pandas.DataFrame
        The resulting gProfiler results dataframe

    """
    
    gp = GProfiler(return_dataframe=True)
    
    ret = gp.profile(
        organism=organism,
        query=markers,
        no_evidences=False,
        ordered=ordered,
        sources=sources
    )
    
    if (max_term_size) & (max_term_size > 0):
        ret = ret[ret["term_size"] < max_term_size]
    
    return ret