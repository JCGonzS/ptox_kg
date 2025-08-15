
def build_nodes_and_edges(chemicals, organisms, biosystems, proteins):#annotations):
    nodes = []
    edges = []

    for chem in chemicals:
        chem_id = f"chemical_{chem.ptx_code}"
        chem_attributes = {
            "type": "Chemical",
            "ptx_code": chem.full_ptx_code,
            "name": chem.name,
            "selected": chem.selected
        }
        nodes.append((chem_id, chem_attributes))
  
    for org in organisms:
        org_id = f"organism_{org.organism_id}"
        org_attributes = {
            "type": "Organism", 
            "scientific_name": org.scientific_name,
            "common_name": org.common_name,
            "uniprot_name": org.uniprot_acronym
        }
        nodes.append((org_id, org_attributes))

    for biosys in biosystems:
        biosys_id = f"biosystem_{biosys.biosystem_id}"
        biosys_attributes = {
            "type": "Biosystem", 
            "name": biosys.ptox_biosystem_name,
            "code": biosys.ptox_biosystem_code
        }
        nodes.append((biosys_id, biosys_attributes))
        if biosys.organism:
            org_id = f"organism_{biosys.organism.organism_id}"
            edges.append((biosys_id, org_id, {"relation": "corresponds_to"}))

    for prot in proteins:
        prot_id = f"protein_{prot.protein_id}"
        prot_attributes = {
            "type": "Protein", 
            "uniprot_ac": prot.uniprot_ac,
            "uniprot_id": prot.uniprot_id,
            "gene_name": prot.gene_name,
            "name": prot.protein_name
        }
        nodes.append((prot_id, prot_attributes))
        if prot.organism:
            org_id = f"organism_{prot.organism.organism_id}"
            edges.append((prot_id, org_id, {"relation": "from"}))

    # for ann in annotations:
    #     prot_id = f"protein_{ann.protein_id}"
    #     ann_id = f"annotation_{ann.id}"
    #     nodes.append((ann_id, {"type": "Annotation", "label": ann.label}))
    #     edges.append((prot_id, ann_id, {"relation": "has_annotation"}))

    return nodes, edges
