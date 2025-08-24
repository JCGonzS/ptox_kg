from sql.model import (
    Chemical, ChemicalAssociation, Biosystem, Organism, Protein, ProteinMapping, ProteinAnnotation, Ortholog,
    GeneDifferential, Contrast, Dose, Timepoint
)
from sqlalchemy import select, func
import pandas as pd


def get_reactome_identifiers():
    data_file = "data/ReactomePathways.txt"
    df = pd.read_csv(data_file, sep="\t", header=None, names=["id", "name", "org"])
    select_orgs = ["Homo sapiens", "Drosophila melanogaster", "Caenorhabditis elegans", 
                   "Xenopus tropicalis", "Danio rerio", "Daphnia magna"]
    df = df[df["org"].isin(select_orgs)]
    df["id_num"] = df["id"].str.replace(r"R-[A-Z]+-", "", regex=True)
    name_to_ids = (
        df.groupby("name")["id_num"]
        .apply(lambda x: list(set(x)))  # unique IDs as list
        .to_dict()
    )
    return name_to_ids


def add_chemicals(graph, session):
    # Add chemical nodes
    for chem in session.query(Chemical).all():
        chem_id = f"chemical_{chem.ptx_code}"
        chem_attributes = {
            "type": "Chemical",
            "ptx_code": chem.full_ptx_code,
            "name": chem.name,
            "label": f"{chem.full_ptx_code} | {chem.name}"
            # "selected": chem.selected
        }
        graph.add_node(chem_id, **chem_attributes)
       
    # Add disease nodes, chemical-disease edges
    disease_dict = {}
    disease_id_counter = 1
    for assoc in session.query(ChemicalAssociation).all():
        chem_id = f"chemical_{assoc.chemical.ptx_code}"
        ext_id = assoc.external_id

        if assoc.association_type == "disease":
            # Add disease node if not present
            if ext_id not in disease_dict:
                disease_id = f"disease_{disease_id_counter}"
                disease_dict[ext_id] = disease_id
                disease_id_counter += 1
                disease_attrs = {
                    "type": "Disease",
                    "name": assoc.term,
                    "identifier": ext_id,
                    "label": f"{ext_id} | {assoc.term}"
                }
                graph.add_node(disease_id, **disease_attrs)

            disease_id = disease_dict[ext_id]
            edge_attrs = {
                "relation": "associated_to",
                "socio_affinity_score": assoc.socio_affinity_score,
                "z_score": assoc.z_score,
                "pubmed_count": assoc.pubmed_count,
                "pubmed_ids": assoc.pubmed_ids
            }
            graph.add_edge(chem_id, disease_id, **edge_attrs)

    return graph


def add_organisms(graph, session):
    for org in session.query(Organism).all():
        org_id = f"organism_{org.organism_id}"
        org_attributes = {
            "type": "Organism", 
            "scientific_name": org.scientific_name,
            "common_name": org.common_name,
            "uniprot_name": org.uniprot_acronym,
            "label": org.scientific_name
        }
        graph.add_node(org_id, **org_attributes)
    return graph


def add_biosystems(graph, session):
    for biosys in session.query(Biosystem).all():
        biosys_id = f"biosystem_{biosys.biosystem_id}"
        biosys_attributes = {
            "type": "Biosystem", 
            "label": biosys.ptox_biosystem_name,
            "code": biosys.ptox_biosystem_code
        }
        graph.add_node(biosys_id, **biosys_attributes)

        if biosys.organism:
            org_id = f"organism_{biosys.organism.organism_id}"
            graph.add_edge(biosys_id, org_id, **{"relation": "corresponds_to"})  
    return graph


def add_proteins(graph, session):
    # Add protein nodes
    for prot in session.query(Protein).yield_per(1000):
        prot_id = f"protein_{prot.protein_id}"
        prot_attributes = {
            "type": "Protein", 
            "uniprot_ac": prot.uniprot_ac,
            "uniprot_id": prot.uniprot_id,
            "gene_name": prot.gene_name,
            "name": prot.protein_name,
            "label": f"{prot.uniprot_id} | {prot.gene_name}"
        }
        graph.add_node(prot_id, **prot_attributes)
        if prot.organism:
            org_id = f"organism_{prot.organism.organism_id}"
            graph.add_edge(prot_id, org_id, **{"relation": "from"})
    
    # Add ortholog edges
    for ort in session.query(Ortholog).yield_per(1000):
        prot_id_a = f"protein_{ort.protein_id_a}"
        prot_id_b = f"protein_{ort.protein_id_b}"
        graph.add_edge(prot_id_a, prot_id_b, **{"relation": "ortholog_to", "score": ort.score})
    
    return graph


