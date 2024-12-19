import pandas as pd
from anndata import AnnData

from .utils import aggregate_and_filter


def edger_pseudobulk(
    adata_: AnnData,
    group_key: str,
    condition_group: str | list[str] | None = None,
    reference_group: str | None = None,
    cell_identity_key: str | None = None,
    layer: str | None = None,
    replicas_per_group: int = 10,
    min_cells_per_group: int = 30,
    bootstrap_sampling: bool = True,
    use_cells: dict[str, list[str]] | None = None,
    aggregate: bool = True,
    verbosity: int = 0,
) -> dict[str, pd.DataFrame]:
    import anndata2ri
    import rpy2.robjects as robjects
    from rpy2.rinterface_lib.embedded import RRuntimeError
    from rpy2.robjects import numpy2ri, pandas2ri
    from rpy2.robjects.conversion import localconverter

    numpy2ri.activate()

    R = robjects.r

    if aggregate:
        aggr_adata = aggregate_and_filter(
            adata_,
            group_key,
            cell_identity_key,
            layer,
            replicas_per_group,
            min_cells_per_group,
            bootstrap_sampling,
            use_cells,
        )
    else:
        aggr_adata = adata_.copy()

    with localconverter(anndata2ri.converter):
        R.assign("aggr_adata", aggr_adata)

    # defines the R function for fitting the model with edgeR
    R(_fit_model_r_script)

    if condition_group is None:
        condition_group_list = aggr_adata.obs[group_key].cat.categories
    elif isinstance(condition_group, str):
        condition_group_list = [condition_group]
    else:
        condition_group_list = condition_group

    if cell_identity_key is not None:
        cids = aggr_adata.obs[cell_identity_key].cat.categories
    else:
        cids = [""]

    tt_dict = {}
    for condition_group in condition_group_list:
        if reference_group is not None and condition_group == reference_group:
            continue

        if verbosity > 0:
            print(f"Fitting model for {condition_group}...")

        if reference_group is not None:
            gk = group_key
        else:
            gk = f"{group_key}_{condition_group}"

        try:
            R(f"""
                outs <- fit_model(aggr_adata, "{gk}", "{cell_identity_key}", verbosity = {verbosity})
                fit <- outs$fit
                y <- outs$y
            """)

        except RRuntimeError as e:
            print("Error fitting model for", condition_group)
            print("Error:", e)
            print("Skipping...")
            continue

        if reference_group is None:
            new_contrasts_tuples = [
                (
                    condition_group,  # common prefix
                    "",  # condition group
                    "not",  # reference group
                    cid,  # cell identity
                )
                for cid in cids
            ]

        else:
            new_contrasts_tuples = [
                (
                    "",  # common prefix
                    condition_group,  # condition group
                    reference_group,  # reference group
                    cid,  # cell identity
                )
                for cid in cids
            ]

        new_contrasts = [
            f"group{cnd}{prefix}_{cid}".strip("_")
            + "-"
            + f"group{ref}{prefix}_{cid}".strip("_")
            for prefix, cnd, ref, cid in new_contrasts_tuples
        ]

        for contrast, contrast_tuple in zip(new_contrasts, new_contrasts_tuples):
            prefix, cnd, ref, cid = contrast_tuple

            if ref == "not":
                cnd, ref = "", "rest"

            contrast_key = f"{prefix}{cnd}_vs_{ref}"
            if cid:
                contrast_key = f"{cell_identity_key}:{cid}|{contrast_key}"

            if verbosity > 0:
                print(f"Computing contrast: {contrast_key}... ({contrast})")

            R(f"myContrast <- makeContrasts('{contrast}', levels = y$design)")
            R("qlf <- glmQLFTest(fit, contrast=myContrast)")
            R("tt <- topTags(qlf, n = Inf)$table")
            tt: pd.DataFrame = pandas2ri.rpy2py(R("tt"))
            tt.index.name = "gene_ids"

            genes = tt.index
            cnd, ref = [c[5:] for c in contrast.split("-")]
            tt["pct_expr_cnd"] = aggr_adata.var[f"pct_expr_{cnd}"].loc[genes]
            tt["pct_expr_ref"] = aggr_adata.var[f"pct_expr_{ref}"].loc[genes]
            tt_dict[contrast_key] = tt

    return tt_dict


_fit_model_r_script = """
suppressPackageStartupMessages({
    library(edgeR)
    library(MAST)
})

fit_model <- function(adata_, group_key, cell_identity_key = "None", verbosity = 0){

    if (verbosity > 0){
        cat("Group key:", group_key, "\n")
        cat("Cell identity key:", cell_identity_key, "\n")
    }

    # create an edgeR object with counts and grouping factor    
    y <- DGEList(assay(adata_, "X"), group = colData(adata_)[[group_key]])
    # filter out genes with low counts
    if (verbosity > 1){
        cat("Dimensions before subsetting:", dim(y), "\n")
    }
    keep <- filterByExpr(y)
    y <- y[keep, , keep.lib.sizes=FALSE]
    if (verbosity > 1){
        cat("Dimensions after subsetting:", dim(y), "\n")
    }

    # normalize
    y <- calcNormFactors(y)
    # create a vector that is concatentation of condition and cell type that we will later use with contrasts
    if (cell_identity_key == "None"){
        group <- colData(adata_)[[group_key]]
    } else {
        group <- paste0(colData(adata_)[[group_key]], "_", colData(adata_)[[cell_identity_key]])
    }
    if (verbosity > 1){
        cat("Group(s):", group, "\n")
    }
    replica <- colData(adata_)$replica
    # create a design matrix: here we have multiple replicas so also consider that in the design matrix
    design <- model.matrix(~ 0 + group + replica)

    # estimate dispersion
    y <- estimateDisp(y, design = design)
    # fit the model
    fit <- glmQLFit(y, design)
    return(list("fit"=fit, "design"=design, "y"=y))
}
"""
