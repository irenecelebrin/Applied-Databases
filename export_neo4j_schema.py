import json
from connections import neo4j_driver

def export_schema():
    with neo4j_driver.session() as session:
        labels      = session.run('CALL db.labels()').data()
        rel_types   = session.run('CALL db.relationshipTypes()').data()
        prop_keys   = session.run('CALL db.propertyKeys()').data()
        constraints = session.run('SHOW CONSTRAINTS').data()
        indexes     = session.run('SHOW INDEXES').data()

    schema = {
        'labels': labels,
        'relationship_types': rel_types,
        'property_keys': prop_keys,
        'constraints': constraints,
        'indexes': indexes,
    }

    output_path = 'db/neo4j_schema.json'
    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2, default=str)

    print(f'Schema saved to {output_path}')

if __name__ == '__main__':
    export_schema()
