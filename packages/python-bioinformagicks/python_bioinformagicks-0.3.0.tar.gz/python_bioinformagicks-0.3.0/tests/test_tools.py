#!/usr/bin/env python

import pytest


import python_bioinformagicks as bim


@pytest.fixture
def sample_adata():
    '''
    
    Loads an ad.AnnData object from disk to use
    in tests. This is data from multiple publications
    that has been integrated and annotated before 
    subsetting to 5% of the cells and the top
    2000 highly variable genes.
    
    '''

    import anndata as ad

    return ad.read_h5ad("./tests/data/test_adata.h5ad")


def test_scale_by_group(
    sample_adata,
    groupby = "celltype"
):
    '''
    
    Testing bim.tl.scale_by_group.

    '''

    import numpy as np
    
    X = bim.tl.scale_by_group(
        sample_adata,
        groupby = groupby,
        zero_center = True
    )

    assert (X.shape == sample_adata.X.shape)
    assert (-100 < np.min(X) < 0)
    assert (0 < np.max(X) < 100)


def test_subset_by_geosketching(
    sample_adata,
    frac_cells_to_keep = 0.2,
    n_cells_to_keep = 100,
):
    '''

    Testing bim.tl.subset_by_geosketching

    '''

    import numpy as np

    mask = bim.tl.subset_by_geosketching(
        sample_adata,
        frac_cells_to_keep = frac_cells_to_keep,
    )

    assert (len(mask) == len(sample_adata.obs.index))
    assert (0 < np.sum(mask) <= (frac_cells_to_keep * len(sample_adata.obs.index))) 

    mask = bim.tl.subset_by_geosketching(
        sample_adata,
        n_cells_to_keep = n_cells_to_keep,
    )

    assert (len(mask) == len(sample_adata.obs.index))
    assert (0 < np.sum(mask) <= (n_cells_to_keep)) 




def test_calc_jasmine_score(
    sample_adata,
):
    '''

    Testing bim.tl.calc_jasmine_score

    '''
    
    import numpy as np

    genes = ["Col1a1", "Wnt2", "Enpep"]
    
    score = bim.tl.calc_jasmine_score(
        sample_adata,
        genes,
        save_rank = False
    )

    assert (len(score) == len(sample_adata.obs.index))
    assert (np.max(score) <= 1)
    assert (np.min(score) >= 0)

    score = bim.tl.calc_jasmine_score(
        sample_adata,
        genes,
        save_rank = True,
        layer = "counts_raw"
    )

    assert (len(score) == len(sample_adata.obs.index))
    assert (np.max(score) <= 1)
    assert (np.min(score) >= 0)


def test_tf_idf_markers(
    sample_adata,
    n_genes = 10,
    groupby = "celltype"
):
    '''

    Testing bim.tl.tf_idf_markers

    '''
    markers_dict = bim.tl.tf_idf_markers(
        sample_adata,
        n_genes = n_genes,
        groupby = groupby
    )

    assert (len(markers_dict.keys()) == len(sample_adata.obs[groupby].unique()))
    assert (len(markers_dict[list(markers_dict.keys())[0]]) == n_genes)