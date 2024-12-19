from typing import Sequence

import numpy as np
import pandas as pd
from anndata import AnnData


def subset_obs(
    adata: AnnData,
    subset: pd.Index | Sequence[str | int | bool],
) -> None:
    """Subset observations (rows) in an AnnData object.

    This function modifies the AnnData object in-place by selecting a subset of observations
    based on the provided subset parameter. The subsetting can be done using observation
    names, integer indices, a boolean mask, or a pandas Index.

    Parameters
    ----------
    adata : AnnData
        The annotated data matrix to subset. Will be modified in-place.
    subset : pd.Index | Sequence[str | int | bool]
        The subset specification. Can be one of:
        * A pandas Index containing observation names
        * A sequence of observation names (strings)
        * A sequence of integer indices
        * A boolean mask of length `adata.n_obs`

    Examples
    --------
    >>> # Create an example AnnData object
    >>> import anndata
    >>> import pandas as pd
    >>> import numpy as np
    >>> adata = anndata.AnnData(
    ...     X=np.array([[1, 2], [3, 4], [5, 6]]),
    ...     obs=pd.DataFrame(index=['A', 'B', 'C']),
    ...     var=pd.DataFrame(index=['gene1', 'gene2'])
    ... )
    >>> # Subset using pandas Index
    >>> subset_obs(adata, pd.Index(['B', 'C']))
    >>> adata.obs_names.tolist()
    ['B', 'C']
    >>> # Subset using observation names
    >>> subset_obs(adata, ['A', 'B'])
    >>> adata.obs_names.tolist()
    ['A', 'B']
    >>> # Subset using integer indices
    >>> subset_obs(adata, [0, 1])
    >>> adata.obs_names.tolist()
    ['A', 'B']
    >>> # Subset using boolean mask
    >>> subset_obs(adata, [True, False, True])
    >>> adata.obs_names.tolist()
    ['A', 'C']

    Notes
    -----
    - The function modifies the AnnData object in-place
    - When using a boolean mask, its length must match the number of observations
    - When using integer indices, they must be valid indices for the observations
    - Invalid observation names or indices will raise KeyError or IndexError respectively
    - The order of observations in the output will match the order in the subset parameter
    """
    if isinstance(subset, pd.Index):
        adata._inplace_subset_obs(subset)
        return

    subset = np.array(subset)

    # Handle boolean mask
    if subset.dtype.kind == "b":
        if len(subset) != adata.n_obs:
            raise IndexError(
                f"Boolean mask length ({len(subset)}) does not match number of "
                f"observations ({adata.n_obs})"
            )
        subset = adata.obs_names[subset]

    # Handle integer indices
    elif subset.dtype.kind in "iu":
        if np.any(subset < 0) or np.any(subset >= adata.n_obs):
            raise IndexError(f"Integer indices must be between 0 and {adata.n_obs - 1}")
        subset = adata.obs_names[subset]

    adata._inplace_subset_obs(subset)


def subset_var(
    adata: AnnData,
    subset: pd.Index | Sequence[str | int | bool],
) -> None:
    """Subset variables (columns) in an AnnData object.

    This function modifies the AnnData object in-place by selecting a subset of variables
    based on the provided subset parameter. The subsetting can be done using variable
    names, integer indices, a boolean mask, or a pandas Index.

    Parameters
    ----------
    adata : AnnData
        The annotated data matrix to subset. Will be modified in-place.
    subset : pd.Index | Sequence[str | int | bool]
        The subset specification. Can be one of:
        * A pandas Index containing variable names
        * A sequence of variable names (strings)
        * A sequence of integer indices
        * A boolean mask of length `adata.n_vars`

    Examples
    --------
    >>> # Create an example AnnData object
    >>> import anndata
    >>> import pandas as pd
    >>> import numpy as np
    >>> adata = anndata.AnnData(
    ...     X=np.array([[1, 2, 3], [4, 5, 6]]),
    ...     obs=pd.DataFrame(index=['cell1', 'cell2']),
    ...     var=pd.DataFrame(index=['gene1', 'gene2', 'gene3'])
    ... )
    >>> # Subset using pandas Index
    >>> subset_var(adata, pd.Index(['gene2', 'gene3']))
    >>> adata.var_names.tolist()
    ['gene2', 'gene3']
    >>> # Subset using variable names
    >>> subset_var(adata, ['gene1', 'gene2'])
    >>> adata.var_names.tolist()
    ['gene1', 'gene2']
    >>> # Subset using integer indices
    >>> subset_var(adata, [0, 1])
    >>> adata.var_names.tolist()
    ['gene1', 'gene2']
    >>> # Subset using boolean mask
    >>> subset_var(adata, [True, False, True])
    >>> adata.var_names.tolist()
    ['gene1', 'gene3']

    Notes
    -----
    - The function modifies the AnnData object in-place
    - When using a boolean mask, its length must match the number of variables
    - When using integer indices, they must be valid indices for the variables
    - Invalid variable names or indices will raise KeyError or IndexError respectively
    - The order of variables in the output will match the order in the subset parameter
    """
    if isinstance(subset, pd.Index):
        adata._inplace_subset_var(subset)
        return

    subset = np.array(subset)

    # Handle boolean mask
    if subset.dtype.kind == "b":
        if len(subset) != adata.n_vars:
            raise IndexError(
                f"Boolean mask length ({len(subset)}) does not match number of "
                f"variables ({adata.n_vars})"
            )
        subset = adata.var_names[subset]

    # Handle integer indices
    elif subset.dtype.kind in "iu":
        if np.any(subset < 0) or np.any(subset >= adata.n_vars):
            raise IndexError(
                f"Integer indices must be between 0 and {adata.n_vars - 1}"
            )
        subset = adata.var_names[subset]

    adata._inplace_subset_var(subset)
