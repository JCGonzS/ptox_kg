from sql.model import Chemical, Biosystem, Organism, Protein, ProteinAnnotation


def fetch_chemicals(session):
    return session.query(Chemical).all()

def fetch_biosystems(session):
    return session.query(Biosystem).all()

def fetch_organisms(session):
    return session.query(Organism).all()

def fetch_proteins(session):
    return session.query(Protein).limit(10).all()

def fetch_annotations(session):
    return session.query(ProteinAnnotation).all()