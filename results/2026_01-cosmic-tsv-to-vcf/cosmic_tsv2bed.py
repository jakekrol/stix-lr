#!/usr/bin/env python3
import pandas as pd


def main() -> None:
    # Read COSMIC TSV
    df = pd.read_csv(
        "cosmic.filtered.tsv",
        sep="\t",
        low_memory=False,
        dtype={"CHROMOSOME_FROM": str, "CHROMOSOME_TO": str},
    )

    # Coordinate columns
    coord_cols = [
        "LOCATION_FROM_MIN",
        "LOCATION_FROM_MAX",
        "LOCATION_TO_MIN",
        "LOCATION_TO_MAX",
    ]

    # Ensure coordinate columns are numeric
    for col in coord_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Keep only intra-chromosomal events
    same_chrom = df["CHROMOSOME_FROM"] == df["CHROMOSOME_TO"]
    df = df[same_chrom].copy()

    # Drop rows with any missing coordinate
    df = df.dropna(subset=coord_cols)

    # For each row, choose START as the minimal coordinate and END as the maximal
    start = df[coord_cols].min(axis=1).astype("int64")
    end = df[coord_cols].max(axis=1).astype("int64")

    # SVTYPE from MUTATION_TYPE
    mt = df["MUTATION_TYPE"].astype(str).str.lower().fillna("")
    svtype = pd.Series("BND", index=df.index)
    svtype[mt.str.contains("insertion")] = "INS"
    svtype[mt.str.contains("deletion")] = "DEL"
    svtype[mt.str.contains("duplication")] = "DUP"
    svtype[mt.str.contains("inversion")] = "INV"

    # SVLEN as simple interval length (end - start)
    svlen = (end - start).astype("int64")

    # Filter out SVs with length < 50
    keep = svlen >= 50
    start = start[keep]
    end = end[keep]
    svtype = svtype[keep]
    svlen = svlen[keep]
    chrom = ("chr" + df.loc[keep, "CHROMOSOME_FROM"].astype(str))

    # Carry through COSMIC identifiers for traceability
    cosmic_struct_id = df.loc[keep, "COSMIC_STRUCTURAL_ID"].astype(str)
    cosmic_sample_id = df.loc[keep, "COSMIC_SAMPLE_ID"].astype(str)
    sample_name = df.loc[keep, "SAMPLE_NAME"].astype(str)

    out = pd.DataFrame({
        "CHROM": chrom.values,
        "START": start.values,
        "END": end.values,
        "SVTYPE": svtype.values,
        "SVLEN": svlen.values,
        "COSMIC_STRUCTURAL_ID": cosmic_struct_id.values,
        "COSMIC_SAMPLE_ID": cosmic_sample_id.values,
        "SAMPLE_NAME": sample_name.values,
    })

    # Drop exact duplicate variants (same CHROM, START, END, SVTYPE)
    out = out.drop_duplicates(subset=["CHROM", "START", "END", "SVTYPE"])

    # Sort by chromosome, then start, then end
    out = out.sort_values(by=["CHROM", "START", "END"], kind="mergesort")

    out.to_csv("cosmic.bed", sep="\t", index=False)


if __name__ == "__main__":
    main()
