class Tree():
    def onProjectView_row_expand(self, project_view, path, column):
        project = self.project_store.get_iter(path)
        projectId = self.project_store.get_value(project, 0)
        # Buscar en Server los datos bajo el Projecto
        self.project_store.append(project,["Prj12",projectId])

