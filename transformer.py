class Transformer:
    def __init__(self, project_id, location, dataset):
        self.project_id = project_id
        self.location = location
        self.dataset = dataset

    def run(self):
        # Aquí deberías añadir el código para ejecutar las vistas y transformaciones en Dataform.
        # Por simplicidad, se asume que existe una función `run_dataform_transformations`.
        run_dataform_transformations(self.project_id, self.location, self.dataset)