def add_protein_annotations(graph, session):
    reactome_ids = get_reactome_identifiers()
    pathway_dict = {}
    pathway_counter = 1
    for annot in session.query(ProteinAnnotation).yield_per(1000):
        source = annot.source_database
        name = annot.annotation
        prot_id = f"protein_{annot.protein_id}"
        if source == "GO":
            # later
            continue
        if name not in pathway_dict:
            pathway_id = f"pathway_{pathway_counter}"
            pathway_dict[name] = pathway_id
            pathway_counter += 1
            external_id = ""
            if source == "Reactome":
                external_id = ", ".join(["R-"+str(x) for x in reactome_ids.get(name, "")])
            pathway_attrs = {
                "type": "Pathway",
                "name": name,
                "id": external_id,
                "source": source,
                "label": f"{external_id} | {name}" if external_id else name
            }
            graph.add_node(pathway_id, **pathway_attrs)

        pathway_id = pathway_dict[name]
        edge_attrs = {
            "relation": "involved_in"
        }
        graph.add_edge(prot_id, pathway_id, **edge_attrs)
    
    return graph


def add_transcriptomics(graph, session):
    # Add nodes for Timepoints and Doses
    stmt = (
        select(
            Timepoint.timepoint_hr
        )
        .distinct()
    )
    for row in session.execute(stmt).all():
        node_id = f"timepoint_{row.timepoint_hr}hr"
        node_attrs = {
            "type": "Timepoint",
            "exposure_time": f"{row.timepoint_hr} hrs",
            "label": f"Exposure time: {row.timepoint_hr} hrs"
        }
        graph.add_node(node_id, **node_attrs)

    stmt = (select(Dose.dose_code, Dose.dose_name))
    dd = {"L": "Low", "M": "Medium", "H": "High", "Z": "Control"}
    for row in session.execute(stmt).all():
        node_id = f"dose_{row.dose_code}"
        node_attrs = {
            "type": "Dose",
            "code": row.dose_code,
            "label": f"Exposure dose: {dd[row.dose_code]}",
            "description": row.dose_name
            }
        graph.add_node(node_id, **node_attrs)

    # Add exposure nodes and 
    stmt = (
        select(
            GeneDifferential.gene,
            GeneDifferential.log2_fc,
            GeneDifferential.padj,
            Contrast.contrast_id,
            Contrast.ptox_contrast_id,
            Contrast.ptx_code,
            Biosystem.biosystem_id,
            Biosystem.ptox_biosystem_code,
            Biosystem.ptox_biosystem_name,
            Dose.dose_code,
            Timepoint.timepoint_hr,
            Protein.protein_id
        )
        .join(Contrast, GeneDifferential.contrast_id == Contrast.contrast_id)
        .join(Biosystem, Contrast.biosystem_id == Biosystem.biosystem_id)
        .join(Dose, Contrast.treatment_dose_id == Dose.dose_id)
        .join(Timepoint, Timepoint.timepoint_id == Contrast.timepoint_id)
        .join(ProteinMapping, GeneDifferential.gene == ProteinMapping.external_id)
        .join(Protein, ProteinMapping.protein_id == Protein.protein_id)
        .where(
            (GeneDifferential.padj <= 0.05) &
            (func.abs(GeneDifferential.log2_fc) > 1) &
            (Biosystem.organism_id == Protein.organism_id)
        )
        .order_by(GeneDifferential.padj.asc())
        # .limit(1000)
    )

    rows = session.execute(stmt).all()
    exposure_nodes = set()
    for row in rows:
        ptx_code = "PTX"+str(row.ptx_code).zfill(3)
        org = row.ptox_biosystem_name[0]+row.ptox_biosystem_name.split("_")[1][:2]
        exposure_id = f"exposure_{row.ptox_biosystem_code}_{org}_{ptx_code}_{row.dose_code}-dose_{row.timepoint_hr}hr"
        if exposure_id not in exposure_nodes:
            exposure_attrs = {
                "type": "Exposure"
            }
            graph.add_node(exposure_id, **exposure_attrs)
            exposure_nodes.add(exposure_id)
            biosys_id = f"biosystem_{row.biosystem_id}"
            chem_id = f"chemical_{row.ptx_code}"
            time_id = f"timepoint_{row.timepoint_hr}hr"
            dose_id = f"dose_{row.dose_code}"
            graph.add_edge(exposure_id, biosys_id, **{"relation": "sampled_from"})
            graph.add_edge(exposure_id, chem_id, **{"relation": "exposed_to"})
            graph.add_edge(exposure_id, time_id, **{"relation": "exposed_for"})
            graph.add_edge(exposure_id, dose_id, **{"relation": "exposure_dose"})
        
        protein_id = f"protein_{row.protein_id}"
        if row.log2_fc > 0:
            change = "increases"
        else:
            change = "decreases"
        edge_attrs = {
            "relation": f"{change}_expression",
            "logFC": row.log2_fc,
            "pvalue": row.padj
        }
        graph.add_edge(exposure_id, protein_id, **edge_attrs)

    return graph


def add_all_nodes_and_edges(graph, session):
    graph = add_chemicals(graph, session)
    graph = add_organisms(graph, session)
    graph = add_biosystems(graph, session)
    graph = add_proteins(graph, session)
    graph = add_protein_annotations(graph, session)
    graph = add_transcriptomics(graph, session)
    return graph    
